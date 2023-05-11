from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('fantasy-league/', views.fantasy_league, name='fantasy-league'),
    path('live/', views.live, name='live'),
    path('statistics-main/', views.statistics_main, name='statistics-main'),
    path('statistics-rankings/', views.statistics_rankings, name='statistics-rankings'),
    path('statistics-by-time/', views.statistics_by_time, name='statistics-by-time'),
    path('statistics-jumper/', views.statistics_jumper, name='statistics-jumper'),
    path('blog/', views.blog, name='blog'),
]
