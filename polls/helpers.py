from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.http import Http404
import requests
import json
import os
import sys
import structlog
logger = structlog.get_logger()



def fetchCovidCases(*args, **kwrgs):
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.append(BASE_DIR)
    # from django.core.wsgi import get_wsgi_application
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19.settings")
    logger.info("fetch_covid_cases called")
    url = "https://api.covid19api.com/summary"
    try:
        resp = requests.get(url)
        resp_json = resp.json()
        if resp.status_code == 200:
            # global  data
            global_data = resp_json["Global"]
            global_cases_key = "polls.cases.country.code:{}".format("TOTAL")
            global_deaths_key = "polls.deaths.country.code:{}".format("TOTAL")
            cache.set(global_cases_key, global_data["TotalConfirmed"])
            cache.set(global_deaths_key, global_data["TotalDeaths"])
            # country wise data
            countries_data = resp_json["Countries"]
            for cdata in countries_data:
                country_code = cdata["CountryCode"]
                total_cases = cdata["TotalConfirmed"]
                total_deaths = cdata["TotalDeaths"]
                logger.info(
                    "code {}, total case {}, total deaths {}".format(
                        country_code, total_cases, total_deaths
                    )
                )
                redis_key = "polls.cases.country.code:{}".format(country_code)
                cache.set(redis_key, total_cases)
                redis_key = "polls.deaths.country.code:{}".format(country_code)
                cache.set(redis_key, total_deaths)
            logger.info("covid updates successfully fetched")
        else:
            logger.info(
                "error while fetching covid updates status {} err {}".format(
                    resp.status_code, resp_json
                )
            )
    except Exception as e:
        logger.info(
            "error while fetching covid updates status {} err {}".format(
                resp.status_code, resp.text
            )
        )