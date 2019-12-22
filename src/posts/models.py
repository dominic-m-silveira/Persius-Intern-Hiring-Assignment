import re
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

from .validators import validate_blank_content


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, validators=[validate_blank_content])
    image = models.ImageField(upload_to="posts", null=True, blank=True, default=None)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.user.username) + " | " + str(self.id) + " | " + str(self.created_on))

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-updated_on']

