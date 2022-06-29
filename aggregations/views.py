from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def generate_discrimination_qrung_matrix(request):
    print(request.query_params)
    expert_data = request.query_params.get('expert_data')

    return Response(status=200, data=expert_data)
