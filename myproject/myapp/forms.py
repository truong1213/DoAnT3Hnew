from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser,Product,Category,Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Nhập mật khẩu",widget=forms.PasswordInput(attrs={'"autocomplete": "new-password",class': 'form-control'}))
    password2 = forms.CharField(label='Nhập lại mật khẩu',widget=forms.PasswordInput(attrs={'"autocomplete": "new-password",class':'form-control'}))
    field_order = ['email', 'username', 'password1', 'password2']
    class Meta:
        model = CustomUser
        fields = ['email','username','password1','password2']
    
class CustomUserChangeForm(UserChangeForm):
    
 class Meta:
    model = CustomUser
    fields = "__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'category', 'product_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
           
        }
        labels = {
            'title': 'Tên sản phẩm',
            'selling_price': 'Giá gốc',
            'discounted_price': 'Giá đã giảm',
            'description': 'Mô tả sản phẩm',
            'category': 'Loại sản phẩm',
            'product_image': 'Ảnh sản phẩm',
        }

    