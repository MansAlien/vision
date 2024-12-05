from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.filters import UserProfileFilter
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


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for consistent pagination across viewsets
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class JobTitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing JobTitle endpoints.
    """
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]


class CountryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Country endpoints.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]


class GovernorateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Governorate objects.
    Dynamically selects serializer class based on the request method.
    """
    queryset = Governorate.objects.select_related('country').all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

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
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return CityDetailSerializer
        return CityUpdateSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing UserProfile objects.
    Only allows retrieving and updating profiles, as creation and deletion are handled through User model.
    Includes pagination, filtering, and custom actions.
    """
    queryset = UserProfile.objects.select_related(
        'user',
        'job_title',
        'city',
        'city__governorate',
        'city__governorate__country'
    ).all()
    filterset_class = UserProfileFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    search_fields = ['user__username', 'user__email', 'address']
    ordering_fields = ['age', 'salary', 'start']
    ordering = ['-start']  # Default ordering
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']  # Only allow GET and UPDATE operations

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return UserProfileDetailSerializer
        return UserProfileUpdateSerializer

    @action(detail=True, methods=['get'])
    def deductions_summary(self, request, pk=None):
        """Get summary of user's deductions"""
        profile = self.get_object()
        deductions = profile.deduction_set.all()
        
        summary = {
            'total_deductions': sum(d.amount for d in deductions),
            'deduction_count': deductions.count(),
            'latest_deduction': DeductionDetailSerializer(
                deductions.order_by('-date').first()
            ).data if deductions.exists() else None
        }
        return Response(summary)

    @action(detail=True, methods=['get'])
    def salary_history(self, request, pk=None):
        """Get user's salary history"""
        profile = self.get_object()
        history = profile.salaryhistory_set.all().order_by('-start')
        return Response(SalaryHistorySerializer(history, many=True).data)


class DeductionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Deduction objects.
    Includes pagination, filtering, and error handling.
    """
    queryset = Deduction.objects.select_related("user_profile", "user_profile__user").all()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    search_fields = ['name', 'description']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return DeductionDetailSerializer
        return DeductionUpdateSerializer

    # def perform_create(self, serializer):
    #     """Create deduction with additional validation"""
    #     try:
    #         with transaction.atomic():
    #             instance = serializer.save()
    #             # Update user's salary history if needed
    #             profile = instance.user_profile
    #             if profile.salary != profile.salary - instance.amount:
    #                 SalaryHistory.objects.create(
    #                     user_profile=profile,
    #                     amount=profile.salary - instance.amount,
    #                     start=instance.date
    #                 )
    #     except Exception as e:
    #         raise serializers.ValidationError(str(e))


class BlackListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing BlackListedAccessToken objects.
    """
    queryset = BlacklistedAccessToken.objects.all()
    serializer_class = BlacklistedAccessTokenSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]


class JobTitleHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing JobTitleHistory objects.
    """
    queryset = JobTitleHistory.objects.select_related("user_profile", "job_title").all()
    serializer_class = JobTitleHistorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']


class SalaryHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing SalaryHistory objects.
    """
    queryset = SalaryHistory.objects.select_related("user_profile").all()
    serializer_class = SalaryHistorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']


class LoggedInUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LoggedInUser objects.
    """
    queryset = LoggedInUser.objects.all()
    serializer_class = LoggedInUserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
