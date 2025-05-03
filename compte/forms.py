from django import forms
from django.contrib.auth.models import User
from .models import Etudiant
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

# Formulaire d'inscription
class InscriptionForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Etudiant
        fields = ['matricule', 'telephone', 'universite']

# Formulaire de connexion
class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    # Cette fonction est utilisée pour traiter la connexion dans la vue
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe invalide")
            else:
                self.user = user
        return self.cleaned_data

# Vue de connexion
def connexion_view(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('accueil')  # à adapter si tu veux une autre page
    else:
        form = ConnexionForm()
    return render(request, 'compte/connexion.html', {'form': form})
