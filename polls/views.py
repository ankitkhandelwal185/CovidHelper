import humanize
import structlog
from django.core.cache import cache
from iso3166 import countries
from rest_framework.response import Response
from rest_framework.views import APIView

logger = structlog.get_logger()


class Stats(APIView):
    stat_name = {
        "confirmed": "confirmed cases",
        "deaths": "confirmed deaths",
        "active": "active cases",
        "recovered": "recovered cases",
    }

    def post(self, request):
        logger.info(
            "data {} {} {}".format(
                request.data.get("Field_country_code_Value", None),
                request.data.get("Field_state_name_Value", None),
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
                if country_code_val and state_name_val is None:
                    country_code = countries.get(country_code_val).alpha2
                    redis_key = "polls.{}.country.code:{}".format(
                        stat_type, country_code
                    )
                    if redis_key is None:
                        msg = "hmm something went wrong, I am working on it."
                    else:
                        redis_value = humanize.naturalsize(
                            cache.get(redis_key), gnu=True
                        )
                        msg = "{} {} {}".format(
                            country_code_val, self.stat_name[stat_type], redis_value
                        )
                if state_name_val:
                    redis_key = "polls.{}.country.state.code:{}".format(
                        stat_type, state_name_val
                    )
                    if redis_key is None:
                        msg = "hmm something went wrong, I am working on it."
                    else:
                        redis_value = humanize.naturalsize(
                            cache.get(redis_key), gnu=True
                        )
                        msg = "{} {} {}".format(
                            state_name_val, self.stat_name[stat_type], redis_value
                        )
        except Exception as e:
            logger.error("api/cases failed - Error: {}".format(str(e)))
            msg = "hmm something went wrong, I am working on it."
        return Response({"actions": [{"say": msg}, {"listen": True}]})


class Health(APIView):
    def get(self, request):
        return Response({"success": True})
