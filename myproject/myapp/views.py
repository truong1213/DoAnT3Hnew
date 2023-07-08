import json
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .forms import CustomUserCreationForm,ProductForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import TokenRegister,CustomUser,Product,Category,TokenReset,Cart
from .serializers import TokenRegisterSerializer,ProductSerializer,ProfileSerializer,TokenResetSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.decorators import permission_classes
import os
from django.conf import settings
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
# ********************************  REGISTER   ************************************
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request,'myapp/register.html',locals())
    def post(self, request, *args, **kwargs):
        
        form = CustomUserCreationForm(request.POST)
        data = request.POST
        email = data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            return JsonResponse(data={'message':"email đã sử dụng để đăng kí trước đó"})
        else: 
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                token = TokenRegister.objects.create(user=user)
                serializer = TokenRegisterSerializer(token)
                html = render_to_string('myapp/mailregister.html',{'token':serializer.data['token']})
                send_mail(
                    subject='',
                    html_message=html,
                    message=html,
                    fail_silently=False,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return HttpResponse(f'Đăng kí thành công. Chúng tôi đã gửi mail xác nhận cho bạn ')
            else:
                return HttpResponse(f'đăng kí thất bại {form.error_messages}')
class ResendMail(APIView):
    permission_classes = [AllowAny]
    def post(self, request,email):
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            token = TokenRegister.objects.filter(user=user).first()   
            if token is not None:
                token_send = token
            else:
                token_send = TokenRegister.objects.create(user=user)
                
            serializer = TokenRegisterSerializer(token_send)
            html = render_to_string('myapp/mailregister.html',{'token':serializer.data['token']})
            send_mail(
                        subject='',
                        html_message=html,
                        message=html,
                        fail_silently=False,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                    )
            return HttpResponse(f'Đăng kí thành công. Chúng tôi đã gửi mail xác nhận cho bạn ')
        else:
            return HttpResponse(f'Tài khoản không tồn tại')
class VerifyRegisterComplete(APIView):
    permission_classes = [AllowAny]
    def get(self, request, token):
        token = TokenRegister.objects.filter(token=token).first()
        if token:
            email = token.user
            user = CustomUser.objects.filter(email=email).first()
            user.is_active = True
            user.save()
            token.delete()
            TokenRegister.objects.filter(user=user).delete()
            return HttpResponse(f'Xác nhận thành công {user.username} ')
        else:
            return HttpResponse('đường link sai ')

# *******************************   ADD_PRODUCT    ************************
class AddProduct(APIView):
    form = ProductForm
    # permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        return render(request,'myapp/addproduct.html',{"form":self.form})
    def post(self, request):
        if request.method == 'POST':
            form = ProductForm(request.POST,files=request.FILES)
            
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Thêm sản phẩm thành công!'})
            else:
                errors = form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)

# ******************************     PRODUCT_DETAIL    **************************
class ProductDetail(APIView):
    def get(self, request,product_id):
        product = Product.objects.filter(id=product_id).first()
        serializer_product = ProductSerializer(product)
        return JsonResponse(data=serializer_product.data,safe=False)

# ******************************     PAGINATION       *****************************
class MyPagination(PageNumberPagination):
    page_size = 6
class MyPagination2(LimitOffsetPagination):
    default_limit=5
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class=ProductSerializer
    pagination_class = MyPagination
class ProductList2(ListAPIView):
    queryset = Product.objects.all()
    serializer_class=ProductSerializer
    pagination_class = MyPagination2
# *****************************     PROFILE        *********************
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        serializer = ProfileSerializer(instance=profile)
        if serializer:
            data = serializer.data
            return HttpResponse(f'{data}')
        else:
            message = "chưa cập nhật thông tin "
            return JsonResponse(data={"message":message})
    def post(self, request, *args, **kwargs):
        data_request = request.POST
        profile = Profile.objects.filter(user=request.user).first()
        if profile is None:
            data = Profile(user=request.user)
            data.adress = data_request['adress']
            data.name = data_request['name']
            data.mobile = data_request['mobile']
            data.save()
            if data.id:
                return JsonResponse(data={"message":"thêm dữ liệu thành công"})
            else:
                return JsonResponse(data={"message":"thêm dữ liệu thất bại"})
        else:
            profile.adress = data_request['adress']
            profile.name = data_request['name']
            profile.mobile = data_request['mobile']
            profile.save()
            return JsonResponse(data={"message":"thêm dữ liệu thành công"})

# ***************************       CHANGE PASWORD      *****************************
class Changepassword(APIView):
    permission_classes = [IsAuthenticated]
    # form = PasswordChangeForm
    def post(self, request):
        form = PasswordChangeForm(user=request.user,data=request.data)
        if form.is_valid():
            form.save()
            return JsonResponse(data={"message":"Đổi mật khẩu thành công"})
        else:
            return JsonResponse(data=form.errors,safe=False)
# ***************************      RESETPASSWORD      ******************************
class ResetPassword(APIView):
    def get(self, request, *args, **kwargs):
        return render(request,'myapp/formresetpass.html')
    def post(self, request):
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email).first()
        if user:
            TokenReset.objects.create(user=user)
            token = TokenReset.objects.filter(user=user).first()
            serializer = TokenResetSerializer(token)
            html = render_to_string('myapp/sendmailresetpassword.html',{"token":serializer.data['token']})     
            send_mail(
                subject="mail reset password",
                message=html,
                html_message=html,
                from_email='sharingan.cmth@outlook.com',
                recipient_list = [email],
                fail_silently=False,
            )
            return HttpResponse('check your mail')
        else:
            return JsonResponse(data={'message':"Tài khoản chưa đăng kí"})
class ResetPasswordConfirm(APIView):
    def get(self, request, token):
        token_test = TokenReset.objects.filter(token=token).first()
        if token_test:
            return render(request,'myapp/formresetconfirm.html')
        else:
            return redirect('resspassword')
    def post(self, request,token):
        test_token = TokenReset.objects.filter(token=token).first()
        pass1 = request.POST['new_password1']
        pass2 = request.POST['new_password2']
        if pass1 == pass2:
            if test_token:
                email = test_token.user
                password = request.POST.get('new_password1')
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    user.password = password
                    user.save()
                    test_token.delete()
                    TokenReset.objects.filter(user=user).delete()
                    return HttpResponse('đổi mật khẩu thành công')
        return HttpResponse('Đổi mật khẩu thất bại ')


   
 #*****************************      CART            **********************************

# *****************************     CART        *********************
class ShowCart(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).all()
        serializer = CartSerializer(cart,many=True)
        data = serializer.data
        return JsonResponse(data=data,safe=False)
class AddCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,product_id):
        user = request.user
        user_id = user.id
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.filter(user=user_id,product=product).first()
        if cart:
            cart.quantity +=1
            cart.save()
        else:   
            Cart.objects.create(user=user,product=product)
        return JsonResponse(data={"message":"Thành công"})
        
        