from rest_framework import serializers
from core.models import *


class TenderSerializer(serializers.HyperlinkedModelSerializer):
    contractor = serializers.ReadOnlyField(source='contractor.email')
    bids = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='bid-detail'
    )

    class Meta:
        model = Tender
        fields = ['url', 'id', 'category', 'description', 'budget', 'opening_date', 'deadline', 'contractor', 'bids']


class BidSerializer(serializers.HyperlinkedModelSerializer):
    supplier = serializers.ReadOnlyField(source='supplier.email')
    tender_id = serializers.HyperlinkedRelatedField(many=True, view_name='tender-detail', read_only=True)

    class Meta:
        model = Bids
        fields = ['url', 'id', 'description', 'bid_price', 'submission_date', 'tender_id', 'supplier']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
