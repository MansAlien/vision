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


class GovernorateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Governorate model.
    Includes a reference to the related Country.
    """
    country = CountrySerializer()
    class Meta:
        model = Governorate
        fields = ('country', 'name')


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for the City model.
    Includes a reference to the related Governorate.
    """
    governorate = GovernorateSerializer()
    class Meta:
        model = City
        fields = ('governorate', 'name')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    Includes nested serializers for job title and city relationships.
    """
    job_title = JobTitleSerializer()
    city = CitySerializer()
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
    user_profile = UserProfileSerializer()
    class Meta:
        model = JobTitleHistory
        fields = ('job_title', 'user_profile', 'start', 'end')


class SalaryHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for SalaryHistory.
    Tracks salary changes over time for a UserProfile.
    """
    user_profile = UserProfileSerializer()
    class Meta:
        model = SalaryHistory
        fields = ('amount', 'user_profile', 'start', 'end')


class DeductionSerializer(serializers.ModelSerializer):
    """
    Serializer for Deduction.
    Represents salary deductions for a UserProfile.
    """
    user_profile = UserProfileSerializer()
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


