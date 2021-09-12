from django.db import models, migrations
from django.db.models.fields import CharField, IntegerField
from django.contrib.auth.models import User
from django.utils.timezone import now
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    num_followers = IntegerField(default=0)
    last_updated = models.DateTimeField(default = now)
    def __str__(self):
        return self.user.username
class Repository(models.Model):
    name = CharField(default='', max_length=200)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    stars = IntegerField(default=0)
    def __str__(self):
        return self.name
