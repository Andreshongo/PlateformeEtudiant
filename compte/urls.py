from django.urls import path
from . import views
from .views import connexion_view

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', connexion_view, name='connexion'),
]


