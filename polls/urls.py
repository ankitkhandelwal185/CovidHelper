from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from polls import views

name = "polls"
urlpatterns = [
    url(r"^stats/$", views.Stats.as_view(), name="cases"),
    url(r"hello/", views.Health.as_view(), name="health"),
]
