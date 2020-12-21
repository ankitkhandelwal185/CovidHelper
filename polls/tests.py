# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import requests
import os, sys


# Create your tests here.
class StatsTestCase(TestCase):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19.settings")
    def testPost(self):
        url = "http://localhost:8020/polls/stats/"
        payload = {
            "Field_type_Value": "recovered",
            "Field_country_code": "IND"
        }
        resp = requests.post(url, payload)
        self.assertEqual(resp.status_code, 200)
