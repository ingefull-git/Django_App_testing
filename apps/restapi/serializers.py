from django.contrib.auth import get_user_model
from django.http import Http404
# from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from apps.logchecker.models import District
from apps.accountuser.models import UserAccount
User = get_user_model()


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('user', 'name', 'psid', 'status', 'created')

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'username', 'password', 'password2', 'created')
        extra_kwargs = {
            'password': {'write_only': True}
            }
        
    def save(self, *args, **kwargs):
        useraccount = UserAccount(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise ValidationError({'password': 'Password must match'})
        useraccount.set_password(password)
        useraccount.save()
        return useraccount


class UserAccountGetUpdateSerializer(serializers.ModelSerializer):

    # username = serializers.SerializerMethodField('get_username_from_useraccount')

    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'username', 'created', 'login', 'password',)

    # def get_username_from_useraccount(self, user_account):
    #     username = user_account.username
    #     return username

    def save(self, *args, **kwargs):
        userid = self.data['id']
        try:
            useraccount = UserAccount.objects.get(pk=userid)
        except UserAccount.DoesNotExist:
            useraccount = None
        useraccount.email=self.validated_data['email']
        useraccount.username=self.validated_data['username']
        password = self.validated_data['password']
        useraccount.set_password(password)
        useraccount.save()
        return useraccount