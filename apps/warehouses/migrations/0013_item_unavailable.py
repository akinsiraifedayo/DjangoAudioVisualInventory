# Generated by Django 4.2.5 on 2024-04-17 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouses', '0012_alter_item_barcode_alter_transfer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='unavailable',
            field=models.IntegerField(default=0),
        ),
    ]
