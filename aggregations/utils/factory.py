from aggregations.models import AggregationType
from aggregations.utils.aggregation_handlers.fuzzy_choquet_integral import FuzzyChoquetIntegralAggregator
from aggregations.utils.aggregation_handlers.qrf_dempster_extreme_expectations import \
    QRungFuzzyDempstersExtremeExpectations
from aggregations.utils.aggregation_handlers.qrfowa import QRungFuzzyOrderedWeightedAverage
from aggregations.utils.aggregation_handlers.qrfwa import QRungFuzzyWeightedAverage


def aggregation_handler_factory(aggregation_type):
    aggregator = None

    if aggregation_type == AggregationType.weighted_average:
        aggregator = QRungFuzzyWeightedAverage
    elif aggregation_type == AggregationType.ordered_weighted_average:
        aggregator = QRungFuzzyOrderedWeightedAverage
    elif aggregation_type == AggregationType.dempster_extreme_expectations:
        aggregator = QRungFuzzyDempstersExtremeExpectations
    elif aggregation_type == AggregationType.choquet_integral:
        aggregator = FuzzyChoquetIntegralAggregator
    elif aggregation_type == AggregationType.discrimination_analysis:
        pass

    if not aggregator:
        raise Exception("Unknown aggregation type")

    return aggregator
