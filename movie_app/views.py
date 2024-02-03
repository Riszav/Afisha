from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director,Movie,Review
from .serializers import (DirectorSerializer, MovieSerializer, ReviewSerializer,
                          DirectorValidateSerializer, MovieValidateSerializer, ReviewValidateSerializer)
from rest_framework import status


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data=data)

    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data={'director_id': director.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        # print(request.data.get('bool'))
        # Step 1: Collect data of products from DB
        director = Director.objects.prefetch_related('movies').all()

        # Step 2: Reformat(Serialize) of products
        data = DirectorSerializer(director, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)

    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # name = serializer.validated_data.get('name')

        director = Director.objects.create(**serializer.validated_data)

        return Response(data={'director_id': director.id}, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(movie, context={'favorites': [1, 2]}).data
        return Response(data=data)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.category_id = serializer.validated_data.get('category_id')
        movie.tags.set(serializer.validated_data.get('tags'))
        movie.save()
        return Response(data={'movie_id': movie.id}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # Step 1: Collect data of products from DB
        movie = Movie.objects.select_related('director','category').prefetch_related('reviews','tags').all()

        # Step 2: Reformat(Serialize) of products
        data = MovieSerializer(movie, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)

    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')
        movie = Movie.objects.create(title=title, description=description, duration=duration,
                                     director_id=director_id, category_id=category_id)

        movie.tags.set(tags)
        movie.save()

        return Response(data={'movie_id': movie.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.stars = serializer.validated_data.get('stars')

        review.save()
        return Response(data={'movie_id': review.id}, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        # Step 1: Collect data of products from DB
        review = Review.objects.select_related('movie').all()

        # Step 2: Reformat(Serialize) of products
        data = ReviewSerializer(review, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # text = request.data.get('text')
        # movie_id = request.data.get('movie_id')
        # stars = request.data.get('stars')

        review = Review.objects.create(**serializer.validated_data)

        return Response(data={'review_id': review.id}, status=status.HTTP_201_CREATED)