from django.urls import path
from personalization import views


urlpatterns = [
    path('', views.PersonalizationList.as_view()),
]