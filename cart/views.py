# cart/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem
from decimal import Decimal

# Add product to cart

@require_POST
def cart_add(request, product_id):
    cart = request.session.get('cart', {})  # Retrieve the cart from session or initialize a new one
    product = get_object_or_404(Product, pk=product_id)  # Ensure the product exists

    if str(product_id) in cart:
        if 'quantity' in cart[str(product_id)]:
            cart[str(product_id)]['quantity'] += 1  # Increment the quantity if it exists
        else:
            cart[str(product_id)]['quantity'] = 1  # Initialize quantity if it's missing
    else:
        # Initialize the cart item with quantity 1 and store the price
        cart[str(product_id)] = {
            'quantity': 1,
            'price': str(product.price)  # Store price as string to avoid JSON serialization issues
        }

    request.session['cart'] = cart  # Update the cart in the session

    return redirect('cart_view')  # Redirect to cart view after adding product
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Product removed from cart.")
    return redirect('cart_view')

# View cart details
def cart_view(request):
    cart_items = request.session.get('cart', {})
    cart_details = []
    total_price = Decimal('0.00')  # Initialize total price as Decimal

    for product_id, item in cart_items.items():
        product = get_object_or_404(Product, pk=product_id)
        item_price = Decimal(item['price'])  # Ensure price is Decimal
        item_details = {
            'product_id': product.id,
            'name': product.name,
            'image_url': product.image.url if product.image else '/default_image.jpg',
            'description': product.description,
            'price': item_price,
            'quantity': item['quantity'],
            'total_price': item_price * item['quantity']
        }
        cart_details.append(item_details)
        total_price += item_price * item['quantity']

    return render(request, 'cart/cart_view.html', {
        'cart_items': cart_details,
        'total_price': total_price
    })

# Update cart quantity
@require_POST
def cart_update(request, product_id):
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] = quantity
        request.session['cart'] = cart
    return redirect('cart_view')
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        # Create order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Create order items
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear cart
        request.session['cart'] = {}

        # Redirect to order confirmation
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'cart/checkout.html', {'total_price': total_price})

# Order confirmation view
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_confirmation.html', {'order': order})
# Order history view
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cart/order_history.html', {'orders': orders})

# Order detail view
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_detail.html', {'order': order})

@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    total_price = Decimal('0.00')
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = int(item['quantity'])
        price = Decimal(item['price'])
        total_price += price * quantity

    # Create the Order
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Add OrderItems to the Order
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = int(item['quantity'])
        price = Decimal(item['price'])
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

    # Clear the cart
    request.session['cart'] = {}

    # Redirect to order confirmation with the order_id
    return redirect('order_confirmation', order_id=order.id)
def home_view(request):
    return render(request, 'home.html')

@require_POST
def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] = quantity
        request.session['cart'] = cart
    return redirect('cart_view')
