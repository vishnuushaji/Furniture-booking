from django.urls import path
from .views import (
    IndexView, CartView, CheckoutView, ContactView,
    ShopView, ThankYouView,
    SignupView, LoginView, LogoutView,
    PasswordChangeView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    ActivateAccountView 
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('thankyou/', ThankYouView.as_view(), name='thankyou'),
    path('contact/', ContactView.as_view(), name='contact'),

    # Authentication-related URLs
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordResetDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
]
