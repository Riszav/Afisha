from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()
        # exclude = 'id'.split()

class MovieSerializer(serializers.ModelSerializer):
    # director = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = 'id title description duration director_name reviews average_rating'.split()
        depth = 1

    # def get_director(self, movie):
    #     return movie.director.name


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = 'id text movie stars'.split()

    def get_movie(self, review):
        return review.movie.title
