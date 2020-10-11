
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Userprofile


class UserSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(validators=[RegexValidator("^0?[5-9]\d{9}$")],
                                max_length=15)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'phone_no', 'password', 'password2')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        email = data['email']
        phoneno = data['phone_no']
        user_qs = User.objects.filter(email=email)
        user_pf_qs = Userprofile.objects.filter(phone_no = phoneno)
        if user_qs.exists():
            raise ValidationError("This email already registered")
        elif user_pf_qs.exists():
            raise ValidationError("This Mobile no already registered")
        else:
            return data


class UserSerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password')