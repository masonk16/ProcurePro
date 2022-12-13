from rest_framework import serializers
from core.models import Tender


class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'category', 'description', 'budget', 'opening_date', 'deadline']