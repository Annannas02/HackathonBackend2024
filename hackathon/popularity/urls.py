from django.urls import path
from popularity import views


urlpatterns = [
    path('', views.PopularityList.as_view()),
]