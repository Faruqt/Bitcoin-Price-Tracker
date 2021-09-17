from django.urls import path
from .views import chart

urlpatterns = [
    path("", chart, name="chart"),
]
