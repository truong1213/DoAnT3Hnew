from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
 TokenObtainPairView,
 TokenRefreshView,
)
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # **************************    REGISTER    ****************************
    path('register/',views.RegisterView.as_view(),name='register'),
    path('resendmail/<email>',views.ResendMail.as_view(),name='resendmail'),
    path('registercomplete/<token>',views.VerifyRegisterComplete.as_view(),name='VerifyRegisterComplete'),
    # **************************    LOGIN   *********************************
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),
    # *************************     ADD_PRODUCT    *************************
    path('addproduct/',views.AddProduct.as_view(),name="addProduct"),
   
    # *************************     PRODUCT_DETAIL  ************************
    path('productdetail/<product_id>',views.ProductDetail.as_view(),name="productdetail"),
    # *************************     LISTPRODUCT    ********************************
    # path('productlist/',views.ProductList.as_view(),name="productlist"),
    # path('productlist2/',views.ProductList2.as_view(),name="productlist2"),
    # # ************************      PROFILE     **********************************
    path('profile/',views.ProfileView.as_view(),name="profile"),
    # ************************      CHANGEPASSW0RD      *******************************
    path('changepassword/',views.Changepassword.as_view(),name="Changepassword"),
    # ************************      RESETPASSWORD      ****************************
    path('resetpassword/',views.ResetPassword.as_view(),name="resspassword"),
    path('reset-password-confirm/<token>',views.ResetPasswordConfirm.as_view(),name="resetpasswordconfirm"),
    # ************************      CART          *************************
    path('showcart/',views.ShowCart.as_view(),name="showcart"),
    path('addcart/<product_id>',views.AddCart.as_view(),name="addcart"),
    # *************************     SWAGER     ******************************
   path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
]