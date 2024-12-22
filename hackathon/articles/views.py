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
from subcategories.models import Subcategories
from articles.serializers import ArticleSelectionSerializer, ArticlesSerializer
from articlesession.models import Articlesession
from django.utils import timezone

class ArticleList(generics.ListCreateAPIView):

    queryset = models.Articles.objects.all()
    serializer_class = serializers.ArticlesSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_top_articles(request):
    user = request.user

    # Get the category from query params or payload
    category_name = request.query_params.get('category') or request.data.get('category')

    # If a category is provided, validate it
    category = None
    if category_name:
        try:
            category = Categories.objects.get(name=category_name)
        except Categories.DoesNotExist:
            return Response(
                {"error": f"Category '{category_name}' not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    # Check if the user has entries in the Personalization table
    user_personalizations = Personalization.objects.filter(user_id=user)
    
    if user_personalizations.exists():
        # Get subcategories sorted by the highest personalization value
        subcategories = user_personalizations.order_by('-value')
        articles = []

        # Fetch articles by subcategories and their popularity
        for subcategory in subcategories:
            subcategory_articles = Popularity.objects.select_related('article_id').filter(
                article_id__subcategory_id=subcategory.subcategory_id
            )
            if category:  # Filter by category if specified
                subcategory_articles = subcategory_articles.filter(
                    article_id__category_id=category
                )
            articles.extend(subcategory_articles.order_by('-value'))

        # Sort the combined articles list by popularity
        articles = sorted(articles, key=lambda x: x.value, reverse=True)[:10]

    else:
        # Fetch the top 10 articles overall or by category
        articles_query = Popularity.objects.select_related('article_id')
        if category:  # Filter by category if specified
            articles_query = articles_query.filter(article_id__category_id=category)
        articles = articles_query.order_by('-value')[:10]

    # Prepare the response
    response = [
        {
            "article_id": article.article_id.id,
            "title": article.article_id.title,
            "authors": article.article_id.authors,
            "summary": article.article_id.summary,
            "popularity": article.value,
            "subcategory": article.article_id.subcategory_id.name,
            "category": article.article_id.category_id.name,
        }
        for article in articles
    ]

    return Response(response, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_article(request):
    try:
        # Get required fields from request data
        title = request.data.get("title")
        authors = request.data.get("authors")
        publish_date = request.data.get("publish_date")
        modify_date = request.data.get("modify_date")
        summary = request.data.get("summary")
        category_name = request.data.get("category")
        subcategory_name = request.data.get("subcategory")
        identifier = request.data.get("identifier")

        identifiers = Articles.objects.filter(identifier=identifier).first()

        if identifiers:
            return Response({"error": f"{identifiers} exists."}, status=status.HTTP_404_NOT_FOUND)


        # Validate category and subcategory
        try:
            category = Categories.objects.get(name=category_name)
        except Categories.DoesNotExist:
            return Response({"error": f"Category '{category_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            subcategory = Subcategories.objects.get(name=subcategory_name, category_id=category)
        except Subcategories.DoesNotExist:
            return Response({"error": f"Subcategory '{subcategory_name}' not found in category '{category_name}'."}, status=status.HTTP_404_NOT_FOUND)

        print("arrivedhere")
        # Create the Article
        article = Articles.objects.create(
            title=title,
            authors=authors,
            publish_date=publish_date,
            modify_date=modify_date,
            summary=summary,
            category_id=category,
            subcategory_id=subcategory,
            identifier=identifier
        )

        # Create a corresponding entry in the Popularity table with value 0
        Popularity.objects.create(
            article_id=article,
            value=0
        )

        return Response({
            "message": "Article added successfully.",
            "article": {
                "id": article.id,
                "title": article.title,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "modify_date": article.modify_date,
                "summary": article.summary,
                "category": category.name,
                "subcategory": subcategory.name,
                "identifier": article.identifier
            },
            "popularity": {"value": 0}
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_article(request):
    user = request.user
    serializer = ArticleSelectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    article_id = serializer.validated_data['article_id']
    time_spent = serializer.validated_data['time_spent']
    
    # Fetch the article
    try:
        article = Articles.objects.get(id=article_id)
    except Articles.DoesNotExist:
        return Response({"error": f"Article with ID {article_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    # Compute the new popularity value
    
    # Calculate the increment based on the weighted formula
    increment = time_spent
    
    # Update the Popularity entry
    popularity_entry, created = Popularity.objects.get_or_create(article_id=article)
    popularity_entry.value += increment
    popularity_entry.save()

    # Update Personalization for users
    # Fetch all Personalization entries related to the article's subcategory
    subcategory = article.subcategory_id
    user_personalizations = Personalization.objects.get(user_id=user, subcategory_id=subcategory)

    # Example logic: Increment personalization value based on increment
    user_personalizations.value += int(increment * 2)  # Adjust the multiplier as needed
    user_personalizations.save()
    
    Articlesession.objects.create(
        article_id=article,
        time_spent=time_spent,
        timestamp = timezone.now(),
        user_id=user
    )

    serialized_article = ArticlesSerializer(article).data
    return Response(
        {
            "message": "Article popularity updated successfully.",
            "article": serialized_article
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_article_by_id(request):
    # Retrieve the user by username, return 404 if not found
    article = Articles.objects.get(id=request.data.get("article_id"))

    # Serialize the user data
    serialized_article = serializers.ArticlesSerializer(article)
    
    # Return the user data
    return Response(serialized_article.data, status=status.HTTP_200_OK)