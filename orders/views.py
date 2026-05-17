from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart_detail')

    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        address = request.POST.get('address')
        email = request.POST.get('email')

        order = Order.objects.create(
            user=request.user,
            address=address,
            email=email,
            paid=True
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        request.session['cart'] = {}
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success')

    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})


def order_success(request):
    return render(request, 'orders/success.html')