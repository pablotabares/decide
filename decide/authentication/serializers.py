from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')

class AuthCustomTokenSerializer(serializers.Serializer):
    """ Login by Username and Email"""
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        # Ask for the request attributes
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:

            # Try to find the user with the request data
            user_request = self.get_user_object(email_or_username)

            if (not user_request):
                raise serializers.ValidationError('Unable to login with the provided credentials')

            username = user_request.username
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled')
            else:
                raise serializers.ValidationError('Unable to login with the provided credentials')
        else:
            raise serializers.ValidationError('Must include email_or_username and password')

        attrs['user'] = user
        return attrs

    def get_user_object(self, username_or_email):
        """ Return the user object by email or username"""
        try:
            user = User.objects.get(email=username_or_email)
            return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email)
                return user
            except User.DoesNotExist:
                return None
