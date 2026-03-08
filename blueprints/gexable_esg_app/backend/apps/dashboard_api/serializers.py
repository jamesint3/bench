from rest_framework import serializers


class DashboardFilterSerializer(serializers.Serializer):
    period = serializers.CharField(required=False)
    site = serializers.CharField(required=False)


class EmissionsOverviewSerializer(serializers.Serializer):
    filters = DashboardFilterSerializer()
    summary = serializers.DictField(child=serializers.FloatField())
    trend = serializers.ListField(child=serializers.DictField())
    breakdown = serializers.ListField(child=serializers.DictField())
