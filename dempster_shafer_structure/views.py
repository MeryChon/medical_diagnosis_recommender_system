from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from aggregations.models import AggregationType
from dempster_shafer_structure.models import Diagnose, Symptom, FocalElement
from dempster_shafer_structure.serializers import DiagnoseSerializer, SymptomSerializer, FocalElementSerializer
from dempster_shafer_structure.utils.factory import DSBSSingletonFactory
from utility_matrix.models import UtilityMatrixData
from utility_matrix.serializers import UtilityMatrixDataSerializer
from utility_matrix.utils.fuzzy_numbers.serializers import OrderedAlternativeSerializer


class DempsterShaferBeliefStructureDataViewSet(APIView):
    def get(self, request):
        diagnoses = Diagnose.objects.all()
        serialized_diagnoses = DiagnoseSerializer(many=True).to_representation(diagnoses)

        symptoms = Symptom.objects.all()
        serialized_symptoms = SymptomSerializer(many=True).to_representation(symptoms)

        focal_elements = FocalElement.objects.all()
        serialized_focal_elements = FocalElementSerializer(many=True).to_representation(focal_elements)

        data = {
            'diagnoses': serialized_diagnoses,
            'symptoms': serialized_symptoms,
            'focal_elements': serialized_focal_elements
        }

        return Response(status=200, data=data)


@api_view(['POST'])
def run_decision_making_process(request):
    expert_data = request.data.get('expert_data')

    if not expert_data:
        raise ValidationError({
            "non_field_errors": ["Expert data is required"]
        })

    serializer = UtilityMatrixDataSerializer(data={
        'expert_raw_data_json': expert_data,
        'expert_user': request.user.pk
    })
    serializer.is_valid(raise_exception=True)
    utility_matrix = serializer.save()  # type: UtilityMatrixData

    focal_elements = FocalElementSerializer(many=True).to_representation(FocalElement.objects.all())
    focal_elements_map = {fe.get('name'): fe for fe in focal_elements}
    weight_vectors = {}
    for fe in focal_elements:
        weight_vectors[fe.get('name')] = {str(s.get('id')): s.get('weight') for s in fe.get('symptoms')}

    results = {}
    for aggregation_type in AggregationType.choices:
        aggregation_type = aggregation_type[0]
        dsbs_handler = DSBSSingletonFactory.get_dsbs_handler(
            aggregation_type,
            utility_matrix_data=utility_matrix,
            focal_elements=focal_elements_map,
            focal_element_weight_vectors=weight_vectors
        )
        dsbs_handler.run(aggregation_type)
        results[aggregation_type] = {
            "ordered_alternatives": OrderedAlternativeSerializer(dsbs_handler.ordered_alternatives,
                                                                 many=True).to_representation(),
            "optimal_alternative": OrderedAlternativeSerializer(dsbs_handler.optimal_alternative).to_representation()
        }

    return Response(status=200, data={"results": results})
