from django.db import models

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey("user.user",on_delete=models.CASCADE)
    product = models.ForeignKey("products.products",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name