from django import template
from allofood.models import Comment
from allofood.models import User
from allofood.models import Restaurant


def iterate(value):
    r = ''
    for i in range(value):
        r += i.__str__()
    return r


def revrse_iterate(value):
    r = ''
    for i in range(value, 5):
        r += i.__str__()
    return r


def get_username(value):
    if type(value) == Comment:
        username = list(User.objects.values('first_name', 'last_name')
                        .filter(id=Restaurant(pk=value.restaurant_id)
                                .comment_set.filter(user_id=value.user_id)[0]
                                .user_id)[0].values())
        return username.__str__().replace("', '", " ").replace("'", "").replace("[", "").replace("]", "")
    else:
        raise ("This is not a comment object, man")


def get_rating(value):
    if type(value) == Restaurant:
        ratings = list(Restaurant.objects.filter(link=value.link)[0].comment_set.values('rating'))
        sum = 0
        if ratings:
            for v in ratings:
                sum += v.get('rating')
            return int(sum / len(ratings))
        else:
            return 0
    else:
        raise ("This is not a restaurant object, man")


def get_restaurant(value, arg):
    return Restaurant.objects.filter(pk=value[0][0].restaurant_id).values(arg)[0][arg]


def sliders_list(value):
    return value.split(', ')


def json_cart_to_html(value):
    if type(value) is dict:
        cart_div = """<div class="cart-item-header">
      <div class="cart-info title">Product</div>
      <div class="cart-info quantity">Quantity</div>
      <div class="cart-info price">Sub Total</div>
    </div>
    <ul class="cd-cart-items">"""
        for p, infos in value['products'].items():
            cart_div += f"""<li><div class='cart-info title'>{p}</div><div class='cart-info quantity'>
                 <div class='btn-decrement'>-</div>
               <input type="number" class='input-quantity' style='color:black;' value={infos.get('quantity')}>
                 <div class='btn-increment'>+</div>
               </div><div class='cart-info price'>
                 <span class='eachPrice'>{infos.get('price') * infos.get('quantity')}</span>DA
                 </div><div class='cart-info action'>
                 <img class="delete-product" src='/static/allofood/images/trash.svg'>
               </div>
           </li>"""
        if value['total'] > 0:
            cart_div += f"""</ul> <!-- cd-cart-items -->
                        <div class="cd-cart-total">
                        <div class="row">
                        <div class="col-md-8">
                        <p>Prix total: </p>       
                        </div>
                        <div class="col-md-4">
                        <span>{value['total']} DA</span>
                        </div>
                        </div>
                        </div> <!-- cd-cart-total -->"""
        return cart_div


register = template.Library()
register.filter('iterate', iterate)
register.filter('revrse_iterate', revrse_iterate)
register.filter('get_username', get_username)
register.filter('get_rating', get_rating)
register.filter('get_restaurant', get_restaurant)
register.filter('sliders_list', sliders_list)
register.filter('json_cart_to_html', json_cart_to_html)
