from django.db.models import Sum

from aggregations.utils.aggregation_handlers.abstract import AbstractAggregator
from dempster_shafer_structure.models import FocalElement
from utility_matrix.utils.utility_matrix_generators import DiscriminationAnalysisHandler


class QRungFuzzyDiscriminationAnalysisAggregator(AbstractAggregator):
    def __init__(self, *args, **kwargs):
        super(QRungFuzzyDiscriminationAnalysisAggregator, self).__init__(*args, **kwargs)
        self.discrimination_analysis_handler = DiscriminationAnalysisHandler()
        self.focal_element_symptom_weights_map = self._prepare_focal_element_symptom_weights_map()

    def aggregate(self):
        result = {}

        for alternative_id, focal_collections in self.utility_collections_matrix.items():
            result[alternative_id] = {}
            aggregated_positive_discrimination = 0
            aggregated_negative_discrimination = 0
            for focal_elem_key, collection in focal_collections.items():
                aggregated_positive_discrimination += self._calculate_weighted_positive_discrimination_sum(
                    focal_elem_key,
                    collection
                )
                aggregated_negative_discrimination += self._calculate_weighted_negative_discrimination(
                    focal_elem_key,
                    collection
                )
                result[alternative_id][focal_elem_key] = {
                    'weighted_positive_discrimination': aggregated_positive_discrimination,
                    'weighted_negative_discrimination': aggregated_negative_discrimination
                }

        return result

    @staticmethod
    def _prepare_focal_element_symptom_weights_map():
        """
        Returns focal elements to normalized symptom weights two-level-deep dict
        """
        result = {}

        focal_elements = FocalElement.objects.prefetch_related('symptom_weights').all()
        for focal_elem in focal_elements:
            symptom_weights = focal_elem.symptom_weights
            symptom_weights_sum = float(symptom_weights.aggregate(Sum('weight')).get('weight__sum'))

            symptom_weights_map = {}
            for sw in symptom_weights.all():
                symptom_weights_map[str(sw.symptom.id)] = float(sw.weight) / symptom_weights_sum

            result[focal_elem.name] = symptom_weights_map

        return result

    def _calculate_weighted_positive_discrimination_sum(self, focal_elem_key, collection):
        symptom_weights = self.focal_element_symptom_weights_map[focal_elem_key]
        collection_as_map = {i.get('id'): i.get('value') for i in collection}

        weight_sum = sum(symptom_weights.values())
        print(f"{focal_elem_key}: {weight_sum}")

        total = 0

        for index, item in collection_as_map.items():
            symptom_id = index
            weight = symptom_weights[symptom_id]
            positive_discrimination = self.discrimination_analysis_handler.calculate_positive_discrimination(
                index, collection_as_map)
            weighted_positive_discrimination = positive_discrimination * weight
            total += weighted_positive_discrimination

        return total

    def _calculate_weighted_negative_discrimination(self, focal_elem_key, collection):
        symptom_weights = self.focal_element_symptom_weights_map[focal_elem_key]
        collection_as_map = {i.get('id'): i.get('value') for i in collection}

        total = 0

        for index, item in collection_as_map.items():
            symptom_id = index
            weight = symptom_weights[symptom_id]
            positive_discrimination = self.discrimination_analysis_handler.calculate_negative_discrimination(
                index, collection_as_map, weight)
            total += positive_discrimination

        return total
