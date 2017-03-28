from django.db import models

from wallapp.accounts.models import User

from . import settings


class Post(models.Model):

    owner = models.ForeignKey(User, related_name='posts')
    text = models.CharField(max_length=settings.POST_MAX_LENGTH)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
