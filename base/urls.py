from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('', views.index),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
   path("register/", views.register , name="register"),
    path("events/", views.events),
    path('get_all_images/', views.getImages),
    path('upload_image/',views.APIViews.as_view()),
    path('addinfo/', views.PrivetInformationView.as_view()),
    path("addinfo/<int:id>", views.PrivetInformationView.as_view(), name="userinfo_id"),

]  
