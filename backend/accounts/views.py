from rest_framework import viewsets

from accounts.models import (
    BlacklistedAccessToken,
    City,
    Country,
    Deduction,
    Governorate,
    JobTitle,
    JobTitleHistory,
    LoggedInUser,
    SalaryHistory,
    UserProfile,
)
from accounts.serializers import (
    BlacklistedAccessTokenSerializer,
    CityDetailSerializer,
    CityUpdateSerializer,
    CountrySerializer,
    DeductionDetailSerializer,
    DeductionUpdateSerializer,
    GovernorateDetailSerializer,
    GovernorateUpdateSerializer,
    JobTitleHistorySerializer,
    JobTitleSerializer,
    LoggedInUserSerializer,
    SalaryHistorySerializer,
    UserProfileDetailSerializer,
    UserProfileUpdateSerializer,
)


class JobTitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing JobTitle endpoints.
    """
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Country endpoints.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class GovernorateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Governorate objects.
    Dynamically selects serializer class based on the request method.
    """
    queryset = Governorate.objects.select_related('country').all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return GovernorateDetailSerializer
        return GovernorateUpdateSerializer


class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing City objects.
    Dynamically selects serializer class based on the request method.
    """
    queryset = City.objects.select_related('governorate', 'governorate__country').all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return CityDetailSerializer
        return CityUpdateSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing UserProfile objects.
    Dynamically selects serializer class based on the request method.
    """
    queryset = UserProfile.objects.select_related('job_title', 'city', 'city__governorate', 'city__governorate__country').all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return UserProfileDetailSerializer  
        return UserProfileUpdateSerializer


class DeductionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Deduction objects.
    Dynamically selects serializer class based on the request method.
    """
    queryset = Deduction.objects.select_related("user_profile").all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return DeductionDetailSerializer  
        return DeductionUpdateSerializer


class BlackListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing BlackListedAccessToken objects.
    """
    queryset = BlacklistedAccessToken.objects.all()
    serializer_class = BlacklistedAccessTokenSerializer


class JobTitleHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing JobTitleHistory objects.
    """
    queryset = JobTitleHistory.objects.select_related("user_profile", "job_title").all()
    serializer_class = JobTitleHistorySerializer


class SalaryHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing SalaryHistory objects.
    """
    queryset = SalaryHistory.objects.select_related("user_profile").all()
    serializer_class = SalaryHistorySerializer


class LoggedInUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LoggedInUser objects.
    """
    queryset = LoggedInUser.objects.all()
    serializer_class = LoggedInUserSerializer

