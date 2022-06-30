from rest_framework import serializers

from utility_matrix.models import UtilityMatrixData


class UtilityMatrixDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityMatrixData
        fields = (
            'id',
            'expert_user',
            'expert_raw_data_json',
            'discrimination_qrang_matrix_json'
        )
