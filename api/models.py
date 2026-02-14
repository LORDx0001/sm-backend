from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('rektor', 'Rektor (Super Admin)'),
        ('prorektor', 'Prorektor'),
        ('tyuter', 'Tyuter'),
        ('oquv_bolimi', "O'quv Bo'limi"),
        ('inspekciya', 'Inspekciya'),
        ('kadirlar', "Kadirlar Bo'limi"),
        ('kutubxona', 'Kutubxona'),
        ('ombor', 'Ombor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tyuter')
    avatar = models.URLField(blank=True, null=True)


