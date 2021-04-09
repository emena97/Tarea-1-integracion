from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bb/temporadas/<int:season_id>/', views.bb_seasons, name='bb_seasons'),
    path('bcs/temporadas/<int:season_id>/', views.bcs_seasons, name='bcs_seasons'),
    path('bb/temporadas/<int:season_id>/<str:episode_name>', views.bb_episodes, name='bb_episodes'),
    path('bcs/temporadas/<int:season_id>/<str:episode_name>', views.bcs_episodes, name='bcs_episodes'),
    path('search', views.search, name='search'),
    path('<str:character>', views.character, name='character'),

]

