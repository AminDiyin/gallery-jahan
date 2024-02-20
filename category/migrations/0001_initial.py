# Generated by Django 4.2.7 on 2023-12-03 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('cat_images', models.ImageField(blank=True, upload_to='photos/categories/')),
            ],
        ),
    ]
