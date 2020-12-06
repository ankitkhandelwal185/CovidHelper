# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from datetime import datetime
import django_rq
import os
import structlog
from datetime import datetime
logger = structlog.get_logger()


class PollsConfig(AppConfig):
    name = 'polls'
    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":
            from .helpers import fetchCovidCasesCountryWise,fetchCovidCasesStateWise
            logger.info(f"Scheduling: curr time {datetime.utcnow()}")
            scheduler = django_rq.get_scheduler("default")
            # Delete any existing jobs in scheduler
            for job in scheduler.get_jobs():
                job.delete()
            scheduler.schedule(
                datetime.utcnow(),
                func=fetchCovidCasesCountryWise,
                args=[],
                kwargs={},
                interval=3600,
                repeat=None,
                meta={"foo": "bar"},
            )
            scheduler.schedule(
                datetime.utcnow(),
                func=fetchCovidCasesStateWise,
                args=[],
                kwargs={},
                interval=3600,
                repeat=None,
                meta={"foo": "bar"},
            )
