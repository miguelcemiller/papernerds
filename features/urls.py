from django.urls import path
from django.shortcuts import redirect
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.landingView, name='landing'),
    path('home', views.homeView, name='home'),
    path('home/', RedirectView.as_view(pattern_name = 'home')),
    path('paper/<slug:slug>', views.paperView, name="paper"),
    path('paper/<slug:slug>/', RedirectView.as_view(pattern_name = 'paper')),

    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('results', views.resultsView, name='results'),

]