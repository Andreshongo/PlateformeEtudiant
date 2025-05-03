from django.contrib import admin
from .models import Etudiant, Boutique, Produit, Message


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'telephone', 'get_username')
    search_fields = ('nom', 'postnom', 'prenom', 'user__username', 'telephone')
    list_filter = ('user__is_active',)

    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.postnom} {obj.nom}".title()
    nom_complet.short_description = "Nom complet"

    def get_username(self, obj):
        return obj.user.username if obj.user else "Aucun"
    get_username.short_description = "Nom d'utilisateur"


@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'etudiant_username', 'description')
    search_fields = ('nom', 'etudiant__user__username')

    def etudiant_username(self, obj):
        return obj.etudiant.user.username if obj.etudiant and obj.etudiant.user else "Aucun"
    etudiant_username.short_description = "Étudiant"


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'etudiant', 'boutique')
    search_fields = ('nom', 'etudiant__user__username', 'boutique__nom')
    list_filter = ('boutique',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'date_envoi', 'lu')
    search_fields = ('expediteur__username', 'destinataire__username', 'contenu')
    list_filter = ('lu', 'date_envoi')
