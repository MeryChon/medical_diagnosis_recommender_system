from abc import abstractmethod


class AbstractAggregator:
    utility_collections_matrix: dict

    def __init__(self, utility_collections):
        self.utility_collections_matrix = utility_collections

    @abstractmethod
    def aggregate(self):
        pass
