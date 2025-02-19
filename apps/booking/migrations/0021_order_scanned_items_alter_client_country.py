# Generated by Django 4.2.5 on 2024-04-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouses', '0012_alter_item_barcode_alter_transfer_status'),
        ('booking', '0020_remove_orderitem_product_orderitem_w_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='scanned_items',
            field=models.ManyToManyField(blank=True, related_name='order.scanned_items+', to='warehouses.item'),
        ),
        migrations.AlterField(
            model_name='client',
            name='country',
            field=models.CharField(default='Canada', max_length=255),
        ),
    ]
