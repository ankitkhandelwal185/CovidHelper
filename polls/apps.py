# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from datetime import datetime
import django_rq
import os

class PollsConfig(AppConfig):
    name = 'polls'
    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":
            from .helpers import fetchCovidCases
            print("Scheduling")
            scheduler = django_rq.get_scheduler("default")
            # Delete any existing jobs in scheduler
            for job in scheduler.get_jobs():
                job.delete()
            # run every minute
            scheduler.schedule(
                datetime.utcnow(),
                func=fetchCovidCases,
                args=[],
                kwargs={},
                interval=3600,
                repeat=None,
                meta={"foo": "bar"},
            )
