from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from MainApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('shop/<mc>/<sc>/<br>/', shop),
    path('login/',login),
    path('logout/',logout),
    path('signup/',signup),
    path('profile/',profile),
    path('updateProfile/',updateProfile),
    path('add-products/',addProduct),
    # here item is the id of the product which is take in view 
    path('delete-product/<item>/',deleteProduct),
    path('update-product/<item>/',UpdateProduct),
    path('single-product/<id>/',singleProduct),
    path('add-to-wishlist/<id>/',wishList),
    path('delete-wishlist/<id>/',deleteWishlist),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
