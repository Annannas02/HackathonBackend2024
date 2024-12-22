from rest_framework import generics
from articles import models, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from popularity.models import Popularity
from articles.models import Articles
from personalization.models import Personalization
from users.models import User
from categories.models import Categories


class ArticleList(generics.ListCreateAPIView):

    queryset = models.Articles.objects.all()
    serializer_class = serializers.ArticlesSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_top_articles(request):
    user = request.user

    # Check if the user has entries in the Personalization table
    user_personalizations = Personalization.objects.filter(user_id=user)
    
    if user_personalizations.exists():
        # Get subcategories sorted by the highest personalization value
        subcategories = user_personalizations.order_by('-value')
        print (subcategories)
        articles = []

        # Fetch articles by subcategories and their popularity
        for subcategory in subcategories:
            subcategory_articles = Popularity.objects.select_related('article_id').filter(
                article_id__subcategory_id=subcategory.subcategory_id
            ).order_by('-value')
            articles.extend(subcategory_articles)

        # Sort the combined articles list by popularity
        articles = sorted(articles, key=lambda x: x.value, reverse=True)[:10]

        # Prepare the response
        response = [
            {
                "article_id": article.article_id.id,
                "title": article.article_id.title,
                "authors": article.article_id.authors,
                "summary": article.article_id.summary,
                "popularity": article.value,
                "subcategory": article.article_id.subcategory_id.name,
            }
            for article in articles
        ]

        return Response(response, status=status.HTTP_200_OK)
    
    # Fetch the top 10 articles overall by popularity if no personalization entries
    top_articles = Popularity.objects.select_related('article_id').order_by('-value')[:10]

    # Prepare the response
    response = [
        {
            "article_id": article.article_id.id,
            "title": article.article_id.title,
            "authors": article.article_id.authors,
            "summary": article.article_id.summary,
            "popularity": article.value,
            "subcategory": article.article_id.subcategory_id.name,
        }
        for article in top_articles
    ]

    return Response(response, status=status.HTTP_200_OK)