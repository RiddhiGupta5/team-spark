import hashlib
from django.db import models


class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10)
    address = models.TextField()
    password = models.CharField(max_length=1000)

    def __str__(self):
        return self.email + '|' + str(id)

    def save(self, *args, **kwargs):
        m = hashlib.md5()     
        m.update(self.password.encode("utf-8")) 
        self.password = str(m.digest())
        super().save(*args, **kwargs)

class Organization(models.Model):
    org_name = models.CharField(unique=True, max_length=80)
    address = models.TextField()
    areas_catered = models.TextField()
    description = models.TextField(null=True)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    web_link = models.URLField(null=True)
    password = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        m = hashlib.md5()     
        m.update(self.password.encode("utf-8")) 
        self.password = str(m.digest())
        super().save(*args, **kwargs)


class CustomToken(models.Model):
    token = models.CharField(max_length=500)
    object_id = models.IntegerField()
    user_type = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)

class Donation(models.Model):
    item_name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=20)
    description = models.TextField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    org_id = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    location = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True)

class HelpProgram(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    prg_name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    aid_provided = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    address = models.TextField(null=True)
    date_time = models.DateTimeField(auto_now_add=True)

class PhoneNumbers(models.Model):
    phone_no = models.CharField(max_length=10, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)