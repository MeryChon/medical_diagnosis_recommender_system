import math
import random

from aggregations.utils.aggregation_handlers.abstract import AbstractAggregator
from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN


class FuzzyChoquetIntegralAggregator(AbstractAggregator):
    def aggregate(self):
        result = {}
        for alternative_key, focal_collections in self.utility_collections_matrix.items():
            for focal_elem_key, collection in focal_collections.items():
                collection.sort()
                result.setdefault(alternative_key, {})[focal_elem_key] = self._calculate_choquet_integral(collection)

        return result

    def _calculate_choquet_integral(self, collection):
        """
        :param collection: ordered collection of utilities associated to the focal element
        """
        result = QROFN()
        for i in range(0, len(collection)):
            result += collection[i].multiply_by_const(
                self._calculate_associated_probability(collection, i))

        return result

    def _calculate_associated_probability(self, collection: list, index: int):
        if index == 0:
            associated_probability = self._calculate_fuzzy_measure([collection[0]])
        else:
            # TODO pass list of symptoms instead of their utility values
            associated_probability = self._calculate_fuzzy_measure(
                [collection[:index]]) - self._calculate_fuzzy_measure(collection[:index - 1])

        return math.fabs(associated_probability)

    def _calculate_fuzzy_measure(self, symptom_set):
        # TODO calculate fuzzy measure instead of hard-coding it
        # tmp = {
        #     ["Irritability", "Lack of Appetite", "Difficulty Moving", "Visual Hallucinations",
        #      "Auditory Hallucinations"]: 1,
        #     []: 0
        # }

        return random.uniform(0, 1)
