from rest_framework import serializers
from .models import MyUser
from rest_framework.authtoken.models import Token
from apps.utils.custom_exception import BaseCustomException

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'first_name', 'last_name', 
                'mobile_no', 'description', 'address_line_1', 'address_line_2', 
                'city', 'state', 'country', 'pincode']

    def create(self, validated_data):

        email = validated_data.pop('email').lower()
        user = MyUser.objects.create_user(**validated_data, email=email)
        return user
    
class LoginSerializer(serializers.Serializer):
    """ Login seralizer to authenticat and login a user."""

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate_email(self, email):
        """ Validate if email already exist or not.

        Args:
            email (str)

        Raises:
            BaseCustomException: Email validation message.

        Returns:
            email (str)
        """
        print("----------------",email)
        is_email_exist = MyUser.objects.filter(email=email.lower()).exists()
        if not is_email_exist:
            raise BaseCustomException(detail="Email does not exists.",code=400)
        return email
    
class LoginUserDetailSerializer(serializers.ModelSerializer):

    """ Get details of logged user serializer. """
    token = serializers.SerializerMethodField()

    def get_token(self,obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 
                'mobile_no', 'description', 'address_line_1', 'address_line_2', 
                'city', 'state', 'country', 'pincode','token']

