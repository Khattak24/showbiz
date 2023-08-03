from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class GenderChoices(models.TextChoices):
    MALE = 1, "Male"
    FEMALE = 2, "Female"
    OTHER = 3, "Other"


class RoleChoices(models.TextChoices):
    PROFESSIONAL = 1, "Professional"
    FAN = 2, "Fan"


class User(AbstractUser, models.Model):
    name = models.CharField(max_length=255, default="", null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GenderChoices.choices, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    biography = models.TextField()
    role = models.CharField(max_length=255, choices=RoleChoices.choices, null=True, blank=True)


class Profession(models.Model):
    profession_name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
