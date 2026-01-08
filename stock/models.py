from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.FloatField()
    quantite = models.IntegerField()
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name="produits"
    )

    def __str__(self):
        return self.nom
class Mouvement(models.Model):
    TYPE_CHOICES = (
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    )

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantite = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.produit.nom} ({self.quantite})"
