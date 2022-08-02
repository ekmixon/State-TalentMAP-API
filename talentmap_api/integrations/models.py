import datetime
import logging
import os

from dateutil.relativedelta import relativedelta
from dateutil import tz
import defusedxml.lxml as ET

from django.db import models
from django.apps import apps
from django.utils import timezone

from requests.exceptions import Timeout as TimeoutException

from talentmap_api.integrations.synchronization_helpers import get_synchronization_information, get_soap_client, generate_soap_header
from talentmap_api.common.xml_helpers import XMLloader
from talentmap_api.common.common_helpers import ensure_date
from talentmap_api.settings import get_delineated_environment_variable


class SynchronizationJob(models.Model):
    '''
    Represents a synchronization job, consisting of a database model, WSDL commands,
    and timing.

    Synchronization jobs are evaluated by the synchronize_data command, which should
    be called by the deployment environment's scheduling software (e.g. cron)
    '''

    # Some useful time constants, in seconds
    TIME_YEAR = 31536000
    TIME_WEEK = 604800
    TIME_DAY = 86400
    TIME_HOUR = 3600
    TIME_MINUTE = 60
    TIME_SECOND = 1

    last_synchronization = models.DateTimeField(default="1975-01-01T00:00:00Z", help_text="The last time this model was synchronized")
    next_synchronization = models.DateTimeField(null=True, help_text="The next synchronization event")
    delta_synchronization = models.IntegerField(default=TIME_DAY, help_text="The time, in seconds, between synchronizations")
    running = models.BooleanField(default=False, help_text="Whether the synchronization job is currently running")

    talentmap_model = models.TextField(unique=True, help_text="The talentmap model as a string; e.g. position.Position")

    priority = models.IntegerField(default=0, help_text='The job priority, higher numbers run later. Default 0')
    use_last_date_updated = models.BooleanField(default=False, help_text='Denotes if the job should only pull newest records')

    @staticmethod
    def get_scheduled():
        '''
        Returns all SynchronizationJob who should be run (any job whose last sync + delta is in the past)
        '''
        return SynchronizationJob.objects.filter(next_synchronization__lte=timezone.now(), running=False).order_by('priority')

    def synchronize(self, soap_function="IPMSDataWebService", test=False):
        '''
        Runs the SynchronizationJob

        Args:
            soap_function (str) - The function to call on the SOAP client
            test (bool) - Indicates if we should use the testing method of the SOAP client
        '''
        start = datetime.datetime.utcnow()
        self.running = True
        self.save()
        self.job_item_count = 0
        try:
            logger = logging.getLogger(__name__)

            logger.info("Getting SOAP client")

            client = get_soap_client(soap_function=soap_function, test=test)

            logger.info(f"Using function {soap_function}")

            synchronization_tasks = get_synchronization_information(self.talentmap_model)

            last_date_updated = None
            if self.use_last_date_updated:
                # TalentMAP uses UTC, but some integrations do not
                to_local = tz.gettz('America/New_York')
                last_date_updated = self.last_synchronization.replace(tzinfo=tz.tzutc())
                last_date_updated = last_date_updated.astimezone(to_local).strftime('%Y/%m/%d %H:%M:%S')
                logger.info(f"Using last updated date: {last_date_updated}")

            for task in synchronization_tasks:
                logger.info(f"Running task {task.__name__}")
                soap_arguments, instance_tag, tag_map, collision_field, post_load_function, override_loading_method = task(last_updated_date=last_date_updated)
                model = apps.get_model(self.talentmap_model)

                logger.info("Intializing XML loader")

                loader = XMLloader(model, instance_tag, tag_map, 'update', collision_field, override_loading_method, logger)

                logger.info("Loader initialized, pulling XML data")

                '''
                The XML data from DOS SOAP comes back in batches, we need to use the last 'collision_field'
                as the PaginationStartKey of the next request, and continue until we get no more results
                '''
                new_ids = []
                updated_ids = []
                soap_function_name = soap_function
                previous_lpsk = None
                while True:
                    if loader.last_pagination_start_key:
                        if previous_lpsk == loader.last_pagination_start_key:
                            # Prevents getting stuck in a loop on the last page
                            break
                        # Store this as the previous lpsk
                        previous_lpsk = str(int(loader.last_pagination_start_key) + 1)
                        # Set the pagination start key to our last collision field; which should be the remote data's primary key
                        soap_arguments['PaginationStartKey'] = previous_lpsk
                        logger.info(f"Requesting page from primary key: {loader.last_pagination_start_key}")
                    else:
                        logger.info("Requesting first page")

                    # Get the data
                    response_xml = None
                    pre_data_time = datetime.datetime.now()
                    max_attempts = int(get_delineated_environment_variable('SOAP_MAX_ATTEMPTS', 5))
                    if not test:  # pragma: no cover
                        attempts = 0
                        while not response_xml and attempts <= max_attempts:
                            attempts += 1
                            try:
                                with client.options(timeout=int(get_delineated_environment_variable('SOAP_TIMEOUT', 180))):
                                    response_xml = ET.tostring(getattr(client.service, soap_function_name)(**soap_arguments), encoding="unicode")
                            except TimeoutException as e:
                                logger.error(f"SOAP call for {task} timed out")
                                logger.exception(e)
                                if attempts > max_attempts:
                                    logger.error(f"SOAP call for {task} exceeded max attempts.")
                                    break
                    else:
                        response_xml = ET.tostring(getattr(client.service, soap_function_name)(**soap_arguments), encoding="unicode")

                    if not response_xml:
                        logger.error(f"SOAP data for {task} is null, exiting {task}")
                        break
                    data_elapsed_time = (datetime.datetime.now() - pre_data_time).total_seconds()
                    logger.info(f"Retrieved SOAP response in {data_elapsed_time} seconds")
                    newer_ids, updateder_ids = loader.create_models_from_xml(response_xml, raw_string=True)

                    # If there are no new or updated ids on this page, we've reached the end
                    # Also, if the loader has no last pagination start key, we break
                    if (len(newer_ids) == 0 and len(updateder_ids) == 0) or not loader.last_pagination_start_key:
                        break

                    logger.info(f"Got: {len(newer_ids)} new, {len(updateder_ids)} updated this page")

                    # Append our newer and updated-er ids to our total list
                    new_ids = new_ids + newer_ids
                    updated_ids = updated_ids + updateder_ids

            logger.info("Data pull complete")

            # Run the post load function, if it exists
            if callable(post_load_function):
                logger.info(f"Calling post-load function for model {model}")
                post_load_function(model, new_ids, updated_ids)

            logger.info("Synchronization complete")
            d = relativedelta(datetime.datetime.utcnow(), start)
            logger.info(f"Synchronization Report\n\tModel: {self.talentmap_model}\n\tNew: {len(new_ids)}\n\tUpdated: {len(updated_ids)}\n\tElapsed time: {d.days} d {d.hours} hr {d.minutes} min {d.seconds} s\t\t")

            # Successful, set the last synchronization
            self.last_synchronization = timezone.now()
            self.job_item_count = self.job_item_count + len(updated_ids) + len(new_ids)
        except Exception as e:  # pragma: no cover
            logger.exception(e)
        finally:
            self.running = False
            self.save()
            return self.job_item_count

    def save(self, *args, **kwargs):
        self.next_synchronization = ensure_date(self.last_synchronization) + relativedelta(seconds=self.delta_synchronization)
        super(SynchronizationJob, self).save(*args, **kwargs)

    def __str__(self):
        d = relativedelta(seconds=self.delta_synchronization)
        status_string = f"Last@{self.last_synchronization} Next@+{self.next_synchronization} ∆[{d.years}y {d.months}mo {d.days}d {d.hours}hr {d.minutes}min {d.seconds}s]"
        if self.running:
            status_string = "IN PROGRESS"
        return f"SynchronizationJob (Priority: {self.priority}) (Use Last Updated: {self.use_last_date_updated}) - {self.talentmap_model}: {status_string}"

    class Meta:
        managed = True
        ordering = ["talentmap_model"]
