from django.urls import path
from categories import views


urlpatterns = [
    path('', views.CategoryList.as_view()),
]