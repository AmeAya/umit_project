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


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name')


class SubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsection
        fields = ('id', 'name')
