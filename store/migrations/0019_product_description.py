# Generated by Django 4.2.7 on 2024-02-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_feature_remove_product_features_product_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=1500),
        ),
    ]
