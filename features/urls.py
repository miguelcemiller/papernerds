from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingView, name='landing'),
    path('home', views.homeView, name='home'),

    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('results', views.resultsView, name='results'),
    path('paper/<str:pk>', views.paperView, name="paper"),

   
]