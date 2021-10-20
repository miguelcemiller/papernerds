from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingView, name='landing'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
]