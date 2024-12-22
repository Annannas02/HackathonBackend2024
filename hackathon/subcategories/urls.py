from django.urls import path
from subcategories import views


urlpatterns = [
    path('', views.SubcategoryList.as_view()),
]