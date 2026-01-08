from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard

from .views import (
    liste_produits,
    ajouter_produit,
    modifier_produit,
    supprimer_produit,
    ajouter_mouvement,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),

    # Produits
    path('produits/', liste_produits, name='liste_produits'),
    path('produits/ajouter/', ajouter_produit, name='ajouter_produit'),
    path('produits/modifier/<int:id>/', modifier_produit, name='modifier_produit'),
    path('produits/supprimer/<int:id>/', supprimer_produit, name='supprimer_produit'),

    # Mouvements de stock
    path('mouvements/ajouter/', ajouter_mouvement, name='ajouter_mouvement'),

    # Authentification
    path('login/', auth_views.LoginView.as_view(
        template_name='stock/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

