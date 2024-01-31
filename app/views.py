from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Product, Order
from django.contrib.auth.forms import AuthenticationForm
from .serializers import UserSerializer, ProductSerializer, OrderSerializer,LoginSerializer, SignupSerializer
from .forms import UserCreationForm
class AddNewProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer  
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        user_serializer = UserSerializer(user)
        response_data = {
            'access_token': access_token,
            'refresh_token': str(refresh),
            'user': user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer  
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        user_serializer = UserSerializer(user)
        response_data = {
            'access_token': access_token,
            'refresh_token': str(refresh),
            'user': user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
class GetUserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class GetAllProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class GetProductByIdView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class GetOrderByIdView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class IndexView(TemplateView):
    template_name = 'index.html'

class CartView(TemplateView):
    template_name = 'cart.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class BlogView(TemplateView):
    template_name = 'blog.html'

class CheckoutView(TemplateView):
    template_name = 'checkout.html'

class ServicesView(TemplateView):
    template_name = 'services.html'

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

class ThankYouView(TemplateView):
    template_name = 'thankyou.html'

class ContactView(TemplateView):
    template_name = 'contact.html'
