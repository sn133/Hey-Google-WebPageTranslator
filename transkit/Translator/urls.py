from django.urls import path
from . import views
from Translator import views
from django.conf import settings
from django.conf.urls.static import static
from .views import generate_order

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('home', views.home, name='home'),
    # path('home1', views.home1, name='home1'),
    path('translate/', views.translate_view, name='translate'),
    path('generate_order/', generate_order, name='generate_order'),
    # path('razorpay_payment_callback/', views.razorpay_payment_callback, name='razorpay_payment_callback'),
]