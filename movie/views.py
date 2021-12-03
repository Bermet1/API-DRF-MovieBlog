from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from .serializers import ActorDetailSerializer, CreateRatingSerializer, MovieListSerializer, \
    MovieDetailSerializer, ReviewCreateSerializer, ActorListSerializer, \
    ActorDetailSerializer

from .permission import IsSuperUser
from .services import get_client_ip, MovieFilter
from movie import serializers



class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Список фильмов"""
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

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer



class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзывов к фильму"""
    serializer_class = ReviewCreateSerializer



class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer
            

# class MovieListView(generics.ListAPIView):
#     """Список фильмов"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     def get_queryset(self):          
#         movies = Movie.objects.filter(draft=False).annotate(
#            rating_user=models.Count("ratings", 
#                                     filter=models.Q(ratings__ip=get_client_ip(self.request))) 
#         ).annotate(
#             moddle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         return movies


# class MovieDetailView(generics.RetrieveAPIView):
#     """Детайльный просмотр фильмов"""
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#     permission_classes = [permissions.IsAuthenticated]



# class ReviewDestroy(generics.DestroyAPIView):
#     """Удаление отзывов"""
#     queryset = Review.objects.all()
#     permissions_class = [permissions.IsAdminUser]


# class ReviewCreateView(generics.CreateAPIView):
#     """Добавление отзывов"""
#     serializer_class = ReviewCreateSerializer
#     permissions_class = [IsSuperUser]

       

# class AddStarRatingView(generics.CreateAPIView):
#     """Добавить рейтинг к фильму"""

#     serializer_class = CreateRatingSerializer

#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
           


#GenericAPIViews
# class ActorListView(generics.ListAPIView):
#     """Вывод списка актеров и режиссеров """
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer

#APIView
# class ActorListView(APIView):
#     """Вывод списка актеров и режиссеров """

#     def get(self, request):
#         actors = Actor.objects.all()
#         serializer = ActorListSerializer(actors, many=True)
#         return Response(serializer.data)


# class ActorDetailView(generics.RetrieveAPIView):
#     """Вывод актеров и режиссеров"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer