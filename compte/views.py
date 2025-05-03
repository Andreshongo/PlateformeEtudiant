from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import InscriptionForm
from django.contrib import messages
from .models import Etudiant
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            etudiant = form.save(commit=False)
            etudiant.user = user
            etudiant.save()
            messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('connexion')  # ou une autre page après inscription
    else:
        form = InscriptionForm()
    return render(request, 'compte/inscription.html', {'form': form})

from .forms import ConnexionForm
from django.contrib.auth import authenticate, login
def connexion_view(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            user = form.user  # Utilise l'attribut `user` de `ConnexionForm`
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('tableau_de_bord')  # À adapter si tu veux une autre page
    else:
        form = ConnexionForm()
    return render(request, 'compte/connexion.html', {'form': form})


