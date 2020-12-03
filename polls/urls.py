from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from polls import views

name = "polls"
urlpatterns = [
    url(r"^cases/(?P<country_code>[\w-]+)/$", views.Cases.as_view(), name="cases"),
    url(r"^stats/$", views.Stats.as_view(), name="cases"),
    url(r"hello/", views.Hello.as_view(), name="hello"),
]
