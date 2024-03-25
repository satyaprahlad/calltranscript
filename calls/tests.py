from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from notifications.signals import notify

user =User.objects.first()
notify.send(user, recipient=user, verb='you reached level 10')