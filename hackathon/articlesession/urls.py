from django.urls import path
from articlesession import views


urlpatterns = [
    path('', views.ArticlesessionList.as_view()),
]