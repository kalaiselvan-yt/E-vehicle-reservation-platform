from django.contrib import admin
from django.urls import include, path
from authentication import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name="about"),
    path('service', views.service, name="service"),
    path('contact', views.contact, name="contact"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('confirm/<str:fname>/', views.confirm, name='confirm'),
    path('book_location/', views.book_location, name='book_location'),
]
