from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from .models import *

def common_navs_data(request):
    try:
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
        categories = category.objects.all()
        if addresses:
            city = addresses[0].city
        temp1 = list(notifications.objects.filter(user=person))
        temp2 = list(notifications.objects.filter(orderdetail__seller=person))
        temp = [t1 for t1 in temp1 if not t1.read] + [t2 for t2 in temp2 if t2.status == Status.PENDING]
        return {
            'city': city,
            'name': request.user.username,
            'balance': person.wallet,
            'items_in_cart': len(items_in_cart),
            'categories': categories,
            'numnot': len(set(temp))
        }
    except:
        return {}

def home(request):
    if request.user.is_authenticated:
        if not people.objects.filter(user_name=request.user.username).first():
            logout(request)
            return HttpResponseRedirect(reverse("home"))
        return render(request, "amazoff/home.html", common_navs_data(request))
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

        if people.objects.filter(user_name=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if people.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
        except:
            pass
        
        person = people(user_name=username, email=email, user_type=usertype)
        person.wallet = 100000
        person.save()
        cart(buyer=person).save()
        user = User.objects.get(username=username)
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
        if not people.objects.filter(user_name=request.user.username).first():
            logout(request)
            return HttpResponseRedirect(reverse("home"))
        person = people.objects.get(user_name=request.user.username)
        addresses = address.objects.filter(associated_with=person)
        inventories = inventory.objects.filter(associated_with=person)
        navs = {}
        try:
            navs = common_navs_data(request)
        except:
            logout(request)
            return HttpResponseRedirect(reverse("home"))
        navs.update({
            "email":person.email,
            "user_id":person.user_id,
            "user_type":person.user_type.capitalize(),
            "user_inventory":inventories,
            "user_addresses":addresses
            })
        return render(request, "amazoff/dashboard.html", navs)
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
            return render(request, "amazoff/add_address.html", common_navs_data(request))
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
    navs = common_navs_data(request)
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
        cat = request.POST["category"]
        cat = category.objects.get(name=cat)
        image = request.FILES.get("image")
        if not title or not description or not price or not image:
            return HttpResponseRedirect(reverse("addproduct"))
        person = people.objects.get(user_name=request.user.username)
        item = product(title=title, description=description, price=price, image=image, seller=person, company=company.objects.get(company_id=companyid), category = cat)
        item.save()
        return HttpResponseRedirect(reverse("addinventory"))
    navs = {}
    try:
        navs = common_navs_data(request)
    except:
        logout(request)
        return HttpResponseRedirect(reverse("home"))
    navs.update({
        "companies":company.objects.all()
    })
    return render(request, 'amazoff/add_product.html', navs)

def allproducts(request, search = ''):
    if search != '':
        all_inventories = [inv for inv in inventory.objects.all() if search.lower() in inv.product.category.name.lower()] + [inv for inv in inventory.objects.all() if search.lower() in inv.product.title.lower()]
    else:
        search = request.GET.get('q', '')
        if search != '':
            all_inventories = [inv for inv in inventory.objects.all() if search.lower() in inv.product.category.name.lower()] + [inv for inv in inventory.objects.all() if search.lower() in inv.product.title.lower()]
        else:
            all_inventories = inventory.objects.all()
    navs = common_navs_data(request)
    navs.update({
        "all_inventories":all_inventories
    })
    return render(request, "amazoff/all_products.html", navs)

def viewproduct(request, inventory_id):
    item = inventory.objects.get(inventory_id=inventory_id)
    navs = common_navs_data(request)
    similar_products = [inv for inv in inventory.objects.all() if inv.product.category == item.product.category and inv != item]
    navs.update({
        "product":item,
        "similar_products":similar_products
    })
    return render(request, "amazoff/product.html", navs)

def _cart(request, id = -1):
    if(request.method == "POST"):
        person = people.objects.get(user_name=request.user.username)
        _cart, ncreated = cart.objects.get_or_create(buyer=person)
        if ncreated:
            print("creating")
            _cart = cart(buyer=person)
            _cart.save()
        item_response = request.POST["quantity"]
        cartitem = cartitems(cart=_cart, product=product.objects.get(product_id=id), quantity=item_response)
        cartitem.save()
        return HttpResponseRedirect(reverse("viewcart"))
    cart_items = cartitems.objects.filter(cart=cart.objects.get(buyer=people.objects.get(user_name=request.user.username)))
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity
    navs = common_navs_data(request)
    similar_products = []
    for item in cart_items:
        similar_products += [inv for inv in inventory.objects.all() if inv.product.category == item.product.category and inv != item]
    similar_products = list(set(similar_products))
    if similar_products == []:
        similar_products = inventory.objects.all()
    navs.update({
        "cart_items":cart_items,
        "similar_products":similar_products,
        "cart_total":total_price
    })
    return render(request, "amazoff/cart.html", navs)

def remove(request, id):
    cart_item = cartitems.objects.get(id=id)
    cart_item.delete()
    return HttpResponseRedirect(reverse("viewcart"))

def checkout(request):
    cart_items = cartitems.objects.filter(cart=cart.objects.get(buyer=people.objects.get(user_name=request.user.username)))
    total_price = 52.78
    for item in cart_items:
        total_price += float(item.product.price) * float(item.quantity)
    navs = common_navs_data(request)
    wallet_balance = people.objects.get(user_name=request.user.username).wallet
    navs.update({
        "cart_items":cart_items,
        "cart_total":round(total_price, 2),
        "wallet_balance":wallet_balance,
        "addresses":address.objects.filter(associated_with=people.objects.get(user_name=request.user.username))
    })
    return render(request, "amazoff/checkout.html", navs)

def orderconfirmation(request, id):
    cart_items = cartitems.objects.filter(cart=cart.objects.get(buyer=people.objects.get(user_name=request.user.username)))
    total = float(sum([items.product.price * items.quantity for items in cart_items])) + 52.78
    person = people.objects.get(user_name=request.user.username)
    person.wallet = float(person.wallet) - total
    person.save()
    order = orders(total_amount=total, buyer=person, shipped_to=address.objects.get(address_id=id))
    order.save()
    for item in cart_items:
        orderdetail = orderdetails(order=order, product=item.product, quantity=item.quantity, seller=item.product.seller)
        orderdetail.save()
        notifications(user=people.objects.get(user_name=request.user.username), orderdetail=orderdetail).save()
        item.delete()

    return render(request, "amazoff/order_confirmation.html", common_navs_data(request))

def viewnotifications(request):
    person = people.objects.get(user_name=request.user.username)
    temp1 = list(notifications.objects.filter(user=person))
    temp2 = list(notifications.objects.filter(orderdetail__seller=person))
    navs = common_navs_data(request)
    print(person.user_type)
    navs.update({
        "b_notifications":[x for x in temp1 if x.read == False ],
        "s_notifications":[x for x in temp2 if x.status == Status.PENDING],
        "user":person
    })
    return render(request, "amazoff/notifications.html", navs)

def markread(request, id):
    temp = notifications.objects.get(notification_id=id)
    temp.read = True
    temp.save()
    if temp.status != Status.PENDING:
        temp.delete()
    return HttpResponseRedirect(reverse("notifications"))

def updateorderstatus(request, id):
    notification = notifications.objects.get(notification_id=id)
    orderdetail = notification.orderdetail
    post = request.POST
    if "accept" in post:
        inv = inventory.objects.get(product=notification.orderdetail.product, associated_with=notification.orderdetail.seller)
        inv.quantity -= notification.orderdetail.quantity
        seller = inv.associated_with
        seller.wallet = float(seller.wallet) + float(notification.orderdetail.quantity)*float(notification.orderdetail.product.price)
        seller.save()
        notification.read = False
        if inv.quantity <= 0:
            inv.delete()
        else:
            inv.save()
        notification.status = Status.ACCEPTED
        orderdetail.status = Status.ACCEPTED
    elif "reject" in post:
        notification.status = Status.REJECTED
        orderdetail.status = Status.REJECTED
        notification.read = False
        person = notification.user
        person.wallet = float(person.wallet) + float(notification.orderdetail.quantity) * float(notification.orderdetail.product.price) 
        person.save()
    orderdetail.save()
    notification.save()
    temporder = orderdetail.order
    all_details_status = set([detail.status for detail in orderdetails.objects.filter(order = temporder)])
    if Status.PENDING in all_details_status:
        temporder.status = Status.PENDING
    elif Status.REJECTED in all_details_status:
        temporder.status = Status.REJECTED
    elif Status.ACCEPTED in all_details_status:
        temporder.status = Status.ACCEPTED
    temporder.save()
    return HttpResponseRedirect(reverse("notifications"))

def vieworderhistory(request):
    navs = common_navs_data(request)
    order = orders.objects.filter(buyer = people.objects.get(user_name = request.user.username))
    navs.update({"orders":order})
    return render(request, "amazoff/orderhistory.html", navs)