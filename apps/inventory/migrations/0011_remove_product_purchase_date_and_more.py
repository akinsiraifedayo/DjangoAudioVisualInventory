# Generated by Django 4.2.5 on 2024-03-30 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_product_rental_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='purchase_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='purchase_price',
        ),
    ]
