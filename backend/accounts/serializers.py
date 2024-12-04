from rest_framework import serializers

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


class JobTitleSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobTitle model.
    Handles serialization and deserialization of JobTitle objects.
    """
    class Meta:
        model = JobTitle
        fields = ('name',)


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Country model.
    Used for retrieving and creating Country data.
    """
    class Meta:
        model = Country
        fields = ('name',)

class GovernorateDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving Governorate details (GET requests).
    Includes nested relationships.
    """
    country = serializers.CharField(source= "country.name")
    class Meta:
        model = Governorate
        fields = ('country', 'name')

class GovernorateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Governorate (POST, PUT, PATCH, DELETE requests).
    Does not include nested relationships.
    """
    class Meta:
        model = Governorate
        fields = ('country', 'name')


class CityDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving City details (GET requests).
    Includes nested relationships.
    """
    country = serializers.CharField(source="governorate.country.name")
    governorate = serializers.CharField(source="governorate.name")
    class Meta:
        model = City
        fields = ('country', 'governorate', 'name')


class CityUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating City (POST, PUT, PATCH, DELETE requests).
    Does not include nested relationships.
    """
    class Meta:
        model = City
        fields = ('governorate', 'name')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving UserProfile details (GET requests).
    Includes nested relationships and calculated fields.
    """
    user = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email', read_only=True)
    country = serializers.SerializerMethodField()
    governorate = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    years_of_service = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = (
            'user',
            'email',
            'job_title',
            'country',
            'governorate',
            'city',
            'age',
            'date_of_birth',
            'start',
            'address',
            'gender',
            'salary',
            'years_of_service',
        )
    
    def get_job_title(self, obj):
        """Get job title name, handling null values"""
        return obj.job_title.name if obj.job_title else None

    def get_country(self, obj):
        """Get country name, handling null values"""
        if obj.city and obj.city.governorate and obj.city.governorate.country:
            return obj.city.governorate.country.name
        return None

    def get_governorate(self, obj):
        """Get governorate name, handling null values"""
        if obj.city and obj.city.governorate:
            return obj.city.governorate.name
        return None

    def get_city(self, obj):
        """Get city name, handling null values"""
        return obj.city.name if obj.city else None

    def get_years_of_service(self, obj):
        """Calculate years of service from start date to now"""
        from django.utils import timezone
        if obj.start:
            delta = timezone.now().date() - obj.start
            return round(delta.days / 365, 1)
        return 0
    

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating UserProfile (POST, PUT, PATCH, DELETE requests).
    Includes validation and custom field handling.
    """
    class Meta:
        model = UserProfile
        fields = (
            'user',
            'job_title',
            'city',
            'age',
            'date_of_birth',
            'start',
            'address',
            'gender',
            'salary'
        )
    
    def validate_date_of_birth(self, value):
        """Validate that date of birth is not in the future"""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value
    
    def validate_salary(self, value):
        """Validate salary is within acceptable range"""
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative")
        if value > 1000000:  # Example maximum salary
            raise serializers.ValidationError("Salary exceeds maximum allowed value")
        return value

    def validate(self, data):
        """Cross-field validation"""
        if 'date_of_birth' in data and 'age' in data:
            calculated_age = (timezone.now().date() - data['date_of_birth']).days // 365
            if abs(calculated_age - data['age']) > 1:
                raise serializers.ValidationError({
                    'age': 'Age does not match date of birth'
                })
        return data

class JobTitleHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for JobTitleHistory.
    Tracks job title changes over time for a UserProfile.
    """
    job_title = serializers.CharField(source = "job_title.name")
    user_profile = serializers.CharField(source = 'user_profile.user.username')
    class Meta:
        model = JobTitleHistory
        fields = ('job_title', 'user_profile', 'start', 'end')


class SalaryHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for SalaryHistory.
    Tracks salary changes over time for a UserProfile.
    """
    user_profile = serializers.CharField(source = 'user_profile.user.username')
    class Meta:
        model = SalaryHistory
        fields = ('amount', 'user_profile', 'start', 'end')


class DeductionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving Deduction details (GET requests).
    Includes nested relationships and validation.
    """
    user_profile = serializers.CharField(source='user_profile.user.username')
    
    class Meta:
        model = Deduction
        fields = ('user_profile', 'name', 'amount', 'date', 'discription')


class DeductionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Deduction (POST, PUT, PATCH, DELETE requests).
    Includes validation and custom field handling.
    """
    class Meta:
        model = Deduction
        fields = ('user_profile', 'name', 'amount', 'date', 'discription')
    
    def validate_amount(self, value):
        """Validate deduction amount"""
        if value <= 0:
            raise serializers.ValidationError("Deduction amount must be positive")
        
        # Check if deduction exceeds user's salary
        user_profile = self.initial_data.get('user_profile')
        if user_profile:
            if isinstance(user_profile, str):
                try:
                    user_profile = UserProfile.objects.get(user__username=user_profile)
                except UserProfile.DoesNotExist:
                    raise serializers.ValidationError("User profile not found")
            
            if value > user_profile.salary * 0.5:  # Maximum 50% of salary
                raise serializers.ValidationError(
                    "Deduction cannot exceed 50% of user's salary"
                )
        return value
    
    def validate_date(self, value):
        """Validate deduction date"""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Deduction date cannot be in the future")
        return value


class LoggedInUserSerializer(serializers.ModelSerializer):
    """
    Serializer for LoggedInUser.
    Tracks user login sessions and access token status.
    """
    class Meta:
        model = LoggedInUser
        fields = ('user', 'access_token', 'is_online')


class BlacklistedAccessTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for BlacklistedAccessToken.
    Handles tokens that are revoked or invalidated.
    """
    class Meta:
        model = BlacklistedAccessToken
        fields = ('token',)
