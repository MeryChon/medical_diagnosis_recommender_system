from aggregations.utils.aggregation_handlers.abstract import AbstractAggregator
from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN


class QRungFuzzyOrderedWeightedAverage(AbstractAggregator):
    def aggregate(self):
        result = {}
        for alternative_key, focal_collections in self.utility_collections_matrix.items():
            for focal_elem_key, collection in focal_collections.items():
                aggregated_payoff = QROFN()
                weight_vector = self.weight_vectors.get(focal_elem_key)
                collection.sort(key=lambda x: x.get('value'))
                for index, weight in enumerate(weight_vector):
                    product = collection[index].get('value').multiply_by_const(weight)
                    aggregated_payoff += product
                result.setdefault(alternative_key, {})[focal_elem_key] = aggregated_payoff

        return result
