from rest_framework import serializers
from datetime import datetime
from chatbot.models import ( StarRatings)

class StarRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = StarRatings
        fields = '__all__'
