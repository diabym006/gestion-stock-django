from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'categorie', 'prix', 'quantite']
from .models import Mouvement

class MouvementForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = ['produit', 'type', 'quantite']
