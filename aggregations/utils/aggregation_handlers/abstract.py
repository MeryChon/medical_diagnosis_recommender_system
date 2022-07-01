from abc import abstractmethod


class AbstractAggregator:
    utility_collections_matrix: dict
    weight_vectors: dict

    def __init__(self, utility_collections, weight_vectors=None):
        self.utility_collections_matrix = utility_collections
        if weight_vectors:
            self.weight_vectors = weight_vectors

    @abstractmethod
    def aggregate(self):
        pass
