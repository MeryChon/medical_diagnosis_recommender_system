from pprint import pprint

from aggregations.models import AggregationType
from utility_matrix.models import UtilityMatrixData
from utility_matrix.utils.utility_collections import UtilityCollectionsMatrixGenerator


class DSBSHandler:
    utility_matrix_json = None
    focal_elements = None
    aggregated_values = None
    general_expected_values = None
    ordered_alternatives = None
    optimal_alternative = None

    def __init__(self, utility_matrix_data: UtilityMatrixData, focal_elements):
        self.utility_matrix_json = utility_matrix_data.discrimination_qrang_matrix_json
        self.focal_elements = focal_elements
        self.utility_collections_matrix = self._calculate_utility_collections_matrix()

    def run(self, aggregation_method: AggregationType):
        print(f"============== Running For {aggregation_method} ==============")
        aggregated_data = self.aggregate_collections(aggregation_method)
        pprint(aggregated_data)
        generalized_expected_value = self.calculate_generalized_expected_value(aggregated_data)
        pprint(generalized_expected_value)

    def _calculate_utility_collections_matrix(self):
        generator = UtilityCollectionsMatrixGenerator(self.utility_matrix_json, self.focal_elements)
        return generator.generate()

    def aggregate_collections(self, aggregation_method):
        return {}

    def calculate_generalized_expected_value(self, aggregated_values_matrix):
        return {}

    def set_ordered_alternatives(self):
        pass

    def set_optimal_alternative(self):
        pass
