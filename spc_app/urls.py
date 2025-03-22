from django.urls import path
from . import views

urlpatterns = [
    path('defense/submit/', views.submit_defense, name='submit_defense'),
    path('attack/submit/', views.submit_attack, name='submit_attack'),
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spc/', include('spc_app.urls')),
    path('dashboard/', include('spc_app.urls_dashboard')),  # New dashboard endpoints
]
