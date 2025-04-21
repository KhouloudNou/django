from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProductForm
from django.contrib import messages
from .models import Product, Sale, Client,Paiement
from django.contrib import messages
import json  
from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth
from django.contrib import messages
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def dashboard_view(request):
    
    nb_produits = Product.objects.count()
    nb_clients = Client.objects.count()
    total_chiffre_affaire = Sale.objects.aggregate(total=Sum('chiffre_affaire'))['total'] or 0

   
    paiements_statut = (
        Paiement.objects
        .values('statut')
        .annotate(count=Count('id'))
    )
    labels_paiements = [item['statut'].capitalize() for item in paiements_statut]
    data_paiements = [item['count'] for item in paiements_statut]

    
    ventes_par_annee = (
        Sale.objects
        .values('annee')
        .annotate(total=Sum('chiffre_affaire'))
        .order_by('annee')
    )
    labels_annees = [str(item['annee']) for item in ventes_par_annee]
    data_chiffres = [float(item['total']) for item in ventes_par_annee]

    
    paiements_par_produit = (
        Paiement.objects
        .filter(statut='payé')
        .values('produit__name')
        .annotate(total_montant=Sum('montant'))
        .order_by('-total_montant')[:5]  # Top 5 produits
    )
    labels_produits = [item['produit__name'] for item in paiements_par_produit]
    data_produits = [float(item['total_montant']) for item in paiements_par_produit]

    context = {
        'nb_produits': nb_produits,
        'nb_clients': nb_clients,
        'total_chiffre_affaire': float(total_chiffre_affaire),
        'labels_paiements': json.dumps(labels_paiements),
        'data_paiements': json.dumps(data_paiements),
        'labels_annees': json.dumps(labels_annees),
        'data_chiffres': json.dumps(data_chiffres),
        'labels_produits': json.dumps(labels_produits),
        'data_produits': json.dumps(data_produits),
    }

    return render(request, 'dashboard.html', context)


def add_product_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        if name and description and price and image:
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image
            )
            messages.success(request, 'Produit ajouté avec succès !')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

    return render(request, 'add_product.html')


def show_products(request):
    search_query = request.GET.get('search', '')  
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)  
    else:
        products = Product.objects.all()  
    return render(request, 'show_products.html', {'products': products})




def paiement_view(request):
    paiements = Paiement.objects.all()  
    return render(request, 'paiement.html', {'paiements': paiements})



def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit mis à jour avec succès ✅')  # ✅ Message envoyé
            return redirect('show_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Le produit a été supprimé avec succès.")
    return redirect('show_products')


