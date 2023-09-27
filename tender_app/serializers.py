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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'user', 'name', 'bin', 'address', 'face', 'face_phone', 'favourites', 'requisites',
                  'license', 'gos_reg')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name')


class SubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsection
        fields = ('id', 'name')


class TenderFilterSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)
    city = serializers.StringRelatedField(many=False)
    types_of_work = serializers.StringRelatedField(many=True)
    class Meta:
        model = Tender
        fields = ('id', 'author', 'city', 'types_of_work', 'date', 'expire_date', 'budget')

        # def to_representation(self, instance):
        #     return {'author': instance.author.name, 'city': instance.city.name}


class WorkerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'name', 'bin', 'description', 'director', 'rating', 'cities', 'types_of_work')


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'name', 'bin', 'description', 'director', 'phone', 'rating', 'feedbacks', 'cities',
                  'types_of_work', 'docs')
