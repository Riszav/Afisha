from rest_framework import serializers
from rest_framework.response import Response
from .models import Director, Movie, Review, Category, Tag
from rest_framework.exceptions import ValidationError


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
        fields = 'id title description duration director_name reviews average_rating category tags'.split()
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


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(required=False)
    duration = serializers.FloatField()
    director_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director not found!')
        return director_id

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Director.DoesNotExist:
            raise ValidationError('Director not found!')
        return category_id


    def validate_tags(self, tags):
        data = Tag.objects.all()
        data_id = []
        errors = {}
        er_exist = False
        tag_id = 0
        for i in data:
            data_id.append(i.id)
        for i in tags:
            if i not in data_id:
                errors[tag_id] = [f"Element with id '{i}' doesn`t exist in data base."]
                er_exist = True
            tag_id += 1
        if er_exist:
            raise serializers.ValidationError(errors)
        return tags


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    movie_id = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, max_value=5)


    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError('Movie not found!')
        return movie_id
