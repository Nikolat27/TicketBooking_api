from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("register", views.UserRegisterView.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("logout", views.UserLogoutView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
]
