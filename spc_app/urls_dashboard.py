from django.urls import path
from . import views_dashboard

urlpatterns = [
    path('data/metrics/', views_dashboard.dashboard_metrics, name='dashboard_metrics'),
    path('data/leaderboard/', views_dashboard.dashboard_leaderboard, name='dashboard_leaderboard'),
]
