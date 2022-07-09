from dempster_shafer_structure.models import FocalElement
from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN


class UtilityCollectionsMatrixGenerator(object):
    utility_matrix = None
    utility_collections_matrix = None
    focal_elements = None
    focal_elements_name_map = None

    def __init__(self, utility_matrix_json):
        self.utility_matrix = utility_matrix_json
        self._set_focal_elements()

    def generate(self, for_qrofn_matrix=True):
        utility_collections_matrix = {}
        for alternative_key, states_data in self.utility_matrix.items():
            alternative_collection = {}
            for focal_element_key, focal_element_model in self.focal_elements_name_map.items():
                symptoms = focal_element_model.symptoms.all()
                for symptom in symptoms:
                    symptom_id = str(symptom.id)
                    utility_value = self.utility_matrix[alternative_key][symptom_id]
                    if for_qrofn_matrix:
                        utility_value = QROFN(
                            m=utility_value.get('m'),
                            n=utility_value.get('n'),
                            q=utility_value.get('q')
                        )
                    alternative_collection.setdefault(focal_element_key, []).append({
                        'id': symptom_id,
                        'value': utility_value
                    })
            utility_collections_matrix[alternative_key] = alternative_collection

        return utility_collections_matrix

    def _set_focal_elements(self):
        focal_element_models = FocalElement.objects.prefetch_related('symptoms').all()
        self.focal_elements = focal_element_models
        self.focal_elements_name_map = {fem.name: fem for fem in focal_element_models}
