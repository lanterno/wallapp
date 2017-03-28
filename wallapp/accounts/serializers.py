import djoser

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'date_joined',
            'birthdate', 'last_login'
        )
        read_only_fields = ('id', 'date_joined', 'last_login')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    activate = serializers.BooleanField(default=False)

    CLOSED_ACCOUNT_ERROR = "Your account is closed, do you want to reactivate it?"

    default_error_messages = {
        'inactive_account': djoser.constants.INACTIVE_ACCOUNT_ERROR,
        'closed_account': CLOSED_ACCOUNT_ERROR,
        'invalid_credentials': djoser.constants.INVALID_CREDENTIALS_ERROR,
    }

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get(User.USERNAME_FIELD), password=attrs.get('password'))
        if not self.user:
            user = User.objects.filter(email=attrs.get('email'))
            user = user and user[0]  # check if the user exists and reassigns just the first of the queryset
            if user and user.check_password(attrs.get('password')):
                if attrs.pop('activate') and user.email_verified:
                    user.is_active = True
                    user.save()
                    self.user = user
                    return attrs
                elif user.email_verified:
                    raise serializers.ValidationError(self.error_messages['closed_account'])
                else:
                    raise serializers.ValidationError(self.error_messages['inactive_account'])

            raise serializers.ValidationError(self.error_messages['invalid_credentials'])

        return attrs
