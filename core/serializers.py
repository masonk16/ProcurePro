from rest_framework import serializers
from core.models import Tender
from django.contrib.auth.models import User


class TenderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tender
        fields = ['id', 'category', 'description', 'budget', 'opening_date', 'deadline', 'owner']


class UserSerializer(serializers.ModelSerializer):
    tenders = serializers.PrimaryKeyRelatedField(many=True, queryset=Tender.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tenders']
