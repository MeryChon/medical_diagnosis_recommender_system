from aggregations.utils.aggregation_handlers.abstract import AbstractAggregator
from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN


class QRungFuzzyOrderedWeightedAverage(AbstractAggregator):
    def aggregate(self):
        result = {}
        for alternative_key, focal_collections in self.utility_collections_matrix.items():
            for focal_elem_key, collection in focal_collections.items():
                aggregated_payoff = QROFN()
                weight_vector = list(self.weight_vectors.get(focal_elem_key).values())
                collection.sort(key=lambda x: x.get('value'))
                for i, item in enumerate(collection):
                    weight = weight_vector[i]
                    product = item.get('value').multiply_by_const(weight)
                    aggregated_payoff += product
                result.setdefault(alternative_key, {})[focal_elem_key] = aggregated_payoff

        return result
