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
                request.data.get("Field_country_code_Value", None),
                request.data.get("Field_type_Value", None),
            )
        )
        try:
            redis_key = None
            msg = None
            country_code_val = request.data.get("Field_country_code_Value", None)
            stat_type = request.data.get("Field_type_Value", None)
            state_name_val = request.data.get("Field_state_name_Value", None)
            if stat_type is None or (
                country_code_val is None and state_name_val is None
            ):
                msg = "Sorry, I do not understand. Can you repeat?"
            if msg is None:
                if country_code_val:
                    country_code = countries.get(country_code_val).alpha2
                    if stat_type == "confirmed":
                        redis_key = "polls.cases.country.code:{}".format(country_code)
                    elif stat_type == "deaths":
                        redis_key = "polls.deaths.country.code:{}".format(country_code)
                    elif stat_type == "recovered":
                        redis_key = "polls.recovered.country.code:{}".format(
                            country_code
                        )
                    if redis_key is None:
                        msg = "hmm something went wrong, I am working on it."
                    else:
                        redis_value = cache.get(redis_key)
                        msg = "{} {} {}".format(
                            country_code_val, self.stat_name[stat_type], redis_value
                        )
                if state_name_val:
                    if stat_type == "confirmed":
                        redis_key = "polls.cases.country.state.code:{}".format(
                            state_name_val
                        )
                    elif stat_type == "deaths":
                        redis_key = "polls.deaths.country.state.code:{}".format(
                            state_name_val
                        )
                    elif stat_type == "recovered":
                        redis_key = "polls.recovered.country.state.code:{}".format(
                            state_name_val
                        )
                    if redis_key is None:
                        msg = "hmm something went wrong, I am working on it."
                    else:
                        redis_value = cache.get(redis_key)
                        msg = "{} {} {}".format(
                            state_name_val, self.stat_name[stat_type], redis_value
                        )

        except Exception as e:
            logger.error("api/cases failed - Error: {}".format(str(e)))
            raise APIException(str(e))
        return Response({"actions": [{"say": msg}, {"listen": True}]})


class StateStats(APIView):
    stat_name = {
        "confirmed": "confirmed cases",
        "deaths": "confirmed deaths",
        "active": "active cases",
        "recovered": "recovered cases",
    }

    def post(self, request):
        logger.info(
            "data type {} ----------- {} {}".format(
                request.data,
                request.data.get("Field_state_name_Value"),
                request.data.get("Field_type_Value"),
            )
        )
        try:
            redis_key = None
            msg = None
            state_name_val = request.data.get("Field_state_name_Value", None)
            stat_type = request.data.get("Field_type_Value", None)
            if stat_type is None or state_name_val is None:
                msg = "Sorry, I do not understand. Can you repeat?"
            if msg is None:
                if stat_type == "confirmed":
                    redis_key = "polls.cases.country.state.code:{}".format(
                        state_name_val
                    )
                elif stat_type == "deaths":
                    redis_key = "polls.deaths.country.state.code:{}".format(
                        state_name_val
                    )
                elif stat_type == "recovered":
                    redis_key = "polls.recovered.country.state.code:{}".format(
                        state_name_val
                    )
                if redis_key is None:
                    msg = "hmm something went wrong, I am working on it."
                else:
                    redis_value = cache.get(redis_key)
                    msg = "{} {} {}".format(
                        state_name_val, self.stat_name[stat_type], redis_value
                    )
        except Exception as e:
            pass
        return Response({"actions": [{"say": msg}, {"listen": True}]})


class Hello(APIView):
    def get(self, request):
        return Response({"success": True})
