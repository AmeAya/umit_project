from rest_framework import serializers
from .models import *


class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = ('id', 'name', 'duration', 'price')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({'author': instance.author.name})
        return representation


def getInfoSerializer(obj: dict, user_type: str) -> dict:
    data = {
        'bin': obj['bin'],
        'name': obj['name'],
        'registered_date': obj['registerDate']
    }
    if user_type == 'company':
        data.update({'address': obj['katoAddress']})
    return data


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name')


class SubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name')
