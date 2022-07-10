from rest_framework import serializers

from dempster_shafer_structure.models import Diagnose, Symptom, FocalElement


class DiagnoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnose
        fields = ('id', 'name')


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ('id', 'name', 'position')


class FocalElementSerializer(serializers.ModelSerializer):
    symptoms_with_weights = serializers.SerializerMethodField()

    class Meta:
        model = FocalElement
        fields = ('id', 'name', 'symptoms_with_weights', 'bpa')

    def get_symptoms_with_weights(self, instance):
        focal_element_symptom_weights = instance.symptom_weights.all()
        symptom_serializer = SymptomSerializer()
        serialized_data = []
        for fesw in focal_element_symptom_weights:
            symptom = fesw.symptom
            serialized_symptom = symptom_serializer.to_representation(symptom)
            serialized_symptom['weight'] = fesw.weight
            serialized_data.append(serialized_symptom)

        return serialized_data
