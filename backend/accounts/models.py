from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class JobTitle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Governorate(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    GENDER = {
        "M": "Male",
        "F": "Female",
    }
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(null=True)
    start = models.DateField(null=True)
    address = models.TextField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default="M")
    salary = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None


class JobTitleHistory(models.Model):
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user_profile} - {self.job_title}"


class SalaryHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user_profile} - {self.amount}"


class Deduction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.TextField(default="")
    date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name="logged_in_user", on_delete=models.CASCADE)
    access_token = models.CharField(max_length=512, null=True, blank=True)  # Store the JWT access token here
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class BlacklistedAccessToken(models.Model):
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

