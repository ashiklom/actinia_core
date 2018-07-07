# -*- coding: utf-8 -*-
import unittest
import time
import datetime
from copy import deepcopy
from actinia_core.resources.common.process_queue import create_process_queue, enqueue_job, stop_process_queue
from actinia_core.resources.common.resource_data_container import ResourceDataContainer
from actinia_core.resources.common.app import flask_app
try:
    from .test_resource_base import ActiniaResourceTestCaseBase, global_config
except:
    from test_resource_base import ActiniaResourceTestCaseBase, global_config

__license__ = "GPLv3"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__      = "soerengebbert@googlemail.com"


def job_with_exception(rdc):
    print("job_with_exception", rdc.api_info, rdc.orig_time)
    time.sleep(3)
    raise Exception("job_with_exception")


def job_short_run(rdc):
    for i in range(3):
        print("job_short_run", rdc.api_info, rdc.orig_time)
        time.sleep(1)


def job_long_run(rdc):
    for i in range(8):
        print("job_long_run", rdc.api_info, rdc.orig_time)
        time.sleep(3)


class ProcessQueueTestCase(unittest.TestCase):
    """
    This class tests the api logging interface
    """
    def setUp(self):
        # We need to set the application context
        self.app_context = flask_app.app_context()
        self.app_context.push()
        # The test user
        self.user_id = "soeren"

        global global_config
        global_config.NUMBER_OF_WORKERS = 2

        self.rdc = ResourceDataContainer(grass_data_base="grass_data_base",
                                         grass_user_data_base="grass_user_data_base",
                                         grass_base_dir="grass_base_dir",
                                         request_data={"request_data":None},
                                         user_id="user_id",
                                         user_group="user_group",
                                         user_credentials={"user_credentials":None},
                                         resource_id="resource_id",
                                         status_url="status_url",
                                         api_info="api_info",
                                         resource_url_base="resource_url_base",
                                         orig_time=time.time(),
                                         orig_datetime=datetime.datetime.now(),
                                         config=global_config,
                                         location_name="location_name",
                                         mapset_name="mapset_name",
                                         map_name="map_name")

    def tearDown(self):
        self.app_context.pop()

    def otest_1(self):

        create_process_queue(config=global_config, use_logger=False)

        args = deepcopy(self.rdc)
        args.api_info = 0

        enqueue_job(30, job_with_exception, args)

        args = deepcopy(self.rdc)
        args.api_info = 1

        enqueue_job(30, job_short_run, args)

        args = deepcopy(self.rdc)
        args.api_info = 2

        enqueue_job(30, job_short_run, args)

        args = deepcopy(self.rdc)
        args.api_info = 3

        enqueue_job(30, job_short_run, args)

        args = deepcopy(self.rdc)
        args.api_info = 4

        enqueue_job(1, job_short_run, args)

        args = deepcopy(self.rdc)
        args.api_info = 5

        enqueue_job(30, job_long_run, args)

        args = deepcopy(self.rdc)
        args.api_info = 6

        enqueue_job(30, job_long_run, args)

        time.sleep(20)
        stop_process_queue()
        return


if __name__ == '__main__':
    unittest.main()