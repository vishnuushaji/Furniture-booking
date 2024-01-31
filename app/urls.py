from django.urls import path
from .views import (
   AddNewProductView, SignupView, LoginView, GetUserProfileView,
    GetAllProductsView, GetProductByIdView, CreateOrderView, GetOrderByIdView,
    IndexView, CartView, AboutView, BlogView, CheckoutView , ContactView, ServicesView, ShopView, ThankYouView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cart/', CartView.as_view(), name='cart'),
    path('about/', AboutView.as_view(), name='about'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('services/', ServicesView.as_view(), name='services'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('thankyou/', ThankYouView.as_view(), name='thankyou'),
    path('contact/', ContactView.as_view(), name='contact'),


   
    path('product/', AddNewProductView.as_view(), name='add_new_product'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', GetUserProfileView.as_view(), name='get_user_profile'),
    path('products/', GetAllProductsView.as_view(), name='get_all_products'),
    path('products/<int:pk>/', GetProductByIdView.as_view(), name='get_product_by_id'),
    path('orders/', CreateOrderView.as_view(), name='create_order'),
    path('orders/<int:pk>/', GetOrderByIdView.as_view(), name='get_order_by_id'),

    
    
   
]
