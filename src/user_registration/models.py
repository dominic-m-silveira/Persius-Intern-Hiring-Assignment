from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy


# Create your models here.

class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = Profile.objects.get_or_create(user=user)
        print(created)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def toggle_remove_follow(self, user, to_toggle_user):
        user_profile, created = Profile.objects.get_or_create(user=to_toggle_user)
        print(created)
        # if to_toggle_user in user_profile.following.all():
        user_profile.following.remove(user)
        # return True
        # else:
        #     user_profile.following.add(user)
        #     added = True
        # return added

    def is_following(self, user, followed_by_user):
        user_profile, created = Profile.objects.get_or_create(user=user)
        print(user_profile.following.all())

        if created:
            return False
        for users in user_profile.following.all():
            if followed_by_user == users.username:
                return True
                break
        return False


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_by', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="profile_pic", null=True, blank=True)

    objects = UserProfileManager()  # User.objects.all()

    ##abc=...   User.abc.all()
    def get_following(self):
        return self.following.all().exclude(username=self.user)

    def get_follow_url(self):
        return reverse_lazy("user-follow", kwargs={"slug": self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("user-profile", kwargs={"slug": self.user.username})

    def __str__(self):
        return str(int(self.pk))

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
