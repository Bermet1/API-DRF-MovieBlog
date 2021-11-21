from rest_framework import fields, serializers
from .models import Category, Movie, Rating, Review, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)



class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")



class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data



class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление Отзывов к фильму"""

    class Meta:
        model = Review
        fields = "__all__"




class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы к фильму"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("text", 'name', 'children')



class ActorListSerializer(serializers.ModelSerializer):
    """Вывод списка актеров и режиссеров"""
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')



class ActorDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр актеров и режиссеров"""
    class Meta:
        model = Actor
        fields = '__all__'



class MovieDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр фильмов"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True) 
    actors = ActorListSerializer(read_only=True, many=True) 
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True) 
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)



class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга"""
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validate_data):
        rating = Rating.objects.update_or_create(
            ip=validate_data.get('ip', None),
            movie=validate_data.get('movie', None),
            defaults={"star":validate_data.get("star")}
        )

        return rating
