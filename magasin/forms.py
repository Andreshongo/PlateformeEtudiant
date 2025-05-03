from .models import Boutique
from django import forms
from .models import Message
from .models import Produit
class BoutiqueForm(forms.ModelForm):
    class Meta:
        model = Boutique
        fields = ['nom', 'description']
        labels = {
            'nom': 'Nom de la boutique',
            'description': 'Description de la boutique',
        }
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['destinataire', 'contenu']
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'image']




