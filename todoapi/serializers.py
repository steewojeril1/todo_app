# from .models import Todo
from rest_framework import serializers
from .models import Todo

from django.contrib.auth import get_user_model

User = get_user_model() # this will return value in AUTH_USER_MODEL in settings

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # write only

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone', 'address']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)   # to hash the password use create_uer()


class TodoSerializer(serializers.Serializer):
    '''
    we dont give user field here.
    It’s a security risk — a user could submit a todo for another user by changing the user field.
    Instead, we always use the logged-in user from request.user.
    '''
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField()
    completed = serializers.BooleanField(default = True)
    created_at = serializers.DateTimeField(read_only = True)


    # ModelSerialwhen using a ModelSerializer, this would automatically save the instance to the database. 
    def create(self, validated_data):   # this is because we are passing user in serializer.save()
        user = self.context['user']  # access request.user
        return Todo.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        # For PUT/PATCH requests
        instance.title = validated_data.get('title', instance.title) # instance - existing data
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance
    


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(allow_blank=True)
    '''  
        required=False - By default, fields are required in serializers. Even if `null=True` is set in the model, you must specify `required=False` in the serializer to make the field optional.

        {}                     ✅ (phone is skipped)
        {"phone": "123456"}    ✅ (non-empty string)
        allow_blank=True - You can give an empty string ("") as its value without any validation error.
        {"phone": ""}          ✅ (empty string allowed)
        '''
    address = serializers.CharField(allow_blank=True)

    def update(self, instance, validated_data):
        # For PUT/PATCH requests
        instance.username = validated_data.get('username', instance.username) # instance - existing data
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
