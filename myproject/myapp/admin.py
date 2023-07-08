from django.contrib import admin
from .forms import CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser,TokenRegister,Product,Category,Profile,TokenReset,Cart
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(CustomUser)
class NewUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'is_active',
    'is_staff', 'is_superuser', 'last_login',)
    
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    
    fieldsets = (
    ("Thong tin co ban", {'fields': ('username', 'email', 'password')}),
    ('Phan quyen', {'fields': ('is_staff', 'is_active',
    'is_superuser', 'groups', 'user_permissions')}),
    ('Ngay thang', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
    ("Thong tin", {
    'classes': ('wide',),
    'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
    ),
    )
    search_fields = ('email',)
    ordering = ('email',)
@admin.register(TokenRegister)
class TokenRegister(admin.ModelAdmin):
    pass
@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['id','name']
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','category']
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id','user','name']
@admin.register(TokenReset)
class TokenReset(admin.ModelAdmin):
    pass
@admin.register(Cart)
class Cart(admin.ModelAdmin):
    pass

