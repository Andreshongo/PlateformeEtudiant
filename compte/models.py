from django.db import models
from django.contrib.auth.models import User

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='etudiant_compte')
    matricule = models.CharField(max_length=20, unique=True)
    telephone = models.CharField(max_length=15)
    universite = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

