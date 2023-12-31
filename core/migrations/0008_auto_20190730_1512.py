# Generated by Django 2.2.3 on 2019-07-30 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='customer',
            name='street',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='customer',
            name='zip',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
