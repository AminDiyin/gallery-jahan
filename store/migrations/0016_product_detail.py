# Generated by Django 4.2.7 on 2024-01-25 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_product_info_product_product_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.CharField(default=True, max_length=50),
        ),
    ]
