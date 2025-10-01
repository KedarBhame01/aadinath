from django.db import models

# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey("user.user",on_delete=models.CASCADE)
    product_id = models.ForeignKey("products.products",on_delete=models.CASCADE)
    def __str__(self):
        return self.name