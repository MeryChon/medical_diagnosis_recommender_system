from aggregations.models import AggregationType
from aggregations.utils.factory import aggregation_handler_factory
from dempster_shafer_structure.models import FocalElement
from dempster_shafer_structure.utils.dsbs import DSBSHandler
from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN
from utility_matrix.utils.utility_collections import UtilityCollectionsMatrixGenerator


class DiscriminationAnalysisDSBSHandler(DSBSHandler):
    def __init__(self, *args, **kwargs):
        super(DiscriminationAnalysisDSBSHandler, self).__init__(*args, **kwargs)
        self.focal_elements_map = self._prepare_focal_elements_map()

    @staticmethod
    def _prepare_focal_elements_map():
        all_focal_elements = FocalElement.objects.all()
        return {str(fe.name): fe for fe in all_focal_elements}

    def calculate_utility_collections_matrices(self):
        generator = UtilityCollectionsMatrixGenerator(self.initial_utility_matrix_json)
        self.initial_utility_collections_matrix = generator.generate(for_qrofn_matrix=False)

    def aggregate_collections(self, aggregation_type):
        aggregation_class = aggregation_handler_factory(AggregationType.discrimination_analysis)
        return aggregation_class(self.initial_utility_collections_matrix,
                                 self.focal_element_weight_vectors).aggregate()

    def calculate_generalized_expected_value(self, aggregated_values_matrix):
        for alternative_id, aggregated_collections in aggregated_values_matrix.items():
            gev_m = 0
            gev_n = 0
            for focal_element_key, aggregated_value in aggregated_collections.items():
                bpa = float(self.focal_elements_map[focal_element_key].bpa)
                gev_m += bpa * aggregated_value.get('weighted_positive_discrimination')
                gev_n += bpa * aggregated_value.get('weighted_negative_discrimination')

            generalized_expected_value = QROFN(gev_m, gev_n)
            self.generalized_expected_values[alternative_id] = generalized_expected_value

        self.set_ordered_alternatives()
        self.set_optimal_alternative()
        return self.generalized_expected_values
