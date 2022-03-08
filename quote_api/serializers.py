# data from django and serialize for rest framwork to digest and share w other apps
from rest_framework import serializers
from .models import Quote
from django.contrib.auth.models import User

class QuoteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=False, input_formats=['d/m/y'])
    updated_at = serializers.DateTimeField(required=False, input_formats=['d/m/y'])

    class Meta:
        model = Quote
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        #not showing password when requests made
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
