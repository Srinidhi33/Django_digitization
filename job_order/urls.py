from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="job-order-home"),
    path("request/", views.job_request, name="job-request")
]
