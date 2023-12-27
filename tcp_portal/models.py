from django.contrib.auth.models import User
from django.db import models
import json

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class IP(models.Model):
    overall_ip = models.GenericIPAddressField(unique=True, null=False, blank=False, default='0.0.0.0')

    # Fields for authflag
    authflag_count = models.IntegerField(default=0, null=True, blank=True)
    authflag_accounts = models.TextField(default='[]')

    # Fields for publicFlag
    publicflag_count = models.IntegerField(default=0, null=True, blank=True)
    publicflag_ip = models.TextField(default='[]')

    # Fields for autoflag
    autoflag_count = models.IntegerField(default=0, null=True, blank=True)
    autoflag_ip = models.TextField(default='[]')

    def get_authflag_accounts(self):
        return json.loads(self.authflag_accounts)

    def set_authflag_accounts(self, value):
        self.authflag_accounts = json.dumps(value)

    def get_publicflag_ip(self):
        return json.loads(self.publicflag_ip)

    def set_publicflag_ip(self, value):
        self.publicflag_ip = json.dumps(value)

    def get_autoflag_ip(self):
        return json.loads(self.autoflag_ip)

    def set_autoflag_ip(self, value):
        self.autoflag_ip = json.dumps(value)

    def __str__(self):
        return f"IP {self.overall_ip}"