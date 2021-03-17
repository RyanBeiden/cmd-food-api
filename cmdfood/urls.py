from pathlib import Path
from django.urls import path
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import include
from django.conf.urls.static import static
from cmdfoodapi.views import register_user, login_user, ProfileViewSet, LocationViewSet, ProductViewSet, ProductListViewSet

base_dir = Path(__file__).resolve().parent.parent

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profiles', ProfileViewSet, 'profile')
router.register(r'locations', LocationViewSet, 'location')
router.register(r'products', ProductViewSet, 'product')
router.register(r'productlists', ProductListViewSet, 'productlist')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
