from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET
from django.utils.translation import gettext as _
from django.contrib import messages

from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm


def cart_detail_view(request):
    cart = Cart(request)
    for item in cart:
        item['product_update_quantity_form'] = AddToCartProductForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
    })


@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        clean_deta = form.cleaned_data
        quantity = clean_deta['quantity']
        inplace = clean_deta['inplace']
        cart.add(product, quantity, replace_current_quantity=inplace)
    return redirect('cart:cart_detail')


@require_GET
def remove_from_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@require_POST
def clear_cart_view(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
        messages.success(request, _('All product successfully removed from your cart'))
    else:
        messages.warning(request, _('your cart is already empty'))
    return redirect('product_list')
