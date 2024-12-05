import django_filters
from .models import UserProfile


class UserProfileFilter(django_filters.FilterSet):
    """
    Enhanced FilterSet for UserProfile with multiple filtering options.
    """
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')  # Filter by username (case-insensitive)
    email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains')
    job_title = django_filters.CharFilter(field_name='job_title__name', lookup_expr='icontains')  # Filter by job title
    country = django_filters.CharFilter(field_name='city__governorate__country__name', lookup_expr='icontains')  # Filter by country
    governorate = django_filters.CharFilter(field_name='city__governorate__name', lookup_expr='icontains')  # Filter by governorate
    city = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains')  # Filter by city
    
    # Date range filters
    start_date_after = django_filters.DateFilter(field_name='start', lookup_expr='gte')
    start_date_before = django_filters.DateFilter(field_name='start', lookup_expr='lte')
    birth_date_after = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='gte')
    birth_date_before = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='lte')
    
    # Salary range filters
    min_salary = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    max_salary = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')
    
    # Gender filter
    gender = django_filters.ChoiceFilter(choices=UserProfile.GENDER_CHOICES)  # Assuming gender has predefined choices
    
    # Online status filter
    is_online = django_filters.BooleanFilter(field_name='user__logged_in_user__is_online')
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'email', 'first_name', 'last_name', 'job_title', 'country',
            'governorate', 'city', 'gender', 'min_salary',
            'max_salary', 'start_date_after', 'start_date_before',
            'birth_date_after', 'birth_date_before', 'is_online'
        ]
