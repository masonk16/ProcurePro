from rest_framework import serializers
from core.models import Tenders


class TendersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenders
        fields = ['id', 'category', 'description', 'budget', 'opening_date', 'deadline']