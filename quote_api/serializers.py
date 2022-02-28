# data from django and serialize for rest framwork to digest and share w other apps
from rest_framework import serializers
from .models import Quote

class QuoteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Quote
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
