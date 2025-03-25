# Generated by Django 5.1.6 on 2025-03-25 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omaha_places_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='price_level',
            field=models.CharField(blank=True, help_text='Price level of the restaurant', max_length=50, null=True, verbose_name='Price Level'),
        ),
        migrations.AlterField(
            model_name='place',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, help_text='Rating of the restaurant', max_digits=2, null=True, verbose_name='Rating'),
        ),
    ]
