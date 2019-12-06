import ast
import datetime
from collections import defaultdict, namedtuple

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserForm, LoginForm, OrderForm
from .models import *
from .templatetags.extra_filters import json_cart_to_html

CONSTANTS = {
    'nav': 'allofood/nav.html',
    'form': LoginForm(),
}


def index(request):
    if 'HTTP_REFERER' in request.META:
        if request.META['HTTP_REFERER'] == 'http://127.0.0.1:8000/register/':
            messages.add_message(request, messages.INFO, "already_registered", extra_tags='already_registered')
    best_restaurants = Restaurant.objects.all().order_by('-rating')[:3]
    return render(request, 'allofood/index.html', {'best_restaurants': best_restaurants, 'const': CONSTANTS})


def register(request):
    if 'user' in request.session:
        return redirect('index')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            uid = urlsafe_base64_encode(force_bytes(user.email))
            token = urlsafe_base64_encode(force_bytes(make_password(datetime.datetime.now())))
            user.password = make_password(user.password)
            current_site = get_current_site(request)
            activation_link = f"{current_site}/confirm/uid={uid}&token={token}"
            message = f"Hello {user.first_name}, Here's your activation link:\n {activation_link}"
            subject = 'Thank you for registering to our site'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            user.token = token
            user.save()

            send_mail(subject, message, email_from, recipient_list)
            messages.add_message(request, messages.INFO, "email_sent", extra_tags='email_sent')
            return redirect('redir')
    else:
        form = UserForm()
    return render(request, 'allofood/register.html', {'form': form, 'const': CONSTANTS})


def confirm(request, uid, token):
    userid = force_text(urlsafe_base64_decode(uid))
    user = User.objects.get(email=userid)
    if user and token == user.token:
        user.confirmed = True
        user.token = ''
        user.save()
        messages.add_message(request, messages.INFO, "email_confirmed", extra_tags='email_confirmed')
        return redirect('redir')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                u = User.objects.get(email=email)
                if check_password(password, u.password) and u.confirmed:
                    request.session['user'] = model_to_dict(u, exclude=['password', 'token'])
                    # if the user already loaded a cart before(in a previous session)
                    if request.session['user']['cart'] is not None:
                        request.session['cart'] = ast.literal_eval(request.session['user']['cart'])
                    # if the user loaded a cart before loging in and has no cart from a previous session
                    elif request.session['user']['cart'] is None and 'cart' in request.session:
                        User.objects.filter(pk=request.session['user']['id']).update(cart=str(request.session['cart']))
                        request.session['user'] = model_to_dict(u, exclude=['password', 'token'])
                elif u.confirmed is False:
                    messages.add_message(request, messages.ERROR, "email_not_confirmed", extra_tags='email_not_confirmed')
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, "user_not_found", extra_tags='user_not_found')
    s = '../' + str(request.META.get('HTTP_REFERER', '')).split('/', 3)[-1]
    return redirect(s)


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    if 'cart' in request.session:
        del request.session['cart']
    if 'HTTP_REFERER' in request.META:
        if request.META['HTTP_REFERER'] == 'http://127.0.0.1:8000/checkout/':
            return redirect('index')
    s = '../' + str(request.META.get('HTTP_REFERER', '')).split('/', 3)[-1]
    return redirect(s)


def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'allofood/restaurants.html', {'restaurants': restaurants, 'const': CONSTANTS})


def restaurant(request, restaurant_link):
    type_orders = Product.objects.filter(restaurant=Restaurant.objects.filter(link=restaurant_link)[0]).values(
        'type_order').distinct()
    types = list()  # Product types
    for order in range(type_orders.count()):
        types.append(Product.objects.filter(restaurant=Restaurant.objects.filter(link=restaurant_link)[0],
                                                type_order=(order + 1).__str__()))

    comments = Restaurant.objects.filter(link=restaurant_link)[0].comment_set.all()

    return render(request, 'allofood/restaurant.html', {'types': types, 'comments': comments, 'const': CONSTANTS})


def comment(request):
    # Used Ajax to add comments without refreshing the whole page
    if request.is_ajax():
        form = request.POST
        stars = form.get('stars')
        text = form.get('text')
        restaurant = form.get('restaurant')
        user = request.session['user']
        Comment.objects.create(text=text, rating=stars, user_id=user['id'], restaurant_id=restaurant)
        data = {
            'stars': stars,
            'text': text.replace('\n', '<br>'),
            'username': user['first_name'] + ' ' + user['last_name'],
        }
        return JsonResponse(data)
    s = '../' + str(request.META.get('HTTP_REFERER', '')).split('/', 3)[-1]
    return redirect(s)


def update_cart(cart, product, price = 0, quantity=1):
    if type(cart) is dict:
        if product in cart['products'] and quantity * -1 >= cart['products'][product]['quantity']:
            cart['num_products'] -= cart['products'][product]['quantity']
            cart['total'] -= cart['products'][product]['price'] * cart['products'][product]['quantity']
            del cart['products'][product]
            return cart
        if product in cart['products']:
            cart['products'][product]['quantity'] += quantity
        else:
            cart['products'][product] = {'quantity': quantity, 'price': price}
        cart['num_products'] += quantity
        cart['total'] += cart['products'][product]['price'] * quantity
        return cart


def cart(request):
    # Used Ajax to update the cart without refreshing the whole page
    if request.is_ajax():
        form = request.POST
        if form.get('price'):
            price = int(form.get('price'))
        else:
            price = 0
        if form.get('quantity'):
            quantity = int(form.get('quantity'))
        else:
            quantity = 1
        product = form.get('product')
        if 'user' in request.session:   # user connected
            if request.session['user']['cart'] is None: # empty user cart
                if 'cart' not in request.session:   # empty cart
                    request.session['cart'] = {'products': {}, 'total': 0, 'num_products': 0}
            elif request.session['user']['cart'] != str(request.session['cart']):
                request.session['cart'] = ast.literal_eval(request.session['user']['cart'])
        else:   # user not connected
            if 'cart' not in request.session:   # empty cart
                request.session['cart'] = {'products': {}, 'total': 0, 'num_products': 0}

        request.session['cart'] = update_cart(request.session['cart'], product, price, quantity)
        if 'user' in request.session:
            # update the user cart
            User.objects.filter(pk=request.session['user']['id']).update(cart = str(request.session['cart']))
            request.session['user'] = model_to_dict(User(pk=request.session['user']['id']), exclude=['password', 'token'])
        # return the new cart to JavaScript the update the page without refreshing
        data = {'cart': json_cart_to_html(request.session['cart']), 'items': request.session['cart']['num_products']}
        return JsonResponse(data)


def redir(request):
    return render(request, 'allofood/redir.html')


def checkout(request):
    if 'user' not in request.session:
        return redirect('register')
    if 'cart' in request.session:
        return render(request, 'allofood/checkout.html', {'const': CONSTANTS, 'OrderForm': OrderForm()})
    else:
        return redirect('index')


def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            u = User.objects.get(id=request.session['user']['id'])
            if not check_password(form.cleaned_data['password'], u.password):
                return render(request, 'allofood/checkout.html', {'const': CONSTANTS, 'OrderForm': OrderForm()})
            products = request.session['cart']['products']
            orderDate = datetime.datetime.now()
            for p in products:
                o = Order(quantity=products[p]['quantity'], date=orderDate,
                          subtotal=products[p]['quantity'] * products[p]['price'],
                          address=form.cleaned_data['address'], product_id=Product.objects.get(name=p).id,
                          user_id=request.session['user']['id'], telephone=form.cleaned_data['telephone'])
                o.save()
            del request.session['cart']
            request.session['user']['cart'] = None
            u = User.objects.get(id=request.session['user']['id'])
            u.cart = None
            u.save()
            messages.add_message(request, messages.INFO, "ordered", extra_tags='ordered')
            return redirect('redir')
        else:
            return checkout(request)
    else:
        return checkout(request)


def orders(request):
    if not request.user.is_superuser:    # the orders page is only for admins
        return redirect('index')

    if request.POST.get('markPayed'):    # mark an order as payed
        Order.objects.filter(date=request.POST.get('orderDate')).update(payed=True)

    orders = Order.objects.all()
    if request.POST.get('nonPayed'):    # hide the payed orders
        orders = orders.filter(payed=False)

    if request.POST.get('today'):   # only display today's orders
        todayDate = datetime.datetime.now().date()
        orders = orders.filter(date__year=todayDate.year, date__month=todayDate.month, date__day=todayDate.day)

    ordersByDate = defaultdict(set)
    for order in orders:
        ordersByDate[order.date].add(order)
    displayingOrders = []
    orderTuple = namedtuple('order', ['name', 'address', 'telephone', 'products', 'total', 'payement', 'date'])
    for order in ordersByDate.values():
        name=''
        total=0
        products=''
        for subOrder in order:
            name = ' '.join(User.objects.values_list('first_name', 'last_name').get(pk=subOrder.user_id))
            total += subOrder.subtotal
            product = Product.objects.get(pk=subOrder.product_id)
            products += str(subOrder.quantity) + ' x ' + product.name + ' -- ' + Restaurant.objects.get(pk=product.restaurant_id).name + '<br>'
        displayingOrders.append(orderTuple(name, list(order)[0].address, list(order)[0].telephone, products, total,
                                           list(order)[0].payed, str(list(order)[0].date.replace(tzinfo=None))))

    return render(request, 'allofood/orders.html', {'orders': displayingOrders})
