
from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.RegistrationCreateApiView.as_view()),
    path('authorization/', views.AuthorizationCreateApiView.as_view()),
    path('confirm/', views.ConfirmCreateApiView.as_view())
]