from django.shortcuts import render, redirect

from django.views.generic import TemplateView, ListView , CreateView
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
    PasswordChangeView as AuthPasswordChangeView,
    PasswordResetView as AuthPasswordResetView,
    PasswordResetDoneView as AuthPasswordResetDoneView,
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
    PasswordResetCompleteView as AuthPasswordResetCompleteView,
)

from django.urls import reverse_lazy
from .forms import UserRegistrationForm,CustomAuthenticationForm
from .models import Product

class IndexView(TemplateView):
    template_name = 'index.html'

class CartView(TemplateView):
    template_name = 'cart.html'

class CheckoutView(TemplateView):
    template_name = 'checkout.html'

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

class ThankYouView(TemplateView):
    template_name = 'thankyou.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserRegistrationForm  # Assuming you have a custom registration form
    success_url = reverse_lazy('login')  # Replace 'login' with your login URL

class LoginView(AuthLoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse_lazy('shop'))

class LogoutView(AuthLogoutView):
    next_page = '/'  

class PasswordChangeView(AuthPasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')

class PasswordResetView(AuthPasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(AuthPasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView(AuthPasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetCompleteView(AuthPasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
