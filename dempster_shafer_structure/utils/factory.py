from aggregations.models import AggregationType
from dempster_shafer_structure.utils.disctimination_analysis_dsbs import DiscriminationAnalysisDSBSHandler
from dempster_shafer_structure.utils.dsbs import DSBSHandler


class DSBSSingletonFactory:
    general_dsbs_handler = None
    discrimination_analysis_dsbs_handler = None

    @classmethod
    def get_dsbs_handler(cls, aggregation_type, *args, **kwargs):
        if aggregation_type == AggregationType.discrimination_analysis:
            if not cls.discrimination_analysis_dsbs_handler:
                cls.discrimination_analysis_dsbs_handler = DiscriminationAnalysisDSBSHandler(*args, **kwargs)
            handler = cls.discrimination_analysis_dsbs_handler
        else:
            if not cls.general_dsbs_handler:
                cls.general_dsbs_handler = DSBSHandler(*args, **kwargs)

            handler = cls.general_dsbs_handler

        return handler
