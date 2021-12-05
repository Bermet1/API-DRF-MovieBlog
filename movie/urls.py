from django.urls import path
from . import views
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('movie/', views.MovieViewSet.as_view({'get':'list'})),
    path('movie/<int:pk>/', views.MovieViewSet.as_view({'get':'retrieve'})),
    path('review/', views.ReviewCreateViewSet.as_view({'post':'create'})),
    path('rating/', views.AddStarRatingViewSet.as_view({'post':'create'})),
    path('actors/', views.ActorViewSet.as_view({'get': 'list'})),
    path('actors/<int:pk>/', views.ActorViewSet.as_view({'get': 'retrieve'})),

    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
])


# urlpatterns = [
#     path('movie/', views.MovieListView.as_view()),
#     path('movie/<int:pk>/', views.MovieDetailView.as_view()),
#     path('review/', views.ReviewCreateView.as_view()),
#     path('review/<int:pk>/', views.ReviewDestroy.as_view()),
#     path('rating/', views.AddStarRatingView.as_view()),
#     path('actors/', views.ActorListView.as_view()),
#     path('actors/<int:pk>/', views.ActorDetailView.as_view()),
# ]