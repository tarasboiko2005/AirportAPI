from rest_framework import serializers
from .models import RoadmapRequest, RoadmapResult

class RoadmapInputSerializer(serializers.Serializer):
    topic = serializers.CharField()

class RoadmapRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapRequest
        fields = ["id", "user", "topic", "created_at"]

class RoadmapResultSerializer(serializers.ModelSerializer):
    request = RoadmapRequestSerializer()

    class Meta:
        model = RoadmapResult
        fields = ["id", "request", "response_json", "created_at"]