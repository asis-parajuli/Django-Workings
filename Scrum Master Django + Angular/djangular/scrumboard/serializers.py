from rest_framework import serializers

from .models import List, Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Card


class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(read_only=True, many=True)
    class Meta:
        fields = '__all__'
        model = List