from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.serializers import JobTitleHistorySerializer

from .views import (
    BlackListViewSet,
    CityViewSet,
    CountryViewSet,
    DeductionViewSet,
    GovernorateViewSet,
    JobTitleHistoryViewSet,
    JobTitleViewSet,
    LoggedInUserViewSet,
    SalaryHistoryViewSet,
    UserProfileViewSet,
)

router = DefaultRouter()
router.register(r'blacklist', BlackListViewSet, basename='blacklist')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'deduction', DeductionViewSet, basename='deduction')
router.register(r'governorate', GovernorateViewSet, basename='governorate')
router.register(r'job-title', JobTitleViewSet, basename='jobtitle')
router.register(r'job-title-history', JobTitleHistoryViewSet, basename='jobtitle_history')
router.register(r'logged-in-user', LoggedInUserViewSet, basename='logged_in_user')
router.register(r'salary-history', SalaryHistoryViewSet, basename='salary_history')
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
]
