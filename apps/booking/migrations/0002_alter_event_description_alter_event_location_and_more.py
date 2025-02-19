# Generated by Django 4.2.5 on 2024-01-25 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=2047, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.CharField(blank=True, max_length=2047, null=True),
        ),
    ]
