from django.contrib import admin
from accounts.models import UserProfile, JobTitle, City, Country, Governorate


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(JobTitle)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Governorate)
