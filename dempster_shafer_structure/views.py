from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from aggregations.models import AggregationType
from dempster_shafer_structure.utils.dsbs import DSBSHandler
from utility_matrix.serializers import UtilityMatrixDataSerializer

DIAGNOSES = [
    {
        "index": 0,
        "name": "Depression"
    },
    {
        "index": 1,
        "name": "Bipolar Disorder"
    },
    {
        "index": 2,
        "name": "Autism Spectrum"
    }
]

SYMPTOMS = [
    {
        "index": 0,
        "name": "Irritability"
    },
    {
        "index": 1,
        "name": "Lack of Appetite"
    },
    {
        "index": 2,
        "name": "Difficulty Moving"
    },
    {
        "index": 3,
        "name": "Visual Hallucinations"
    },
    {
        "index": 4,
        "name": "Auditory Hallucinations"
    }
]

FOCAL_ELEMENTS = {
    "B1": {
        "symptoms": ["Irritability", "Lack of Appetite"],
        "bpa": 0.1
    },
    "B2": {
        "symptoms": ["Irritability", "Lack of Appetite", "Visual Hallucinations"],
        "bpa": 0.2
    },
    "B3": {
        "symptoms": ["Lack of Appetite", "Difficulty Moving"],
        "bpa": 0.4
    },
    "B4": {
        "symptoms": ["Difficulty Moving", "Visual Hallucinations"],
        "bpa": 0.05
    },
    "B5": {
        "symptoms": ["Difficulty Moving", "Visual Hallucinations", "Auditory Hallucinations"],
        "bpa": 0.25
    }
}


@api_view(['GET'])
def get_dempster_shafer_structure_data(request):
    data = {
        'diagnoses': DIAGNOSES,
        'symptoms': SYMPTOMS,
        'focal_elements': FOCAL_ELEMENTS
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
    utility_matrix = serializer.save()

    dsbs_handler = DSBSHandler(utility_matrix_data=utility_matrix,
                               focal_elements=FOCAL_ELEMENTS)

    results = {}
    for aggregation_type in AggregationType.choices:
        dsbs_handler.run(aggregation_type)
        results[aggregation_type] = {
            "ordered_alternatives": dsbs_handler.ordered_alternatives,
            "optimal_alternative": dsbs_handler.optimal_alternative
        }

    return Response(status=200, data={"results": results})
