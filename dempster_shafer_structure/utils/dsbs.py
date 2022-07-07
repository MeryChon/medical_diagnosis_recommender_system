from pprint import pprint

from aggregations.models import AggregationType
from aggregations.utils.factory import aggregation_handler_factory
from utility_matrix.models import UtilityMatrixData
from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN
from utility_matrix.utils.utility_collections import UtilityCollectionsMatrixGenerator


class DSBSHandler:
    utility_matrix_json = None
    focal_elements = None
    aggregated_values = None
    generalized_expected_values = None
    focal_element_weight_vectors = None
    ordered_alternatives = None
    optimal_alternative = None

    def __init__(self, utility_matrix_data: UtilityMatrixData, focal_elements, focal_element_weight_vectors=None):
        self.utility_matrix_json = utility_matrix_data.discrimination_qrang_matrix_json
        self.focal_elements = focal_elements
        self.focal_element_weight_vectors = focal_element_weight_vectors
        self.generalized_expected_values = {}
        self.utility_collections_matrix = self._calculate_utility_collections_matrix()

    def run(self, aggregation_method: AggregationType):
        print(f"============== Running For {aggregation_method} ==============")
        aggregated_data = self.aggregate_collections(aggregation_method)
        pprint(aggregated_data)
        generalized_expected_value = self.calculate_generalized_expected_value(aggregated_data)
        pprint(generalized_expected_value)

    def _calculate_utility_collections_matrix(self):
        generator = UtilityCollectionsMatrixGenerator(self.utility_matrix_json)
        return generator.generate()

    def aggregate_collections(self, aggregation_type):
        aggregation_class = aggregation_handler_factory(aggregation_type)
        if not aggregation_class:
            raise Exception("Aggregation class not found")
        return aggregation_class(self.utility_collections_matrix, self.focal_element_weight_vectors).aggregate()

    def calculate_generalized_expected_value(self, aggregated_values_matrix):
        for alternative_key, focal_elem_aggregated_payoffs in aggregated_values_matrix.items():
            expected_value = QROFN()
            for focal_elem, aggregated_payoff in focal_elem_aggregated_payoffs.items():
                expected_value += aggregated_payoff.multiply_by_const(self.focal_elements.get(focal_elem).get("bpa"))
            self.generalized_expected_values[alternative_key] = expected_value
        pprint(self.generalized_expected_values)
        self.set_ordered_alternatives()
        self.set_optimal_alternative()
        return self.generalized_expected_values

    def set_ordered_alternatives(self):
        generalized_expected_values_list = list()
        for alternative, value in self.generalized_expected_values.items():
            generalized_expected_values_list.append({
                "alternative": alternative,
                "value": value
            })

        self.ordered_alternatives = sorted(generalized_expected_values_list,
                                           key=lambda alt: alt.get('value'),
                                           reverse=True)
        print(f"=========== ORDERED ALTERNATIVES ===========")
        for alt in self.ordered_alternatives:
            print(f"{alt.get('alternative')}: {str(alt.get('value'))}")

    def set_optimal_alternative(self):
        self.optimal_alternative = self.ordered_alternatives[0]
