from rest_framework import serializers
from core.models import *


class UserSerializer(serializers.ModelSerializer):
    tenders = serializers.PrimaryKeyRelatedField(many=True, queryset=Tender.objects.all())
    bids = serializers.PrimaryKeyRelatedField(many=True, queryset=Bids.objects.all())

    class Meta:
        model = User
        fields = "__all__"


class TenderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Tender
        fields = ['id', 'category', 'notice_number', 'tender_name', 'requirement_details', 'budget', 'opening_date', 'deadline', 'owner']
        lookup_field = ['id', 'owner', 'category', 'tender_name']

    def create(self, validated_data):
        return Tender.objects.create(**validated_data)


class BidSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Bids
        fields = ['id', 'description', 'bid_price', 'submission_date', 'tender_id', 'owner']
        lookup_field = ['id', 'owner', 'tender_id']

    def create(self, validated_data):
        return Bids.objects.create(**validated_data)
