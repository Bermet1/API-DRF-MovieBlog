from rest_framework import fields, serializers

from .models import Category, Movie, Review

class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")



class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление Отзывов к фильму"""

    class Meta:
        model = Review
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы к фильму"""

    class Meta:
        model = Review
        fields = ("text", 'name', 'parent')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр фильмов"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True) 
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True) 
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True) 
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)

