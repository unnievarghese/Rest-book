from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import book
from django.contrib.auth import authenticate
from rest_framework import exceptions

class bookserializers(ModelSerializer):
    class Meta:
        model=book
        fields='__all__'

class loginserializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        username=data.get('username')
        password=data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                data['user']=user
            else:
                msg='wrong username or password'
                raise exceptions.ValidationError(msg)
        else:
            msg='provide username and password'
            raise exceptions.ValidationError(msg)
        return data
