from rest_framework import serializers
from .models import Events 
from .models import PrivetInformation
from django.contrib.auth.models import User 
 
 
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class UserInformationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = PrivetInformation
        fields= '__all__'


    def create(self, validated_data):
        return PrivetInformation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.age = validated_data.get('age', instance.age)
        instance.email = validated_data.get('email', instance.email)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.postalcode = validated_data.get('postalcode', instance.postalcode)
        return instance
