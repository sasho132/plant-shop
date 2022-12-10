from django.db import models
from django.contrib.auth import get_user_model
from plant_shop.store.models import Product

UserModel = get_user_model()


class Cart(models.Model):
    cart_id = models.CharField(max_length=50, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        if self.product.on_sale:
            return f"{self.product.on_sale_price * self.quantity:.2f}"
        return f"{self.product.price * self.quantity:.2f}"

    def __unicode__(self):
        return self.product
