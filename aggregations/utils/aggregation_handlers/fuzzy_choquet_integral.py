import math

from aggregations.utils.aggregation_handlers.abstract import AbstractAggregator
from dempster_shafer_structure.models import FocalElement
from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN


class FuzzyChoquetIntegralAggregator(AbstractAggregator):
    def aggregate(self):
        result = {}
        for alternative_key, focal_collections in self.utility_collections_matrix.items():
            for focal_elem_key, collection in focal_collections.items():
                collection.sort(key=lambda x: x.get('value'))
                result.setdefault(alternative_key, {})[focal_elem_key] = self._calculate_choquet_integral(collection)

        return result

    def _calculate_choquet_integral(self, collection):
        """
        :param collection: ordered collection of utilities associated to the focal element
        """
        result = QROFN()
        for i in range(0, len(collection)):
            result += collection[i].get('value').multiply_by_const(
                self._calculate_associated_probability(collection, i))

        return result

    def _calculate_associated_probability(self, collection: list, index: int):
        if index == 0:
            associated_probability = self._calculate_fuzzy_measure([collection[0]])
        else:
            associated_probability = self._calculate_fuzzy_measure(
                collection[:index]) - self._calculate_fuzzy_measure(collection[:index - 1])

        return math.fabs(associated_probability)

    @staticmethod
    def _calculate_fuzzy_measure(symptoms_subset):
        """
        We'll use belief measure as a fuzzy measure
        """
        result = 0

        current_subset_symptoms = [s.get('id') for s in symptoms_subset]
        all_focal_elements = FocalElement.objects.all()

        for focal_element in all_focal_elements:
            fe_symptoms = focal_element.symptoms.all()
            for fe_symptom in fe_symptoms:
                if str(fe_symptom.id) in current_subset_symptoms:
                    result += focal_element.bpa
                    break

        return result
