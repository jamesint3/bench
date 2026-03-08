from rest_framework import serializers

from .models import EmissionFactor, EmissionRecord


class EmissionFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionFactor
        fields = [
            "id",
            "tenant_id",
            "factor_code",
            "region",
            "unit_from",
            "unit_to",
            "factor_value",
            "valid_from",
            "valid_to",
            "version",
        ]


class EmissionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionRecord
        fields = [
            "id",
            "tenant_id",
            "source",
            "factor",
            "activity_date",
            "activity_amount",
            "activity_unit",
            "emissions_tco2e",
        ]
        read_only_fields = ["emissions_tco2e"]


class EmissionCalculationSerializer(serializers.Serializer):
    tenant_id = serializers.UUIDField()
    source_id = serializers.IntegerField()
    factor_id = serializers.IntegerField()
    activity_date = serializers.DateField()
    activity_amount = serializers.DecimalField(max_digits=18, decimal_places=6)
    activity_unit = serializers.CharField(max_length=30)
