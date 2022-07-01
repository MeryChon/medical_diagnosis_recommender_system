class OrderedAlternativeSerializer:
    data = None
    many = False

    def __init__(self, data=None, many=False):
        self.data = data
        self.many = many

    def to_representation(self, data=None):
        data = data or self.data
        if self.many:
            representation = []
            for datum in data:
                representation.append(self.alternative_to_dict(datum))
        else:
            representation = self.alternative_to_dict(data)

        return representation

    def alternative_to_dict(self, alternative):
        qrofn = alternative.get("value")
        return {
            "alternative": alternative.get("alternative"),
            "value": {
                "m": qrofn.m,
                "n": qrofn.n,
                "q": qrofn.q,
                "accuracy": qrofn.accuracy,
                "score": qrofn.score
            }
        }
