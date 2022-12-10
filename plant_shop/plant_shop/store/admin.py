from django.contrib import admin
from django.utils.safestring import mark_safe
from plant_shop.store.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type','price', 'in_stock','created', 'updated']
    list_filter = ['in_stock', 'category']
    list_editable = ['price', 'in_stock']
    readonly_fields = ['product_image']

    @staticmethod
    def product_image(obj):
        return mark_safe('<img src="{url}" width="{width}"/>'.format(
            url=obj.image.url,
            width=200,
        )
        )
