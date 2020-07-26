# Allofood

A food ordering website built with Django that lets users order food from multiple restaurants and pay on delivery

****

### Usage:

- `git clone https://github.com/Badredine-Kheddaoui/allofood`

- `pip install -r requirements.txt`

- `python manage.py makemigrations`

- `python manage.py migrate`

- `python manage.py runserver`

- go to 'http://127.0.0.1:8000/'

****

To be able to send registration confirmation and password recovery emails you need to provide your google account credentials  in the `settings.py` file:
- EMAIL_HOST_USER  = 'your gmail address'
- EMAIL_HOST_PASSWORD = 'your gmail password'

****

### Tech stack
- Django on the server side
- jQuery and Bootstrap for responsiveness
- AJAX/Django communication to update parts of the page according to the database without refreshing the whole page

****

### Features
- User registration, email confirmation and password recovery(using email)
- Shopping cart saved with products from different restaurants inside a session
- An admin panel to add, update and delete users, restaurants, products and managing orders.
- The content(restaurants rating, reviews and products) is dynamic and changes according to the database
- Since most HTML pages have similar sections(shopping cart, navbar, footer...), They all extend a base HTML page.
- If the user is connected, the content of their cart will be saved in the database for later logins and won't be deleted until they checkout
- If a user is not connected, The content of their cart will be saved in their browsing session and will be copied to the database if they create an account

****

### Security Measures
- User passwords are hashed before saved in the database.
- Protection against Cross Site Request Forgeries by sending the user a token that has to be returned when submitting the form.
- Input fields are sanitized to prevent JavaScript injections.
- Database queries are protected from SQL injection by using query parameterization.

****

### Screenshots

The home page:

![home-login](./images/home-login.jpg)



The restaurants page:

![restaurants](./images/restaurants.png)



A restaurant page:

![quality](./images/quality.jpg)



The shopping cart:

![restaurants-cart](./images/restaurants-cart.png)



The registration page:

![register](./images/register.png)



The checkout page:

![checkout-filled](./images/checkout-filled.png)



The admin panel:

![admin](./images/admin.png)



The orders page(only accessible to the admin):

![orders](./images/orders.png)