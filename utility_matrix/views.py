import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from utility_matrix.models import UtilityMatrixData
from utility_matrix.serializers import UtilityMatrixDataSerializer
from utility_matrix.utils.utility_matrix_generators import QRungUtilityMatrixGenerator


@api_view(['POST'])
def generate_discrimination_qrung_matrix(request):
    expert_data = request.data.get('expert_data')
    runner = QRungUtilityMatrixGenerator(expert_data)
    orthopair_matrix = runner.get_orthopair_matrix()
    orthopair_matrix_json = json.loads(orthopair_matrix.to_json(orient="index"))

    serializer = UtilityMatrixDataSerializer(data={
        'expert_user': request.user.pk,
        'expert_raw_data_json': expert_data,
        'discrimination_qrang_matrix_json': orthopair_matrix_json
    })
    print(orthopair_matrix)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(status=200, data=serializer.data)
