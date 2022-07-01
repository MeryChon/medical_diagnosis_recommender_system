import json

from rest_framework import serializers

from utility_matrix.models import UtilityMatrixData
from utility_matrix.utils.utility_matrix_generators import QRungUtilityMatrixGenerator


class UtilityMatrixDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityMatrixData
        fields = (
            'id',
            'expert_user',
            'expert_raw_data_json',
            'discrimination_qrang_matrix_json',
            'matrix_rung',
        )

    def create(self, validated_data):
        expert_data = validated_data.get('expert_raw_data_json')

        generator = QRungUtilityMatrixGenerator(frequency_matrix=expert_data)
        discrimination_qrang_matrix_dataframe, max_rung = generator.get_orthopair_matrix()
        discrimination_qrang_matrix_json = json.loads(discrimination_qrang_matrix_dataframe.to_json(orient="index"))

        validated_data['discrimination_qrang_matrix_json'] = discrimination_qrang_matrix_json
        validated_data['matrix_rung'] = max_rung

        return super(UtilityMatrixDataSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        pass
