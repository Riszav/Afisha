
from django.urls import path
from movie_app import views
from const import LIST_CREATE, DETAIL

urlpatterns = [
    path('directors/', views.DirectorListCreateAPIView.as_view()),
    path('directors/<int:id>/', views.DirecorDetailAPIView.as_view()),
    path('movies/', views.MovieListCreateAPIView.as_view()),
    path('movies/<int:id>/', views.MovieDetailAPIView.as_view()),
    path('reviews/', views.ReviewModelViewSet.as_view(LIST_CREATE)),     #{'get': 'list', 'post': 'create'}
    path('reviews/<int:id>/', views.ReviewModelViewSet.as_view(DETAIL)),     #{'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
]
