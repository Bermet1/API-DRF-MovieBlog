from django.db.models import query
from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor
from .serializers import ActorDetailSerializer, CreateRatingSerializer, MovieListSerializer, \
    MovieDetailSerializer, ReviewCreateSerializer, ActorListSerializer, \
    ActorDetailSerializer

class MovieListView(APIView):
    """Список фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    """Детайльный просмотр фильмов"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Добавление комментриев"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавить рейтинг к фильму"""

    def get_client_ip(self, request):
        x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward_for:
            ip = x_forward_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


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