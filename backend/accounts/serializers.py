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
    Includes nested relationships.
    """
    user = serializers.CharField(source = 'user.username')
    country = serializers.CharField(source="city.governorate.country.name")
    governorate = serializers.CharField(source="city.governorate.name")
    city = serializers.CharField(source="city.name")
    job_title = serializers.CharField(source="job_title.name")
    class Meta:
        model = UserProfile
        fields = (
            'user',
            'job_title',
            'country',
            'governorate',
            'city',
            'age',
            'date_of_birth',
            'start',
            'address',
            'gender',
            'salary'
        )

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating UserProfile (POST, PUT, PATCH, DELETE requests).
    Does not include nested relationships.
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


class JobTitleHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for JobTitleHistory.
    Tracks job title changes over time for a UserProfile.
    """
    job_title = JobTitleSerializer()
    # user_profile = UserProfileSerializer()
    class Meta:
        model = JobTitleHistory
        fields = ('job_title', 'user_profile', 'start', 'end')


class SalaryHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for SalaryHistory.
    Tracks salary changes over time for a UserProfile.
    """
    # user_profile = UserProfileSerializer()
    class Meta:
        model = SalaryHistory
        fields = ('amount', 'user_profile', 'start', 'end')


class DeductionSerializer(serializers.ModelSerializer):
    """
    Serializer for Deduction.
    Represents salary deductions for a UserProfile.
    """
    # user_profile = UserProfileSerializer()
    class Meta:
        model = Deduction
        fields = ('user_profile', 'name', 'amount', 'date', 'discription')


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
        fields = ('token')


