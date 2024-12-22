from django.urls import path
from articles import views


urlpatterns = [
    path('', views.ArticleList.as_view()),
    path('fetch/', views.get_top_articles),
    path('add/', views.add_article),
    path('click/', views.select_article),
    path('id/', views.get_article_by_id),
]