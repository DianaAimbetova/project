from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import JsonResponse

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request, cart=None):
    if cart == None:
        cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_update(request):
    cart = Cart(request)
    product_id = request.POST.get('id')
    action = request.POST.get('action')
    quantity = int(request.POST.get('quantity'))
    clicks = int(request.POST.get('clicks'))
    if product_id and action and quantity:
        try:
           product = get_object_or_404(Product, id=product_id)
           if action == 'plus':
               quantity = quantity + clicks
           else:
               quantity = quantity - clicks
           cart.add(product=product, quantity=quantity, override_quantity=True)
           return JsonResponse({'status': 'ok'})
        except Product.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})