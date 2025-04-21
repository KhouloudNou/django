from django.db import models
from django.utils import timezone


class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()

class Sale(models.Model):
    annee = models.IntegerField()
    chiffre_affaire = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Sale for {self.annee} - {self.chiffre_affaire} TND"


class Paiement(models.Model):
    STATUT_CHOICES = [
        ('payé', 'Payé'),
        ('en_attente', 'En attente'),
        ('annulé', 'Annulé'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"{self.client} - {self.montant} TND - {self.statut}"
    

