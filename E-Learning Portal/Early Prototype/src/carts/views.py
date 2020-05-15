from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from courses.models import Course
from .models import Cart

def cart_detail_api_view(request):
    cart_obj , new_obj = Cart.objects.new_or_get(request)
    courses = [{
            "id": x.id,
            "url":x.get_absolute_url(),
            "name":x.name,
            "price":x.price
            }
             for x in  cart_obj.courses.all()]    
    cart_data = {"courses":courses, "subtotal":cart_obj.subtotal, "total":cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj , new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart":cart_obj})

def cart_update(request):
    course_id   = request.POST.get('course_id')
    if course_id is not None:
        try:
            course_obj = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            print("Show message to user, Course Doesn't Exist")
            return redirect("cart:home")
        cart_obj , new_obj = Cart.objects.new_or_get(request)
        if course_obj in cart_obj.courses.all():
            cart_obj.courses.remove(course_obj)
            added = False
        else:    
            cart_obj.courses.add(course_obj)
            added = True
        request.session['cart_items'] = cart_obj.courses.count()

        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.courses.count()
            }
            return JsonResponse(json_data)
    return redirect("cart:home")

def checkout_home(request):
    cart_obj , cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.courses.count() == 0:
        return redirect("cart:home")

    login_form          = LoginForm()
    guest_form          = GuestForm()
    address_form        = AddressForm()
    billing_address_id  = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        "check that order is done"
        is_done = order_obj.check_done()
        if is_done:   
            order_obj.mark_paid()
            request.session['cart_items'] = 0         
            del request.session['cart_id']
            return redirect("cart:success")

    context = {
        "object":order_obj,
        "billing_profile":billing_profile,
        "login_form":login_form,
        "guest_form":guest_form,
        "address_form":address_form,
    }
    return render(request, "carts/checkout.html", context)


def checkout_success_view(request):
    return render(request, "carts/checkout-done.html", {})