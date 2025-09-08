from django.db import models

class Products(models.Model):
    BOOLEAN_CHOICES = [
        ('True', 'true'),
        ('False', 'false'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    category_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    images = models.JSONField(default=list, blank=True, null=True)  # List of image URLs or file paths

    rating = models.FloatField()
    reviews = models.PositiveIntegerField()
    is_new = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    is_sale = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    is_customizable = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    customization_options = models.JSONField(default=list, blank=True, null=True)  # List of options

    show_on_home = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    show_on_products = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
