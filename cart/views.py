from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)] += int(request.POST.get('quantity', 1))
    else:
        cart[str(pk)] = int(request.POST.get('quantity', 1))

    request.session['cart'] = cart
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('product_list')


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
    request.session['cart'] = cart
    return redirect('cart_detail')