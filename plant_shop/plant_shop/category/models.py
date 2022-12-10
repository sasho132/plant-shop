from django.db import models
from django.urls import reverse


class Category(models.Model):
    CATEGORY_NAME_MAX_LEN = 30

    name = models.CharField(
        max_length=CATEGORY_NAME_MAX_LEN,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    image = models.ImageField(
        upload_to='categories/',
        null=False,
        blank=True,
    )

    def get_url(self):
        return reverse('products-by-category', args=[self.slug])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
