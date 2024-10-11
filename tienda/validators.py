from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator as BaseUserAttributeSimilarityValidator
from django.contrib.auth.password_validation import MinimumLengthValidator as BaseMinimumLengthValidator
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator

class CustomMinimumLengthValidator(BaseMinimumLengthValidator):
    def __init__(self, min_length=8, *args, **kwargs):
        super().__init__(min_length=min_length, *args, **kwargs)
        self.message = _("La contraseña debe tener al menos %(min_length)d caracteres.")

class CustomUserAttributeSimilarityValidator(BaseUserAttributeSimilarityValidator):
    def __init__(self, user_attributes=None, *args, **kwargs):
        if user_attributes is None:
            user_attributes = ['username', 'first_name', 'last_name', 'email']
        super().__init__(user_attributes=user_attributes, *args, **kwargs)
        self.message = _("La contraseña es demasiado similar a tu información personal.")
