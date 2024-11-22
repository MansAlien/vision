from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import JobTitleHistory, LoggedInUser, SalaryHistory, UserProfile

# Receivers
""" Add a record to the JobTitleHistory when the UserProfile is created """
@receiver(post_save, sender=UserProfile)
def create_job_title_history(sender, instance, created, **kwargs):
    if created:
        job_title = instance.job_title
        start = instance.start
        JobTitleHistory.objects.create(
            job_title=job_title, user_profile=instance, start=start
        )


"""
    update the first record at JobTitleHistory when the UserProfile's jobtitle is changed 
    and the first JobTitleHistory record is None
"""
@receiver(pre_save, sender=UserProfile)
def update_first_job_title_history(sender, instance, **kwargs):
    if (
        instance.pk
    ):  # Check if the instance is already in the database (i.e., being updated)
        original_instance = UserProfile.objects.get(pk=instance.pk)
        if original_instance.start != instance.start:
            # Get the first job title history associated with the profile
            first_job_title_history = instance.jobtitlehistory_set.first()
            if first_job_title_history and first_job_title_history.job_title == None:
                first_job_title_history.job_title = (
                    instance.job_title
                )  # Update the job title
                first_job_title_history.start = instance.start  # Update the start time
                first_job_title_history.save()
            elif first_job_title_history.job_title != None:
                first_job_title_history.start = instance.start  # Update the start time
                first_job_title_history.save()
                pass


"""
    update the JobTitleHistory when the UserProfile's jobtitle is changed
    and the first JobTitleHistory record is not None 
"""
@receiver(pre_save, sender=UserProfile)
def update_job_title_history(sender, instance, **kwargs):
    if (
        instance.pk
    ):  # Check if the instance is already in the database (i.e., being updated)
        last_job_title_history = (
            instance.jobtitlehistory_set.last()
        )  # Get the last job title history
        if last_job_title_history:
            if (
                last_job_title_history.job_title != instance.job_title
            ):  # Check if job_title is changed
                last_job_title_history.end = (
                    timezone.now()
                )  # End the current job title period
                last_job_title_history.save()
                # Create a new JobTitleHistory with the new job title
                JobTitleHistory.objects.create(
                    job_title=instance.job_title,
                    user_profile=instance,
                    start=timezone.now(),
                )
                # Cancel the saving process to prevent UserProfile changes
                return


""" create UserProfile record when a new user is created """
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


""" add a new record the the SalaryHistory when the UserProfile's salary is changed """
@receiver(pre_save, sender=UserProfile)
def update_salary_history(sender, instance, **kwargs):
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        # If UserProfile instance is being created, no need to update salary history
        return

    # Check if salary has changed
    if old_instance.salary != instance.salary:
        # If salary changed, update the end date of the last salary history
        last_salary_history = (
            SalaryHistory.objects.filter(user_profile=instance).order_by("start").last()
        )
        if last_salary_history:
            last_salary_history.end = timezone.now()
            last_salary_history.save()

        # Create a new salary history record
        SalaryHistory.objects.create(
            user_profile=instance,
            amount=instance.salary,
            start=timezone.now(),
            end=None,
        )


"""
    update the SalaryHistory when the UserProfile's salary is changed
    and the first SalaryHistory record is not None 
"""
@receiver(pre_save, sender=UserProfile)
def update_first_salary_history(sender, instance, **kwargs):
    if (
        instance.pk
    ):  # Check if the instance is already in the database (i.e., being updated)
        original_instance = UserProfile.objects.get(pk=instance.pk)
        if original_instance.start != instance.start:
            # Get the first salary history associated with the profile
            first_salary_history = instance.salaryhistory_set.first()
            if first_salary_history:
                first_salary_history.start = instance.start  # Update the start time
                first_salary_history.save()

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
