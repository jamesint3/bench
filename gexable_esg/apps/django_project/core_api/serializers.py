from rest_framework import serializers


class ActivityRecordInSerializer(serializers.Serializer):
    site_id = serializers.CharField()
    quantity = serializers.FloatField(min_value=0.0001)
    unit = serializers.CharField(required=False, default="kWh")
    source_type = serializers.CharField(required=False, default="manual_upload")


class EmissionsCalculateInSerializer(serializers.Serializer):
    activity_record_id = serializers.CharField(required=False)
    quantity = serializers.FloatField(min_value=0.0001)
    scope = serializers.CharField(required=False, default="scope2")
    factor = serializers.FloatField(required=False)
    calculation_method_version = serializers.CharField(required=False, default="v1")
    factor_version = serializers.CharField(required=False, default="v1")


class DisclosurePublishInSerializer(serializers.Serializer):
    framework = serializers.ChoiceField(choices=["CSRD", "ISSB", "GRI", "CDP", "SEC"], required=False, default="CSRD")
    period = serializers.CharField(required=False, default="2026-Q1")
