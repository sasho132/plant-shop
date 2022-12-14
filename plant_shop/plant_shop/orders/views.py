import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from plant_shop.cart.models import CartItem, Cart
from plant_shop.cart.views import _cart_id
from plant_shop.orders.forms import OrderForm
from plant_shop.orders.models import Order, Payment, OrderProduct
from plant_shop.store.models import Product
from plant_shop.utils.utils import total_cart_items_price, get_cart_items_quantity, get_current_date


@login_required
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart = Cart.objects.filter(cart_id=_cart_id(request)).get()
    cart_items = CartItem.objects.filter(user=current_user, cart=cart)
    cart_count = cart_items.count()
    if cart_count == 0:
        return redirect('store')

    total += total_cart_items_price(cart_items)
    quantity += get_cart_items_quantity(cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.zip_code = form.cleaned_data['zip_code']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            current_date = get_current_date()
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.filter(user=current_user, is_ordered=False, order_number=order_number).get()

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
            }

            return render(request, 'orders/payments.html', context)
    else:
        return redirect('cart:checkout')


@login_required
def payments_view(request):
    body = json.loads(request.body)
    order = Order.objects.filter(user=request.user, is_ordered=False, order_number=body['orderID']).get()

    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        status=body['status'],
        amount_paid=order.order_total,
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        if product.stock <= 0:
            product.in_stock = False
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)


def order_complete_view(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.filter(order_number=order_number, is_ordered=True).get()
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        payment = Payment.objects.filter(payment_id=transID).get()

        context = {
            'order': order,
            'order_products': ordered_products,
            'transID': payment.payment_id,
            'payment': order.payment,
        }

        return render(request, 'orders/order-complete.html', context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home-page')
