from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from plant_shop.category.models import Category

UserModel = get_user_model()


class Product(models.Model):
    PRODUCT_NAME_MAX_LEN = 50
    PRODUCT_NAME_MIN_LEN = 3

    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LEN,
    )

    image = models.ImageField(
        upload_to='products/',
        null=False,
        blank=False,
    )

    description = models.TextField(
        validators=(
            MinLengthValidator(10),
        ),
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    price = models.FloatField(
        validators=(
            MinValueValidator(0),
        )
    )

    on_sale_price = models.FloatField(
        null=True,
        blank=True,
        validators=(
            MinValueValidator(0),
        )
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    stock = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    created_by = models.ForeignKey(
        UserModel,
        related_name='plant_creator',
        on_delete=models.RESTRICT,
    )

    product_type = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    in_stock = models.BooleanField(
        default=True,
    )

    on_sale = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse('product-details', args=[self.category.slug, self.slug])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.pk}-{self.name}')

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
