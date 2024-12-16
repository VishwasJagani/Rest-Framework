from rest_framework import serializers
from home.models import *
from django.contrib.auth.models import *


# Custom Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username Already Taken")

        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email Already Taken")

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

    def validate_color(self, data):
        if data['color_name'] == "":
            raise serializers.ValidationError("Please Add Color")


class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()  # To display color name
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = person
        # To pass Only specific field
        # fields = ['name', 'age']
        # To pass all the fields use below
        fields = '__all__'
        # To exclude fields use below
        # exclude = ['name','age']

        # It is used to display ForeignKey data from ForeignKey table
        # depth = 1

    # To pass extra data without adding field in model

    def get_color_info(self, obj):
        print(obj)
        color_obj = Color.objects.get(id=obj.color.id)
        return {'Color_Name': color_obj.color_name, "HEX_Code": '#000'}

    # To Validate name and age field
    def validate(self, data):
        print(data)
        specialchar = '!@#$%^&*()_-+=?,.<>~`'
        if any(c in specialchar for c in data['name']):
            raise serializers.ValidationError("Special Char Not Allowed")

        if data['age'] < 18:
            raise serializers.ValidationError("Age Should Be greater Than 18")

        return data
