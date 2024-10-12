from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Category,Cart,userDetails,Product
import os

# Create your views here.


def home(request):
    cat = Category.objects.all()
    current_user = request.user
    if current_user.is_authenticated:
        ct = Cart.objects.filter(user=current_user)
        num = len(ct)
        return render(request,'home.html',{'category':cat,"number":num})
    else:
        return render(request,'home.html',{'category':cat})


def login_page(request):
    if request.method == "POST":
        usrname = request.POST['username']
        pswd = request.POST['password']
        user = auth.authenticate(username=usrname,password=pswd)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_home')
            else:
                login(request,user)
                return redirect('home')
        else:
            messages.info(request,"Invalid username or password!!")
            return redirect('login_page')

    return render(request,'login.html')


def signup_page(request):

    if request.method == "POST":
        fname = request.POST['f_name']
        lname = request.POST['l_name']
        uname = request.POST['username']
        pswd = request.POST['password']
        adrss = request.POST['address']
        email = request.POST['email']
        contact = request.POST['contact']
        img = request.FILES.get('file')
        if User.objects.filter(username=uname).exists():
            messages.info(request,"This user already exists!!!")
        else:
            usr = User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=pswd,email=email)
            usr.save()
            dt = userDetails(address=adrss,contact=contact,usr_image=img,user=usr)
            dt.save()
            return redirect('login_page')

    return render(request,'signup.html')

def about(request):
    cat = Category.objects.all()
    current_user = request.user
    if current_user.is_authenticated:
        ct = Cart.objects.filter(user=current_user)
        num = len(ct)
        return render(request,'about.html',{'category':cat,'number':num})
    else:
        return render(request,'about.html',{'category':cat,})


@login_required(login_url='login_page')
def admin_home(request):
    return render(request,'admin_home.html')


@login_required(login_url='login_page')
def add_category(request):
    if request.method == "POST":
        ct_name = request.POST['c_name']
        cat = Category(category_name=ct_name)
        cat.save()
        return render(request, 'add_category.html', {'success': True})
    return render(request,'add_category.html')


@login_required(login_url='login_page')
def add_product(request):
    cat = Category.objects.all()
    if request.method == "POST":
        pname = request.POST['p_name']
        pdisc = request.POST['p_disc']
        price = request.POST['p_price']
        catg = request.POST['p_cat']
        img = request.FILES.get('p_image')
        ctg1 = Category.objects.get(id=catg)
        pdt = Product(category=ctg1,name=pname,price=price,discreption=pdisc,pdt_image=img)
        pdt.save()
        return redirect('view_product')
    return render(request,'add_product.html',{'cat': cat})


@login_required(login_url='login_page')
def view_product(request):
    pdt = Product.objects.all()
    return render(request, 'view_product.html',{'product':pdt})


@login_required(login_url='login_page')
def view_user(request):
    usr = userDetails.objects.all()
    return render(request,'view_user.html',{'user':usr})


@login_required(login_url='login_page')
def delete_user(request,u):
    usr = userDetails.objects.get(id=u)
    usr.delete()
    os.remove(usr.usr_image.path)
    return redirect('view_user')


@login_required(login_url='login_page')
def product_page(request):

    cat = Category.objects.all()
    c = request.GET.get('sel')
    current_user = request.user
    ct = Cart.objects.filter(user=current_user)
    num = len(ct)

    if c is not None:
        pdt = Product.objects.filter(category_id=c)  

        if pdt.exists():
            return render(request, 'cat.html', {'product': pdt, 'category': cat, 'number':num})
        else:
            return render(request, 'cat.html', {'category': cat, 'message': 'Product not found for theses Category.', 'number':num})
    else:
        return render(request, 'cat.html', {'category': cat, 'message': 'Please choose a category.', 'number':num})


@login_required(login_url='login_page')
def cart(request):
    current_user = request.user
    crt = Cart.objects.filter(user=current_user)
    num = len(crt)
    cat = Category.objects.all()
    ct = Cart.objects.all()
    user_id = request.user.id
    total = sum(item.subtotal() for item in ct if item.user.id == user_id)
    return render(request,'cart.html',{'category':cat,"cart":ct,'ttl':total, 'number':num})


@login_required(login_url='login_page')
def add_cart(request,pd):
    pdt = Product.objects.get(id=pd)
    user_id = request.user.id
    usr = User.objects.get(id=user_id)
    cart_item ,created = Cart.objects.get_or_create(user=usr,product=pdt)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required(login_url='login_page')
def delete_product(request,p):
    pdt = Product.objects.get(id=p)
    pdt.delete()
    os.remove(pdt.pdt_image.path)
    return redirect('view_product')


@login_required(login_url='login_page')
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login_page')
def add(request,ct):
    crt = Cart.objects.get(id=ct)
    crt.quantity += 1
    crt.save()
    return redirect('cart')


@login_required(login_url='login_page')
def sub(request,ct):
    crt = Cart.objects.get(id=ct)
    if crt.quantity != 1:
        crt.quantity -= 1
    crt.save()
    return redirect('cart')


@login_required(login_url='login_page')
def remove(requst,ct):
    crt = Cart.objects.get(id=ct)
    crt.delete()
    return redirect('cart')


@login_required(login_url='login_page')
def chcekout(request):
    current_user = request.user
    ct = Cart.objects.filter(user=current_user)
    num = len(ct)
    cat = Category.objects.all()
    return render(request,'checkout.html',{'number':num,'category':cat})
    