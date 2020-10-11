from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]\d{9}$")],
                                max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username

