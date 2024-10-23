from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from .forms import CustomUserForm

from django.contrib.auth import authenticate,login,logout

# Create your views here.

from django.http import JsonResponse
import json
from .models import Product, Cart,Favorite

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'shop/index.html',{'products':products})


def register(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Register sucess")
            return redirect('/login_page')
        

    return render(request,'shop/register.html',{'form':form})

def login_page(request):


    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method=="POST":
            name=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=name,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Login Successfully")
                return redirect('/')
            else:
                messages.error(request,"Invalid Creditinals")
                return redirect('/')
    return render(request,'shop/login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logout sucessfully')
    return redirect('/')

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,'shop/collections.html',{'category':category})


def collectionsview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,'shop/products/index.html',{'products':products,"category__name":name})
    
    else:
        messages.warning(request,'No such category found')
        return redirect("collections")
    
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{"products":products})
        else:
            messages.waring(request,"No such Category found")
            return redirect('collections')
    else:
        messages.warning(request,'No such Director found')
        return redirect('collections')



def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        if request.user.is_authenticated:
            try:
                # Correctly parse the request body to JSON
                data = json.loads(request.body.decode('utf-8'))  # decode from bytes to string
                
                product_qty = data['product_qty']
                product_id = data['pid']
                
                # Check if the product exists
                try:
                    product_status = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return JsonResponse({'status': 'Product Not Found'}, status=404)

                # Check if the product is already in the cart
                if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON Data'}, status=400)
        else:
            return JsonResponse({'status': 'Login to Add to Cart'}, status=403)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    else:
        return redirect("/")
    

def remove_cart(request, cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")
def add_to_fav(request):
    if request.user.is_authenticated:
        product_id = request.GET.get('pid')  
        if product_id:
            try:
                product_status = Product.objects.get(id=product_id)
                if product_status:
                
                    if not Favorite.objects.filter(user=request.user, product_id=product_id).exists():
                        
                        Favorite.objects.create(user=request.user, product_id=product_id)
                
                else:
                    pass  
            except Product.DoesNotExist:
             
                pass
        return redirect("/favviewpage")  
    else:
        return redirect("/login_page") 
 

def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favorite.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {"fav": fav})
    else:
        return redirect("/")


def remove_fav(request, fid):
    item = Favorite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")
