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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19.settings")
    start_datetime = "2020-03-01T00:00:00Z"
    curr_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    logger.info("fetch_covid_cases for time: {}".format(curr_datetime))
    url = "https://api.covid19api.com/summary"
    resp = requests.get(url)
    print("status ".format(resp.status_code))
    if resp.status_code == 200:
        # global  data
        global_data = resp.json()["Global"]
        global_cases_key = "polls.cases.country.code:{}".format("TOTAL")
        global_deaths_key = "polls.deaths.country.code:{}".format("TOTAL")
        cache.set(global_cases_key, global_data["TotalConfirmed"])
        cache.set(global_deaths_key, global_data["TotalDeaths"])
        # country wise data
        countries_data = resp.json()["Countries"]
        for cdata in countries_data:
            country_code = cdata["CountryCode"].encode("utf-8")
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
                resp.status_code, resp.text
            )
        )


def fetchCovidDeaths(*args, **kwrgs):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    pass


if __name__ == "__main__":
    fetchCovidCases()
