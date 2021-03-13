from pathlib import Path
from django.urls import path
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import include
from django.conf.urls.static import static
from cmdfoodapi.views import register_user

base_dir = Path(__file__).resolve().parent.parent

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG is True:
    urlpatterns += static('media/', base_dir / 'media/')
elif settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)