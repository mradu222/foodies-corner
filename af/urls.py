"""af URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from allofood import views

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^$', views.index, name="index"),

    re_path(r'^restaurants/$', views.restaurants, name="restaurants"),

    re_path(r'^register/$', views.register, name="register"),

    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),

    re_path(r'^restaurants/(?P<restaurant_link>quality|2N)/$', views.restaurant, name="restaurant"),

    re_path(r'^comment/$', views.comment, name="comment"),

    re_path(r'^cart/$', views.cart, name="cart"),

    re_path(r'^checkout/$', views.checkout, name="checkout"),

    re_path(r'^confirm/uid=(?P<uid>.+?)&token=(?P<token>.+?)/$', views.confirm, name="confirm"),

    re_path(r'^Merci/$', views.redir, name="redir"),

    re_path(r'^order/$', views.order, name="order"),

    re_path(r'^orders/$', views.orders, name="orders"),

]
