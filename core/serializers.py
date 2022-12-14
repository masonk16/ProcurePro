from rest_framework import serializers
from core.models import Tender
from django.contrib.auth.models import User


class TenderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tender
        fields = ['url', 'id', 'category', 'description', 'budget', 'opening_date', 'deadline', 'owner']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tenders = serializers.HyperlinkedRelatedField(many=True, view_name='tender-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'tenders']
