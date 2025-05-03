from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='etudiant_magasin')
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.prenom} {self.nom}".title()


class Boutique(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    etudiant = models.OneToOneField(Etudiant, on_delete=models.CASCADE, related_name='boutique', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} - {self.etudiant.user.username if self.etudiant and self.etudiant.user else 'Aucun'}"


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)

    def __str__(self):
        return self.nom


# models.py
class Message(models.Model):
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)
    fichier_joint = models.FileField(upload_to='fichiers_messages/', blank=True, null=True)  # Ajout

    def __str__(self):
        return f"De {self.expediteur.username} à {self.destinataire.username}"
