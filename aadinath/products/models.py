from django.db import models

class Products(models.Model):
    BOOLEAN_CHOICES = [
        ('true', 'True'),
        ('false', 'False'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    categoryId = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    originalPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    images = models.JSONField(default=list, blank=True, null=True)  # List of image URLs or file paths

    rating = models.FloatField()
    reviews = models.PositiveIntegerField()
    isNew = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    isSale = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    description = models.TextField()
    shortDescription = models.TextField(null=True, blank=True)
    isCustomizable = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    customizationOptions = models.JSONField(default=list, blank=True, null=True)  # List of options

    showOnHome = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    showOnProducts = models.CharField(default=False,max_length=10, choices=BOOLEAN_CHOICES)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
