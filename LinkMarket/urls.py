from django.urls import path
from django.urls import path
from .views import landing_page, register, login_view, seller_account, product_edit, product_create, product_list, dash, category_create, category_list, product_delete, category_delete, category_detail, category_edit, logout_view, product_detail, buyer_account, About,  products_detail, orders_list, business_create_or_detail, business_list, product_display, cart, add_to_cart, remove_from_cart, create_order, checkout, seller_dashboard_view, buyer_Home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('LinkMarket/', landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('Market/<int:business_id>/', buyer_account, name='buyer_account'),
    path('seller dashboard/', seller_account, name='seller_account'),
    path('product_edit/<int:id>/edit/', product_edit, name='product_edit'),
    
    path('orders/', orders_list, name='orders_list'),
    path('seller/dashboard/<int:business_id>/', seller_dashboard_view, name='orders_list'),
    path('product_create/', product_create, name='product_create'),
    path('product/view/<int:id>/view/', product_detail, name="product_detail"),
    path('product/<int:id>/delete/', product_delete, name='product_delete'),
    path('products/', product_list, name='product_list'),
    path('dash/', dash, name="dash"),
    path('logout/', logout_view, name='logout'),
    
    # category
    path('category/',  category_create, name='category-create'),
    path('categoryList/', category_list, name="category_list"),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),
    path('category/view/<int:id>/view/', category_detail, name="category_detail"),
    path('category/edit/<int:id>/view/', category_edit, name="category_edit"),
    path('About/', About, name="about"),
    path('buyer/', buyer_Home, name="buyer_Home"),
    
    # cart
    path('product/<int:id>/view/', products_detail, name='products_detail'),
    path('cart/', cart, name="cart"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('create-order/', create_order, name='create_order'),
    path('checkout/', checkout, name='checkout'),
    # business
    path('business/', business_create_or_detail, name='business_create_or_detail'),
    path('businesses/', business_list, name='business_list'),
    path('businesses/<int:pk>/', product_display, name='business_products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)