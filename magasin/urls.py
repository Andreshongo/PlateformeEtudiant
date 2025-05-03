from django.urls import path
from . import views
urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.tableau_de_bord, name='tableau_de_bord'),
    path('mes-produits/', views.mes_produits_view, name='mes_produits'),
    path('modifier-produit/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer-produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
    path('creer-boutique/', views.creer_boutique, name='creer_boutique'),
    path('ajouter-produit/', views.ajouter_produit, name='ajouter_produit'),
    path('messagerie/', views.messagerie_view, name='messagerie'),
    path('commander/<int:produit_id>/', views.commander_view, name='commander'),
]
