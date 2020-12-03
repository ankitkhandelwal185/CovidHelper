from django.core.cache import cache
from django.http import Http404
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
        logger.info("Calling api/Cases, country_code: {} and type {}".format(country_code, type))
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
            {"success": True, "msg": "{} {} {}".format(country_code, self.stat_name[type], data)}
        )


class Hello(APIView):
    def get(self, request):
        return Response({"success": True})
