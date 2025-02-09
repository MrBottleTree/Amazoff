from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from .models import *

def common_navbar_data(request):
    person = people.objects.get(user_name=request.user.username)
    items_in_cart = cartitems.objects.filter(
        cart=cart.objects.get(
            buyer=people.objects.get(
                user_name=request.user.username
                )
            )
        )
    addresses = address.objects.filter(associated_with=person)
    city = ""
    if addresses:
        city = addresses[0].city
    return {
        'city': city,
        'name': request.user.username.capitalize(),
        'balance': person.wallet,
        'items_in_cart': len(items_in_cart),
    }

def home(request):
    if request.user.is_authenticated:
        return render(request, "amazoff/home.html", common_navbar_data(request))
    else:
        return render(request, "amazoff/login.html", {"message":"To use this website, please login."})

def _logout(request):
    if request.user.is_authenticated:
        logout(request)
        message = "You have been logged out successfully!."
    else:
        message = "ERROR: You are already logged out."
    return render(request, "amazoff/login.html", {"message":message})

def _login(request):
    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "amazoff/login.html", {"message":"Invalid username or password."})
    else:
        return HttpResponseRedirect(reverse("home"))

def register_view(request):
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        usertype = request.POST["user_type"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        person = people(user_name=user.username, email=user.email, user_type=usertype)
        person.save()
        cart(buyer=person).save()

        login(request, user)
        return redirect("home")
    return render(request, "amazoff/register.html")


def addmoney(request, amount):
    if request.user.is_authenticated:
        person = people.objects.get(user_name=request.user.username)
        person.wallet += amount
        person.save()
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "amazoff/login.html", {"message":"To use this website, please login."})

def dashboard(request):
    if request.user.is_authenticated:
        person = people.objects.get(user_name=request.user.username)
        addresses = address.objects.filter(associated_with=person)
        inventories = inventory.objects.filter(associated_with=person)
        navbar = common_navbar_data(request)
        navbar.update({
            "email":person.email,
            "user_id":person.user_id,
            "user_type":person.user_type.capitalize(),
            "user_inventory":inventories,
            "user_addresses":addresses
            })
        return render(request, "amazoff/dashboard.html", navbar)
    else:
        return HttpResponseRedirect(reverse("home"))

def addaddress(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            street = request.POST["street"]
            city = request.POST["city"]
            state = request.POST["state"]
            zip_code = request.POST["zip_code"]
            country = request.POST["country"]
            person = people.objects.get(user_name=request.user.username)
            address(associated_with=person, street=street, city=city, state=state, zip_code=zip_code, country=country, address_type = person.user_type).save()
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "amazoff/add_address.html", common_navbar_data(request))
    else:
        return HttpResponseRedirect(reverse("home"))
    
def addinventory(request):
    if(request.method == "POST"):
        productid = request.POST["product"]
        quantity = request.POST["quantity"]
        addressid = request.POST["address"]
        selleraddress = address.objects.get(address_id=addressid)
        person = people.objects.get(user_name=request.user.username)
        item = product.objects.get(product_id=productid)
        inventory(product=item, quantity=quantity, associated_with=person, address = selleraddress).save()
        return HttpResponseRedirect(reverse("dashboard"))
    navs = common_navbar_data(request)
    navs.update({
        "user_products":product.objects.filter(seller=people.objects.get(user_name=request.user.username)),
        "user_addresses":address.objects.filter(associated_with=people.objects.get(user_name=request.user.username))
    })
    return render(request, 'amazoff/add_inventory.html', navs)

def addproduct(request):
    if(request.method == "POST"):
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        companyid = request.POST["company"]
        image = request.FILES.get("image")
        if not title or not description or not price or not image:
            return HttpResponseRedirect(reverse("addproduct"))
        person = people.objects.get(user_name=request.user.username)
        item = product(title=title, description=description, price=price, image=image, seller=person, company=company.objects.get(company_id=companyid))
        item.save()
        return HttpResponseRedirect(reverse("addinventory"))
    navs = common_navbar_data(request)
    navs.update({
        "companies":company.objects.all()
    })
    return render(request, 'amazoff/add_product.html', navs)

def allproducts(request, search = ''):
    all_inventories = inventory.objects.all()
    navs = common_navbar_data(request)
    navs.update({
        "all_inventories":all_inventories
    })
    return render(request, "amazoff/all_products.html", navs)