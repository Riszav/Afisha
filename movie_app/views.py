from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director,Movie,Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from rest_framework import status


@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializer(director).data
    return Response(data=data)


@api_view(['GET'])
def director_list_api_view(request):
    # Step 1: Collect data of products from DB
    director = Director.objects.prefetch_related('movies').all()

    # Step 2: Reformat(Serialize) of products
    data = DirectorSerializer(director, many=True).data

    # Step 3: Return data as JSON
    return Response(data=data)


@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = MovieSerializer(movie, context={'favorites': [1, 2]}).data
    return Response(data=data)

@api_view(['GET'])
def movie_list_api_view(request):
    # Step 1: Collect data of products from DB
    movie = Movie.objects.select_related('director').prefetch_related('reviews').all()

    # Step 2: Reformat(Serialize) of products
    data = MovieSerializer(movie, many=True).data

    # Step 3: Return data as JSON
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Review not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    # Step 1: Collect data of products from DB
    review = Review.objects.select_related('movie').all()

    # Step 2: Reformat(Serialize) of products
    data = ReviewSerializer(review, many=True).data

    # Step 3: Return data as JSON
    return Response(data=data)