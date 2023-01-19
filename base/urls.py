from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("register/", views.register , name="register"),
    path("events/", views.events),
    path('userinfo/', views.info, name="userinfo"),
    path("userinfo/<int:id>", views.info, name="userinfo_pk")

]
