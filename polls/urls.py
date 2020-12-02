from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from polls import views

name = "polls"
urlpatterns = [
    url(r"^cases/(?P<country_code>[\w-]+)/$", views.Cases.as_view(), name="cases"),
    url(r"^deaths/(?P<country_code>[\w-]+)/$", views.Deaths.as_view(), name="deaths"),
    url(r"hello/", views.Hello.as_view(), name="hello"),
]
