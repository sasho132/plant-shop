import datetime


def total_cart_items_price(cart_items):
    total = 0
    for cart_item in cart_items:
        if cart_item.product.on_sale:
            total += (cart_item.product.on_sale_price * cart_item.quantity)
        else:
            total += (cart_item.product.price * cart_item.quantity)

    return total


def get_cart_items_quantity(card_items):
    return sum(item.quantity for item in card_items)


def get_current_date():
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr, mt, dt)
    current_date = d.strftime("%Y%m%d")
    return current_date
