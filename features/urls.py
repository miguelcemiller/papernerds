from django.urls import path
from django.shortcuts import redirect
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('home', views.home_view, name='home'),
    path('home/', RedirectView.as_view(pattern_name = 'home')),
    path('paper/<slug:slug>', views.paper_view, name="paper"),
    path('paper/<slug:slug>/', RedirectView.as_view(pattern_name = 'paper')),
    #path('portal/<slug:slug>', views.portal_view, name="portal"),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('results', views.results_view, name='results'),

]