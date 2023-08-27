from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category ,Cart,Order,OrderItem,Profile,SubCategory,Wishlist
from django.http.response import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
import random
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.utils.crypto import get_random_string

# Create your views here.
def home(request):
    product = Product.objects.all()
    sneakers = Product.objects.filter(type="Sneakers")
    category = Category.objects.all()
    trending_products = Product.objects.filter(trending=True)
    category_men = 'Men'
    context = {
        'product': product,
        'category': category,
        'trending_products': trending_products,
        'category_men':category_men,
        'sneakers':sneakers,

    }
    return render(request, 'index.html', context)



def category_view(request, sub_category):
    subcategory = SubCategory.objects.get(name=sub_category)
    products = Product.objects.filter(sub_category_id=subcategory.id)
    return render(request, 'shop.html', {'products': products})

def category(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request, 'category.html',context)

def filter_products(request):
    if request.method == 'POST':
        amount = request.POST.get('max_price')
        products = Product.objects.filter(selling_price__lte=amount)
        return render(request, 'shop.html', {'products': products,'amount':amount})
    return render(request, 'shop.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def shop_with_category(request,category):
    cat = Category.objects.get(name=category)
    products = Product.objects.filter(category=cat)
    return render(request, 'shop.html', {'products': products})



def product_type(request,type):
    products = Product.objects,filter(type=type)
    return render(request, 'shop.html', {'products': products})

def product_view(request,cat_slug,sub_cat_slug,prod_slug):
    category = Category.objects.get(slug=cat_slug)
    sub_category = SubCategory.objects.get(slug=sub_cat_slug)
    category_men = Category.objects.get(name="Men")
    related_products = Product.objects.filter(sub_category=sub_category).exclude(slug=prod_slug)
    size_choices = Product.SIZE_CHOICES
    men_slug = category_men.slug
    products = Product.objects.get(slug=prod_slug,category=category)
    context = {'products':products,'men_slug':men_slug,'related_products' : related_products,'size_choices':size_choices}
    return render(request,'product_view.html',context)

def cart(request):
    if request.user.is_authenticated:
        cart_pro = Cart.objects.filter(user=request.user)
        context = {'cart_product':cart_pro}
        return render(request,'cart.html',context)
    else:
        messages.error(request,'Please login to your account!!')
        return redirect('home')

def wishlist(request):
    if request.user.is_authenticated:
        wish_pro = Wishlist.objects.filter(user=request.user)
        context = {'wish_product':wish_pro}
        return render(request,'wishlist.html',context)
    else:
        messages.error(request,'Please login to your account!!')
        return redirect('home')


def add_to_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':

                prod_id = request.POST.get('product_id')
                product = get_object_or_404(Product, id=prod_id)

                cart_item = Cart.objects.filter(user=request.user, product=product).first()
                if cart_item:
                    # Product already exists in the cart, update the quantity
                    cart_item.product_quantity += 1
                    cart_item.save()
                    return JsonResponse({'message': "Product already added."})
                else:
                    # Product does not exist in the cart, create a new cart item
                    cart_item = Cart.objects.create(user=request.user, product=product)
                    return JsonResponse({'message': "Product added successfully."})
        return JsonResponse({'message':'Invalid request'})

    else:
        return JsonResponse({'message':'Please login to your account!!'})


def orders_view(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders.html', {'orders': orders})
    else:
        messages.error(request,'Please login to your account!!')
        return redirect('home')

def update_quantity(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        prod_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        # Retrieve the cart product and update the quantity
        cart_product = Cart.objects.get(product_id=prod_id)
        cart_product.product_quantity = quantity
        cart_product.save()

        # Return a JSON response indicating success
        response = {'message': 'added'}
        return JsonResponse(response)
    else:
        # Return a JSON response indicating failure
        response = {'message': 'Invalid request'}
        return JsonResponse(response, status=400)

@require_POST
def remove_from_cart(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_item_id = request.POST.get('cart_item_id')
        try:
            cart_item = Cart.objects.get(id=cart_item_id)
            cart_item.delete()
            return JsonResponse({'message': 'Cart item removed successfully'})
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart item does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)



@login_required(login_url='login')
def update_cart_total(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = 0
    total_price = 0
    shipping_price= 0
    for item in cart_items:
        subtotal+=item.product.selling_price*item.product_quantity
        total_price+=item.product.selling_price*item.product_quantity

    if subtotal>=499:
        shipping_price = 0
    elif subtotal<0:
        shipping_price = 40

    total_price+=shipping_price

    data = {
        'subtotal': subtotal,
        'total_price': total_price,
        'shipping_price':shipping_price,
    }

    return JsonResponse(data)

import json
def order_summary(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        subtotal = 0
        total_price = 0
        shipping_price= 0
        for item in cart_items:
            subtotal+=item.product.selling_price*item.product_quantity
            total_price+=item.product.selling_price*item.product_quantity
        if subtotal>=499:
            shipping_price = 0
        elif subtotal<0:
            shipping_price = 40

        total_price+=shipping_price
        user_profile = Profile.objects.filter(user=request.user).first()

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'total_price': total_price,
            'shipping_price':shipping_price,
            'user_profile': user_profile,
        }
        return render(request,'checkout.html',context)
    else:
        messages.success(request,"Sign in to your account.")
    return redirect("cart")


def add_to_wishlist(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                prod_id = request.POST.get('product_id')
                product = get_object_or_404(Product, id=prod_id)

                wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
                if wishlist_item:
                    # Product already exists in the cart, update the quantity
                    # cart_item.product_quantity += 1
                    wishlist_item.save()
                    return JsonResponse({'message': "Product already added to the wishlist."})
                else:
                    # Product does not exist in the cart, create a new cart item
                    wishlist_item = Wishlist.objects.create(user=request.user, product=product)
                    return JsonResponse({'message': "Product successfully added to the wishlist."})
        return JsonResponse({'message':'Invalid request'})

    else:
        return JsonResponse({'message':'Please login to your account!!'})

@require_POST
def remove_from_wishlist(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        wishlist_item_id = request.POST.get('wishlist_item_id')
        try:
            wishlist_item = Wishlist.objects.get(id=wishlist_item_id)
            wishlist_item.delete()
            return JsonResponse({'message': 'Item removed successfully'})
        except Wishlist.DoesNotExist:
            return JsonResponse({'message': 'Item does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)


@login_required(login_url="login")
def checkout(request):
    if request.method=="POST":
        current_user = User.objects.filter(id=request.user.id).first()
        if not current_user.first_name:
            current_user.first_name = request.POST.get('fname')
            current_user.last_name = request.POST.get('lname')
            current_user.save()

        if not Profile.objects.filter(user=request.user):
            user_profile = Profile()
            user_profile.user = request.user
            user_profile.phone = request.POST.get('phone')
            user_profile.address = request.POST.get('address')
            user_profile.city = request.POST.get('city')
            user_profile.state = request.POST.get('state')
            user_profile.country = request.POST.get('country')
            user_profile.pincode = request.POST.get('pincode')
            user_profile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('paymentMethod')
        cart_items = Cart.objects.filter(user=request.user)
        subtotal = 0
        total_price = 0
        shipping_price= 0
        for item in cart_items:
            subtotal+=item.product.selling_price*item.product_quantity
            total_price+=item.product.selling_price*item.product_quantity
        if subtotal>=499:
            shipping_price = 0
        elif subtotal<0:
            shipping_price = 40

        total_price+=shipping_price
        neworder.total_price = total_price
        track_no = 'is'+str(random.randint(11111111,99999999))
        while (Order.objects.filter(tracking_no=track_no)).exists():
            track_no = 'is'+str(random.randint(11111111,99999999))
        neworder.tracking_no=track_no
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_quantity
            )
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity-item.product_quantity
            orderproduct.save()

        Cart.objects.filter(user=request.user).delete()


    return render('checkout.html',{})


stripe.api_key = settings.STRIPE_SECRET_KEY




def view_orders(request):
    # Fetch orders associated with the currently logged-in user
    user_orders = Order.objects.filter(user=request.user)

    context = {
        'orders': user_orders,
    }

    return render(request, 'orders.html', context)

@csrf_exempt
def payment(request,total_price):
    if request.method=='POST':
        cart_items = Cart.objects.filter()
        # cart_items = json.loads(cart_items)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data':{
                            'currency':'inr',
                            'product_data':{
                                'name':'Pay',

                                # 'unit_amount': items.get_total()*100,
                            },
                            'unit_amount':total_price*100,

                        },
                        'quantity': 1,
                        # 'name': 'ecommerce',  # You can set a custom name for the line item
                        # 'amount': int(total_amount * 100),  # Stripe expects amount in cents
                        # 'currency': 'inr',  # Replace with your currency code


                    }


                ],

                mode='payment',
                success_url='http://ishitasharma.pythonanywhere.com',
                cancel_url='http://ishitasharma.pythonanywhere.com',

            )
        except Exception as e:
            return HttpResponse(e)

        return redirect(checkout_session.url)
