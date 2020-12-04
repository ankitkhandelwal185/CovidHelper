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
    logger.info("fetch_covid_cases called")
    url = "{}/summary".format(settings.COVID_BASE_URL)
    try:
        resp = requests.get(url)
        resp_json = resp.json()
        if resp.status_code == 200:
            # global  data
            global_data = resp_json["Global"]
            global_cases_key = "polls.cases.country.code:{}".format("TOTAL")
            global_deaths_key = "polls.deaths.country.code:{}".format("TOTAL")
            global_recovered_key = "polls.recovered.country.code:{}".format("TOTAL")
            cache.set(
                global_cases_key, global_data["TotalConfirmed"], settings.CACHE_TTL
            )
            cache.set(global_deaths_key, global_data["TotalDeaths"], settings.CACHE_TTL)
            cache.set(
                global_recovered_key, global_data["TotalRecovered"], settings.CACHE_TTL
            )
            # country wise data
            countries_data = resp_json["Countries"]
            for cdata in countries_data:
                country_code = cdata["CountryCode"]
                total_cases = cdata["TotalConfirmed"]
                total_deaths = cdata["TotalDeaths"]
                total_recovered = cdata["TotalRecovered"]
                logger.info(
                    "code {}, total case {}, total deaths {}".format(
                        country_code, total_cases, total_deaths, total_recovered
                    )
                )
                cases_key = "polls.cases.country.code:{}".format(country_code)
                deaths_key = "polls.deaths.country.code:{}".format(country_code)
                recovered_key = "polls.recovered.country.code:{}".format(country_code)
                cache.set(cases_key, total_cases, settings.CACHE_TTL)
                cache.set(deaths_key, total_deaths, settings.CACHE_TTL)
                cache.set(recovered_key, total_recovered, settings.CACHE_TTL)
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


if __name__ == "__main__":
    fetchCovidCases()
