# Generated by Django 5.2 on 2025-04-17 18:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_paiement_rename_client_sale_client_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiement',
            name='date',
        ),
        migrations.AddField(
            model_name='paiement',
            name='date_paiement',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='paiement',
            name='produit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='paiement',
            name='statut',
            field=models.CharField(choices=[('payé', 'Payé'), ('en_attente', 'En attente'), ('annulé', 'Annulé')], default='en_attente', max_length=20),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.client'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='montant',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
