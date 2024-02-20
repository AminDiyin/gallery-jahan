from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    category_name = models.CharField( max_length=50)
    slug = models.SlugField(unique=True , max_length=50 , allow_unicode=True)
    description = models.CharField(max_length=700, blank=True)
    cat_images = models.ImageField(upload_to='photos/categories/', blank=True)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=trending")
    meta_title = models.CharField(null=False, blank=True , max_length=150)
    meta_keywords = models.CharField(null=False, blank=True , max_length=150)
    meta_description = models.CharField(max_length=500, blank=True)
    created_at = models.TimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'دسته بندی'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_name = models.CharField( max_length=50)
    slug = models.CharField(unique=True, max_length=50)
    description = models.CharField( max_length=250, blank=True)
    product_image = models.ImageField(upload_to='photos/products/', blank=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'محصول'

    def __str__(self):
        return self.product_name
    