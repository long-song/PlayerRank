from django.urls import path
from django.conf.urls import url
from playerRank_list import views

urlpatterns = [
    url(r'fraction/$', views.Fraction.as_view()),
]
