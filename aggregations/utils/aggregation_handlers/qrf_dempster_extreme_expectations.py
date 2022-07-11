from aggregations.utils.aggregation_handlers.abstract import AbstractAggregator


class QRungFuzzyDempstersExtremeExpectations(AbstractAggregator):
    def aggregate(self):
        result = {}
        for alternative_key, focal_collections in self.utility_collections_matrix.items():
            result[alternative_key] = {}
            for focal_elem_id, collection in focal_collections.items():
                min_expected_value = self.get_minimum_expected_value(collection).get('value')
                max_expected_value = self.get_maximum_expected_value(collection).get('value')
                result[alternative_key][focal_elem_id] = (min_expected_value + max_expected_value).multiply_by_const(
                    0.5)

        return result

    @staticmethod
    def get_minimum_expected_value(collection):
        sorted_collection = sorted(collection, key=lambda x: x.get('value'))
        return sorted_collection[0]

    @staticmethod
    def get_maximum_expected_value(collection):
        sorted_collection = sorted(collection, key=lambda x: x.get('value'), reverse=True)
        return sorted_collection[0]
