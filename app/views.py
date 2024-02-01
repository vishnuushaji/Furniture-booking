from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
    PasswordChangeView as AuthPasswordChangeView,
    PasswordResetView as AuthPasswordResetView,
    PasswordResetDoneView as AuthPasswordResetDoneView,
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
    PasswordResetCompleteView as AuthPasswordResetCompleteView,
)
from .tokens import account_activation_token
from .forms import UserRegistrationForm, CustomAuthenticationForm, ContactForm
from .models import Cart, Product
from django.views.decorators.csrf import csrf_exempt

class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart.products.remove(product)
        cart.save()
        return JsonResponse({'success': True})

@method_decorator(transaction.atomic, name='dispatch')
class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, defaults={'products': []})
            if created:
                messages.success(request, 'Your cart has been created.')
            products = cart.products.all()
            return render(request, 'cart.html', {'cart': cart, 'products': products})
        else:
            # User is not logged in, show empty cart
            return render(request, 'cart.html', {'products': []})

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the latest 3 products
        latest_products = Product.objects.all().order_by('-id')[:3]

        context['latest_products'] = latest_products
        return context

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

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            subject = 'Contact Form Submission'
            message_body = f'First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nMessage: {message}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['noufalmhd112@gmail.com'] 
            send_mail(subject, message_body, from_email, to_email, fail_silently=False)

            return render(request, 'contact_success.html') 
        return self.render_to_response({'form': form})

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_activation_email(self.object)
        return HttpResponse('Please check your email to activate your account.')

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        subject = 'Activate your account'
        message = render_to_string('activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user), 
        })
        user.email_user(subject, message)

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



class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            
            if user is not None:
                user.is_active = False
                user.save()
            return HttpResponse('Activation link is invalid or has expired.')
        

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        if product in cart.products.all():
            messages.info(request, 'Product already in cart.')
        else:
            # Add the product to the cart
            cart.products.add(product)
            messages.success(request, 'Product added to cart.')

        return JsonResponse({'success': True})