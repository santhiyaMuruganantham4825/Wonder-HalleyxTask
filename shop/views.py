
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import  Order
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
import jwt
from . models import *


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken



# Home Page
def home(request):
    return render(request, 'shop/index.html')

from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('customer_dashboard')
        else:
            return render(request, 'shop/login.html', {'error': 'Invalid credentials'})
    return render(request, 'shop/login.html')




# Register Page
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'shop/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'shop/register.html', {'error': 'Email already registered'})

        user = User.objects.create_user(username=username, password=password1,
                                        first_name=first_name, last_name=last_name)
        
        login(request, user)
        return redirect('home')
    return render(request, 'shop/register.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def customer_dashboard(request):
    return render(request, 'shop/customer_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'shop/admin_dashboard.html')



from django.contrib.auth.decorators import login_required

@login_required
def customer_dashboard(request):
    # Your logic
    return render(request, 'customer_dashboard.html')


@login_required
def create_order(request):
    if request.method == 'POST':
        # Get form data
        product = ...
        quantity = ...
        Order.objects.create(
            customer=request.user,
            product=product,
            quantity=quantity
        )
        return redirect('order_success')

from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_view(request):
    # your code
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'shop/order.html', {'orders': orders})


from .models import Product
from django.shortcuts import render

def product_list(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id, status=True)
    else:
        products = Product.objects.filter(status=True)

    categories = Category.objects.filter(status=True)
    return render(request, 'shop/product_list.html', {
        'products': products,
        
    })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def profile_and_password_view(request):
    user = request.user

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully.")

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors in the form.")
    else:
        password_form = PasswordChangeForm(user)

    context = {
        'password_form': password_form,
        'user': user,
    }
    return render(request, 'shop/profile.html', context)


@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'joined': user.date_joined,
    })

from django.shortcuts import render
from .models import Product  # Assuming your model is named Product

def product_list_view(request):
    products = Product.objects.filter(status=True)  # Only active products
    return render(request, 'shop/product_list.html', {'products': products})

from django.shortcuts import redirect, get_object_or_404
from .models import Product, CartItem  # Adjust model import if CartItem is elsewhere

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        cart_item.quantity += 1
        cart_item.save()
        return redirect('product_list')  # or any other page
    else:
        return redirect('login')  # or show message


