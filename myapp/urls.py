from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login_page',views.login_page,name='login_page'),
    path('singup_page',views.signup_page,name='signup_page'),
    path('about',views.about,name='about'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('add_category',views.add_category,name='add_category'),
    path('logout',views.logout,name='logout'),
    path('add_product',views.add_product,name='add_product'),
    path('view_product',views.view_product,name='view_product'),
    path('delete_product/<int:p>',views.delete_product,name='delete_product'),
    path('view_user',views.view_user,name='view_user'),
    path('delete_user/<int:u>',views.delete_user,name='delete_user'),
    path('product_page',views.product_page,name='product_page'),
    path('cart',views.cart,name='cart'),
    path('add_cart/<int:pd>',views.add_cart,name='add_cart'),
    path('add/<int:ct>',views.add,name='add'),
    path('sub/<int:ct>',views.sub,name='sub'),
    path('remove/<int:ct>',views.remove,name='remove'),
    path('checkout',views.chcekout,name='checkout')
]
