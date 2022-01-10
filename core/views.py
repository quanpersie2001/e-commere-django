import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from cart.models import Cart
from user.models import CustomerUser
from order.models import Order, ShippingAddress
from django.contrib import messages
from django.utils.safestring import mark_safe


# Create your views here.

class LoginView(View):
    template_name = 'login/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        error_msg = None
        if not username:
            # messages.error(request, 'Username and password cannot be left blank!')
            error_msg = 'Username cannot be left blank!'
        elif not password:
            error_msg = 'Password cannot be left blank!'
        else:
            mUser = authenticate(username=username, password=password)
            if mUser is not None:
                login(request, mUser)
                messages.success(request, 'Log in successfully!')
                return redirect('index')
            else:
                # messages.error(request, 'Invalid Username or password!')
                error_msg = 'Invalid Username or password!'

        context = {
            'error': error_msg,
            'username': username,
            'password': password
        }
        return render(request, 'login/login.html', context)


class SignUpView(View):
    template_name = 'signup/signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        regex_password = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$'

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')

        if not username:
            error_msg = 'Username cannot be left blank!'
        elif not email:
            error_msg = 'Email cannot be left blank!'
        elif not password:
            # messages.error(request, 'Username, email and password cannot be left blank!')
            error_msg = 'Password cannot be left blank!'
        else:
            if not re.fullmatch(regex_email, email):
                error_msg = 'Invalid Email!'
            elif not re.fullmatch(regex_password, password):
                error_msg = mark_safe(
                    '• Uppercase letters: A-Z<br>• Lowercase letters: a-z<br>• Numbers: 0-9<br>•Any of the special characters: @#$%^&+= ')
            else:
                if password == re_password:
                    if CustomerUser.objects.filter(username=username).exists():
                        # messages.error(request, 'Username already exist!')
                        error_msg = 'Username already exist!'
                    else:
                        user = CustomerUser.objects.create_user(username=username, password=password, email=email)
                        user.save()
                        messages.success(request, 'Log in successfully!')
                        login(request, user)
                        return redirect('index')
                else:
                    # messages.error(request, 'Password does not match!')
                    error_msg = 'Password does not match!'

        context = {
            'error': error_msg,
            'username': username,
            'email': email,
        }
        return render(request, self.template_name, context)


def log_out(request):
    logout(request)
    return redirect('/')


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'checkout/checkout.html'
    login_url = '/account/log-in/'

    def get(self, request):
        user = request.user
        cart_items = Cart.get_all_items(user)
        cart_qs = Cart.objects.filter(user=request.user, active=True)
        cart_quantity = Cart.item_quantity(user)

        first_name = user.first_name if user.first_name else ''
        last_name = user.last_name if user.last_name else ''
        email = user.email if user.email else ''
        company = user.company if user.company else ''
        phone_number = user.phone_number if user.phone_number else ''

        if cart_qs.exists():
            cart = cart_qs[0]
        else:
            cart = None

        sub_total = cart.get_total_price
        total = sub_total + 50
        context = {
            'cart_quantity': cart_quantity,
            'cart_items': cart_items,
            'sub_total': sub_total,
            'total': total,
            'first_name': first_name,
            'last_name': first_name,
            'company': company,
            'phone_number': phone_number,
            'email': email,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        company = request.POST.get('company')
        phone_number = request.POST.get('number')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        zip = request.POST.get('zip')
        message = request.POST.get('message')

        user = request.user
        cart = Cart.objects.filter(user=request.user, active=True)[0]

        sub_total = cart.get_total_price
        total = sub_total + 50
        cart_items = Cart.get_all_items(user)

        if not first_name:
            error_msg = 'First name cannot be left blank!'
        elif not last_name:
            error_msg = 'Last name cannot be left blank!'
        elif not phone_number:
            error_msg = 'Phone number cannot be left blank!'
        elif not country:
            error_msg = 'Country cannot be left blank!'
        elif not state:
            error_msg = 'State cannot be left blank!'
        elif not city:
            error_msg = 'City cannot be left blank!'
        elif not add1:
            error_msg = 'Address cannot be left blank!'
        elif not zip:
            error_msg = 'Zip code cannot be left blank!'
        else:
            if not re.fullmatch(regex_email, email):
                error_msg = 'Invalid Email!'
            else:
                order, created = Order.objects.get_or_create(user=user, total_price=total, order_description=message)
                order.save()
                for item in cart_items:
                    item.order = order
                    item.save()
                cart.active = False
                cart.save()
                ShippingAddress.objects.create(user=user, order=order, phone_number=phone_number, address=f'{add1}, {add2}', city=city, country=country, state=state, zipcode=zip)
                messages.success(request, 'Order complete!')
                return redirect('index')

        context = {
            'cart_items': cart_items,
            'sub_total': sub_total,
            'total': total,
            'error': error_msg,
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'phone_number': phone_number,
            'email': email,
            'country': country,
            'state': state,
            'city': city,
            'add1': add1,
            'add2': add2,
            'zip': zip,
            'message': message,
        }
        return render(request, self.template_name, context)
