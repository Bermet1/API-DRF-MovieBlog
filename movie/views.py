from django.db import models
from django.db.models import query
from django.db.models.fields import DurationField
from rest_framework import serializers, generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import ActorDetailSerializer, CreateRatingSerializer, MovieListSerializer, \
    MovieDetailSerializer, ReviewCreateSerializer, ActorListSerializer, \
    ActorDetailSerializer

from .services import get_client_ip, MovieFilter

class MovieListView(generics.ListAPIView):
    """Список фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
           rating_user=models.Count("ratings", 
                                    filter=models.Q(ratings__ip=get_client_ip(self.request))) 
        ).annotate(
            moddle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Детайльный просмотр фильмов"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer



class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзывов"""
    serializer_class = ReviewCreateSerializer
       


class AddStarRatingView(generics.CreateAPIView):
    """Добавить рейтинг к фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
           


class ActorListView(generics.ListAPIView):
    """Вывод списка актеров и режиссеров """
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


# class ActorListView(APIView):
#     """Вывод списка актеров и режиссеров """

#     def get(self, request):
#         actors = Actor.objects.all()
#         serializer = ActorListSerializer(actors, many=True)
#         return Response(serializer.data)


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод актеров и режиссеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer