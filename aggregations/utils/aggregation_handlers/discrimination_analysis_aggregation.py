from aggregations.utils.aggregation_handlers.abstract import AbstractAggregator


class QRungFuzzyDiscriminationAnalysisAggregator(AbstractAggregator):
    def aggregate(self):
        result = {}
        # TODO
        for alternative_key, focal_collections in self.utility_collections_matrix.items():
            for focal_elem_key, collection in focal_collections.items():
                pass

        return result
