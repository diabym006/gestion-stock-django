from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from .models import Produit, Mouvement
from .forms import ProduitForm, MouvementForm


# =========================
# PRODUITS
# =========================

from django.db.models import Q

@login_required
def liste_produits(request):
    query = request.GET.get('q', '')

    produits = Produit.objects.all()

    if query:
        produits = produits.filter(
            Q(nom__icontains=query) |
            Q(categorie__nom__icontains=query)
        )

    return render(request, 'stock/liste_produits.html', {
        'produits': produits,
        'query': query
    })



@login_required
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm()

    return render(request, 'stock/ajouter_produit.html', {
        'form': form
    })


@login_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'stock/modifier_produit.html', {
        'form': form
    })


@login_required
def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)

    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')

    return render(request, 'stock/supprimer_produit.html', {
        'produit': produit
    })


# =========================
# MOUVEMENTS
# =========================

@login_required
def ajouter_mouvement(request):
    if request.method == 'POST':
        form = MouvementForm(request.POST)
        if form.is_valid():
            mouvement = form.save(commit=False)
            produit = mouvement.produit

            if mouvement.type == 'SORTIE':
                if mouvement.quantite > produit.quantite:
                    messages.error(request, "Stock insuffisant ❌")
                    return redirect('ajouter_mouvement')
                produit.quantite -= mouvement.quantite
            else:
                produit.quantite += mouvement.quantite

            produit.save()
            mouvement.save()

            messages.success(request, "Mouvement enregistré ✅")
            return redirect('liste_produits')
    else:
        form = MouvementForm()

    return render(request, 'stock/ajouter_mouvement.html', {
        'form': form
    })


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    total_produits = Produit.objects.count()
    stock_total = Produit.objects.aggregate(total=Sum('quantite'))['total'] or 0

    produits_faible = Produit.objects.filter(quantite__lte=5)
    derniers_mouvements = Mouvement.objects.order_by('-date')[:5]

    produits = Produit.objects.all()
    noms = list(produits.values_list('nom', flat=True))
    quantites = list(produits.values_list('quantite', flat=True))

    context = {
        'total_produits': total_produits,
        'stock_total': stock_total,
        'produits_faible': produits_faible,
        'derniers_mouvements': derniers_mouvements,
        'noms': noms,
        'quantites': quantites,
    }

    return render(request, 'stock/dashboard.html', context)
