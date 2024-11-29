from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CityViewSet,
    CountryViewSet,
    DeductionViewSet,
    GovernorateViewSet,
    JobTitleViewSet,
    UserProfileViewSet,
)

router = DefaultRouter()
router.register(r'job-titles', JobTitleViewSet, basename='jobtitle')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'deduction', DeductionViewSet, basename='deduction')
router.register(r'governorate', GovernorateViewSet, basename='governorate')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
]
