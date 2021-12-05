from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login

from .models import Movie, Actor, Review
from .serializers import ActorDetailSerializer, CreateRatingSerializer, MovieListSerializer, \
    MovieDetailSerializer, ReviewCreateSerializer, ActorListSerializer, \
    ActorDetailSerializer, UserSerializer, RegisterSerializer

from .permission import IsSuperUser
from .services import get_client_ip, MovieFilter, PaginationMovies
from movie import serializers



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Список фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies
    
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