import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from plant_shop.cart.models import Cart, CartItem
from plant_shop.store.models import Product
from django.http import JsonResponse
from plant_shop.utils.utils import total_cart_items_price, get_cart_items_quantity


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def get_cart_items(cart):
    cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('product_id')
    return cart_items


@login_required
def cart_view(request, total=0, quantity=0):
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).get()
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    cart_items = get_cart_items(cart=cart)
    total += total_cart_items_price(cart_items)
    quantity += get_cart_items_quantity(cart_items)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }

    return render(request, 'store/cart.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    user = request.user

    product = Product.objects.filter(id=productId).get()

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    if action == 'add':
        try:
            cart_item = CartItem.objects.filter(product=product, cart=cart).get()
            cart_item.quantity += 1
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
        cart_item.user = user
        cart_item.save()

    elif action == 'remove':
        cart_item = CartItem.objects.filter(product=product, cart=cart).get()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    cart.save()
    return JsonResponse('Item was added', safe=False)


@login_required
def checkout_view(request, total=0, quantity=0):
    cart = Cart.objects.filter(cart_id=_cart_id(request)).get()

    cart_items = get_cart_items(cart=cart)
    total += total_cart_items_price(cart_items)
    quantity += get_cart_items_quantity(cart_items)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)
