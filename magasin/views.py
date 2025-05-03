from django.contrib.auth import authenticate, logout
from .forms import BoutiqueForm
from .models import Boutique
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produit, Etudiant, Message
from django.shortcuts import get_object_or_404
from .forms import ProduitForm

# Accueil - Tous les produits des boutiques
def accueil_view(request):
    produits = Produit.objects.all()
    return render(request, 'magasin/accueil.html', {'produits': produits})

# Inscription (simple affichage du template)
def inscription_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer un profil Etudiant automatiquement
            Etudiant.objects.create(
                user=user,
                nom=user.last_name or 'Nom',
                postnom='Postnom',
                prenom=user.first_name or 'Prénom'
            )

            login(request, user)  # Connexion automatique après inscription
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'magasin/inscription.html', {'form': form})

# Connexion
def connexion_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tableau_de_bord')
        else:
            return render(request, 'compte/connexion.html', {'error': 'Identifiants incorrects'})
    return render(request, 'compte/connexion.html')

# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('connexion')

# Tableau de bord étudiant
@login_required(login_url='connexion')
def tableau_de_bord(request):
    return render(request, 'magasin/tableau_de_bord.html')


# Création de la boutique
@login_required(login_url='connexion')
def creer_boutique(request):
    user = request.user
    # Vérifier si un profil Etudiant existe, sinon le créer
    etudiant, created = Etudiant.objects.get_or_create(user=user, defaults={
        'nom': user.last_name or 'Nom',
        'postnom': 'Postnom',
        'prenom': user.first_name or 'Prénom'
    })

    if request.method == 'POST':
        form = BoutiqueForm(request.POST)
        if form.is_valid():
            boutique = form.save(commit=False)
            boutique.etudiant = etudiant
            boutique.save()
            return redirect('ajouter_produit')
    else:
        form = BoutiqueForm()
    return render(request, 'magasin/creer_boutique.html', {'form': form})

# Ajout de produit à une boutique
@login_required(login_url='connexion')
def ajouter_produit(request):
    user = request.user
    etudiant = Etudiant.objects.get(user=user)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.etudiant = etudiant
            produit.boutique = etudiant.boutique
            produit.save()
            return redirect('tableau_de_bord')  # Ou la vue où tu rediriges après ajout
    else:
        form = ProduitForm()
    return render(request, 'magasin/ajouter_produit.html', {'form': form})

# Commander un produit
def commander_view(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    return render(request, 'commande/commander.html', {'produit': produit})
@login_required(login_url='connexion')
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if produit.etudiant.user != request.user:
        return redirect('mes_produits')

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('mes_produits')
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'magasin/modifier_produit.html', {'form': form})

@login_required(login_url='connexion')
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if produit.etudiant.user == request.user:
        produit.delete()
    return redirect('mes_produits')

# Accueil avec toutes les boutiques et leurs produits
def accueil(request):
    boutiques = Boutique.objects.prefetch_related('produits').all()
    return render(request, 'magasin/accueil.html', {'boutiques': boutiques})

@login_required(login_url='connexion')
def mes_produits_view(request):
    etudiant = Etudiant.objects.get(user=request.user)
    produits = Produit.objects.filter(etudiant=etudiant)
    return render(request, 'magasin/mes_produits.html', {'produits': produits})
# views.py
@login_required
def messagerie_view(request):
    user = request.user

    # Récupérer l'étudiant connecté
    try:
        etudiant_connecte = user.etudiant_magasin
    except Etudiant.DoesNotExist:
        etudiant_connecte = None

    # Liste des autres étudiants
    etudiants = Etudiant.objects.exclude(user=user)

    if request.method == 'POST':
        destinataire_id = request.POST.get('destinataire_id')
        contenu = request.POST.get('contenu')
        fichier_joint = request.FILES.get('fichier_joint')

        destinataire_user = User.objects.get(id=destinataire_id)

        Message.objects.create(
            expediteur=user,
            destinataire=destinataire_user,
            contenu=contenu,
            fichier_joint=fichier_joint
        )
        return redirect('messagerie')

    # Récupérer les messages reçus et envoyés
    messages_recus = Message.objects.filter(destinataire=user)
    messages_envoyes = Message.objects.filter(expediteur=user)

    return render(request, 'magasin/messagerie.html', {
        'etudiants': etudiants,
        'messages_recus': messages_recus,
        'messages_envoyes': messages_envoyes
    })