from django.core.cache import cache
from django.http import Http404
from iso3166 import countries
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import structlog

logger = structlog.get_logger()


class Cases(APIView):
    def searchCode(self, code):
        # JSON file
        data = open("countrycode.json", "r")
        jsonList = json.loads(data)
        for jsonObj in jsonList:
            if code.lower() == jsonObj["code"].lower():
                return True
        return False

    def get(self, request, country_code):
        country_code = country_code.upper()
        logger.info("Calling api/Cases, country_code: {}".format(country_code))
        try:
            redis_key = "polls.cases.country.code:{}".format(country_code)
            data = cache.get(redis_key)
        except Exception as e:
            logger.error("api/cases failed - Error: {}".format(str(e)))
            raise APIException(str(e))
        return Response(
            {"success": True, "msg": "{} Active Case {}".format(country_code, data)}
        )

    def post(self, request):
        data = request.data
        country_code = data.get("country_code").upper()
        type = data.get("type")
        logger.info(
            "Calling api/Cases, country_code: {} and type {}".format(country_code, type)
        )
        try:
            if type == "active":
                redis_key = "polls.cases.country.code:{}".format(country_code)
            elif type == "deaths":
                redis_key = "polls.deaths.country.code:{}".format(country_code)
            data = cache.get(redis_key)
        except Exception as e:
            logger.error("api/cases failed - Error: {}".format(str(e)))
            raise APIException(str(e))
        return Response(
            {
                "success": True,
                "msg": "{} {} {}".format(country_code, self.stat_name[type], data),
            }
        )


class Stats(APIView):
    stat_name = {
        "confirmed": "confirmed cases",
        "deaths": "confirmed deaths",
        "active": "active cases",
        "recovered": "recovered cases",
    }

    def get(self):
        pass

    def post(self, request):
        logger.info(
            "data type {} ----------- {} {}".format(
                request.data,
                request.data.get("Field_country_code_Value"),
                request.data.get("Field_type_Value"),
            )
        )
        country_code = request.data.get("Field_country_code_Value")
        stat_type = request.data.get("Field_type_Value")
        logger.info(
            "Calling api/Cases, country_code: {} and type {}".format(
                country_code, stat_type
            )
        )
        try:
            if stat_type == "active":
                redis_key = "polls.cases.country.code:{}".format(country_code)
            elif stat_type == "deaths":
                redis_key = "polls.deaths.country.code:{}".format(country_code)
            redis_value = cache.get(redis_key)
            msg = "{} {} {}".format(
                country_code, self.stat_name[stat_type], redis_value
            )
        except Exception as e:
            logger.error("api/cases failed - Error: {}".format(str(e)))
            raise APIException(str(e))
        return Response({"actions": [{"say": msg}, {"listen": True}]})


class Hello(APIView):
    def get(self, request):
        return Response({"success": True})
