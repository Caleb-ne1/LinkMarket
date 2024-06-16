from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomLoginForm, ProductForm, CategoryForm, BusinessForm
from django.http import HttpResponse, JsonResponse
from .models import Product, Category, Cart, Business, CartItem, Order, OrderItem
import random
from django.urls import reverse

# Register View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'buyer':
                return redirect('business_list')
            else:
                return redirect('seller_account')
        else:
            print(form.errors)
    else:
        selected_role = request.session.get('selectedRole')
        form = CustomUserCreationForm(initial={'role': selected_role})
    return render(request, 'LinkMarket/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'buyer':
                    return redirect('business_list')
                else:
                    return redirect('seller_account')
            else:
                form.add_error(None, 'Invalid email or password')
        else:
            print(form.errors)
    else:
        form = CustomLoginForm()
    return render(request, 'LinkMarket/login.html', {'form': form})


# logout
def logout_view(request):
    logout(request)
    return redirect('login')

def landing_page(request):
    return render(request, 'LinkMarket/index.html')


# buyer account
def buyer_account(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    products = Product.objects.filter(business=business)
    return render(request, 'LinkMarket/buyer/ecom.html', {'business': business, 'products': products})

def buyer_Home(request):
    return render(request, 'LinkMarket/buyer/ecom.html')
# seller account
def seller_account(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = f"{first_name} {last_name}"
    initials = f"{first_name[0]}{last_name[0]}".upper()
    return render(request, 'LinkMarket/seller/dash2.html', {'first_name': first_name, 'initials': initials, 'full_name': full_name})

def name(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = f"{first_name} {last_name}"
    
    return render(reverse('seller_account', {'full_name': full_name}))
# dashboard
def dash(request):
    return render(request,'LinkMarket/seller/dash.html' )

# Business logic
def business_create_or_detail(request):
    try:
        business = Business.objects.get(user=request.user)
        return render(request, 'LinkMarket/seller/business_detail.html', {'business': business})
    except Business.DoesNotExist:
        if request.method == 'POST':
            form = BusinessForm(request.POST, request.FILES)
            if form.is_valid():
                business = form.save(commit=False)
                business.user = request.user
                business.save()
                return redirect('LinkMarket/seller/business_detail') 
        else:
            form = BusinessForm()
        return render(request, 'LinkMarket/seller/business_form.html', {'form': form})


# product logic 
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            business = Business.objects.get(user=request.user)
            product.business = business
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'LinkMarket/seller/add-product.html', {'form': form})

def product_list(request):
    try:
        business = Business.objects.get(user=request.user)
    except Business.DoesNotExist:
        business = None
    if business:
        products = Product.objects.filter(business=business)
    else:
        products = Product.objects.none() 
    return render(request,  'LinkMarket/seller/products.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'LinkMarket/seller/product_detail.html', {'product': product})

def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'LinkMarket/seller/product_form.html', {'form': form})

def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  
    return render(request, 'LinkMarket/seller/product_confirm_delete.html', {'product': product})




# category logic
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user 
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'LinkMarket/seller/category_form.html', {'form': form})
        
def category_list(request):
    categorys = Category.objects.filter(user=request.user)
    return render(request, 'LinkMarket/seller/category_list.html', {'categorys': categorys, })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'LinkMarket/seller/category_confirm_delete.html', {'category': category})    

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    return  render(request, 'LinkMarket/seller/category_detail.html', {'category': category})

@login_required
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'LinkMarket/seller/category_edit.html', {'form': form})


    
# customer
def business_list(request):
    businesses = Business.objects.all()
    return render(request, 'LinkMarket/buyer/businessList.html', {'businesses': businesses})

def product_display(request, pk):
    business = get_object_or_404(Business, pk=pk)
    products = Product.objects.filter(business=business)
    return render(request, 'LinkMarket/buyer/ecom.html', {'business': business, 'products': products})

def category_display(request, fk):
    categorys = Category.objects.filter(user=request.user)
    business = Business.object.filter(business_id=fk)
    return render(request, 'LinkMarket/buyer/ecom.html', {'categorys': categorys})

def checkout(request):
    return render(request, 'LinkMarket/buyer/checkout.html')

def About(request):
    return render(request, "LinkMarket/About.html")


@login_required
def products_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'LinkMarket/buyer/view.html', {'product': product})




@login_required
def orders_list(request):
    return render(request, 'LinkMarket/seller/orders.html')

@login_required
def seller_dashboard_view(request):
    orders = Order.objects.filter(business__user=request.user)
    return render(request, 'orders_list', {'orders': orders})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    business = product.business  
    cart, created = Cart.objects.get_or_create(user=request.user, business=business)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect(reverse('cart'))

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect(reverse('cart'))

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    total = cart.total()
    return render(request, 'LinkMarket/buyer/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def create_order(request):
   if request.method == 'POST':
        cart_items = request.user.cart.cart_items.all()
        
        for cart_item in cart_items:
            quantity_input = request.POST.get(f'quantity_{cart_item.id}')
            if quantity_input:
                cart_item.quantity = int(quantity_input)
                cart_item.save()

        
        total_price = sum(cart_item.subtotal() for cart_item in cart_items)
        
        order = Order.objects.create(user=request.user, business=request.user.cart.business, total_price=total_price)
       
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, subtotal=cart_item.subtotal())
        
        request.user.cart.cart_items.all().delete()
        
        return redirect('checkout')
    
    

