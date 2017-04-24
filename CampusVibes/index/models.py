from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.signals import user_logged_in, user_logged_out


class MyCircle(models.Model):
    userC = models.ForeignKey(User)
    username = models.CharField(max_length=30)
    Uname = models.CharField(max_length=50)

    def __unicode__(self):
        return self

class LoggedUser(models.Model):
    user = models.ForeignKey(User, primary_key=True)

    def __unicode__(self):
        return self.user.username

    def login_user(sender, request, user, **kwargs):
        LoggedUser(user=user).save()

    def logout_user(sender, request, user, **kwargs):
        try:
            u = LoggedUser.objects.get(user=user)
            u.delete()
        except LoggedUser.DoesNotExist:
            pass

    user_logged_in.connect(login_user)
    user_logged_out.connect(logout_user)

class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    to_user = models.ForeignKey(MyCircle, null=True)
    message = models.CharField(max_length=100)

    def __unicode__(self):
        return self.message

class Notify(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=70)

    def __unicode__(self):
        return self