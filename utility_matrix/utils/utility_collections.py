from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN


class UtilityCollectionsMatrixGenerator(object):
    utility_matrix = None
    utility_collections_matrix = None
    focal_elements = None

    def __init__(self, utility_matrix_json, focal_elements):
        self.utility_matrix = utility_matrix_json
        self.focal_elements = focal_elements

    def generate(self):
        utility_collections_matrix = {}
        for alternative_key, states_data in self.utility_matrix.items():
            alternative_collection = {}
            for focal_element_key, focal_element_data in self.focal_elements.items():
                states = focal_element_data.get("symptoms")
                for state_key in states:
                    qrofn_dict = self.utility_matrix[alternative_key][state_key]
                    alternative_collection.setdefault(focal_element_key, []).append(
                        QROFN(m=qrofn_dict.get('m'), n=qrofn_dict.get('n'), q=qrofn_dict.get('q')))
            utility_collections_matrix[alternative_key] = alternative_collection

        return utility_collections_matrix
