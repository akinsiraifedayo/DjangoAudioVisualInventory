# Generated by Django 4.2.5 on 2024-01-05 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanedproduct',
            name='status',
            field=models.CharField(choices=[('IN_HOUSE', 'In House'), ('DEFECTIVE', 'Defective'), ('MISSING', 'Missing'), ('OKAY_RETURNED', 'Okay & Returned')], default='IN_HOUSE', max_length=255),
        ),
    ]
