from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=False, blank=False, validators=[
        RegexValidator(r'[A-Za-z0-9@#$%^&+=]{8,}',
                       message='The password must contain at least one in  A-Z and a-z, 0-9 and special character.')])
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "raj.sandip96@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
