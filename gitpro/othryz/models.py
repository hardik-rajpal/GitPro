from django.db import models, migrations
from datetime import datetime
from django.db.models.fields import CharField, IntegerField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.operations import HStoreExtension
class Migration(migrations.Migration):
    ...
    operations=[
        HStoreExtension(),
        ...
    ]
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    repos_str = CharField(default='',max_length=1000)
    num_followers = IntegerField(default=0)
    last_updated = models.DateTimeField(default = datetime.now())
    repos = HStoreField(default=dict)
class Repository(models.Model):
    name = CharField(default='', max_length=200)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    stars = IntegerField(default=0)
# Create your models here.
# class UserProfile(models.Model):
#     # user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
#     # user_id = models.IntegerField(default=0)
#     username = models.CharField(default="js", max_length=150,primary_key=True)
#     last_updated = models.DateTimeField(default = datetime.now())
#     num_followers = models.IntegerField(default=0)
#     
#     repos_str = CharField(default='', max_length=1000)
#     def __str__(self):
#         return str(self.user)