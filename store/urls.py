# store/urls.py
from django.urls import path
from .views import login_view, dashboard_view,add_product_view,show_products,paiement_view,update_product,delete_product
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('add_product/', add_product_view, name='add_product'),
    path('products/', show_products, name='show_products'),
    path('paiement/',paiement_view, name='paiement'),
    path('produits/update/<int:product_id>/', update_product, name='update_product'),
    path('produits/delete/<int:product_id>/', delete_product, name='delete_product'),
    



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
