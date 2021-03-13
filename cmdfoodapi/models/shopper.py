from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class Shopper(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    profile_img = models.ImageField(_("Profile Image"), blank=True, upload_to='profiles/')
    pref_zip = models.PositiveIntegerField(validators=[MinValueValidator(9999), MaxValueValidator(100000)])