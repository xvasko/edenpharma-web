# Generated by Django 2.2.3 on 2019-07-29 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='slug',
            field=models.SlugField(default='default'),
        ),
    ]
