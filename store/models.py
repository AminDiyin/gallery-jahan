from typing import Any
from django.db import models
from category.models import Category
from django.db.models.expressions import Combinable as Combinable
#from django.db.models.query import ValuesQuerySet
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
# Create your models here.


class Feature(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(unique=True , max_length=200)
    features = models.ManyToManyField(Feature)
    description = models.CharField(max_length=1500, blank=True)
    slug = models.SlugField(max_length=200, unique=True,allow_unicode=False)
    price = models.IntegerField()
    off_price = models.IntegerField(null=True, blank=True)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    trending = models.BooleanField(default=False, help_text="0=default, 1=trending")
    tag = models.CharField(null=True , max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(null=False, blank=True , max_length=150)
    meta_keywords = models.CharField(null=False, blank=True , max_length=150)
    meta_description = models.CharField(max_length=500, blank=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'محصولات '

    def __str__(self):
        return self.product_name
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('rating'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color',is_active=True)
    
    def weights(self):
        return super(VariationManager, self).filter(variation_category='weight',is_active=True)

variation_category_choice = (
    ('color','رنگ'),
    ('weight','مقدار'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(choices=variation_category_choice, max_length=100)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
    class Meta:
        verbose_name = 'variations'
        verbose_name_plural = 'آیتم متغیر محصول'

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(blank=True, max_length=100)
    review = models.CharField(blank=True, max_length=500)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.TimeField(auto_now_add=True)
    updated_date = models.TimeField(auto_now=True)

    def __str__(self):
        return self.subject
    class Meta:
        verbose_name = 'reviewrating'
        verbose_name_plural = 'بررسی نظرسنجی'
        


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products',  max_length=255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'گالری محصول'

