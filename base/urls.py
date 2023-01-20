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
    path('userinfo/', views.info, name="userinfo"),
    path("userinfo/<int:id>", views.info, name="userinfo_pk"),
    path('get_all_images/', views.getImages),
    path('upload_image/',views.APIViews.as_view())

]
