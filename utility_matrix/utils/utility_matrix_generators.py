from pandas import DataFrame

from utility_matrix.utils.fuzzy_numbers.qrofn import QROFN


class QRungUtilityMatrixGenerator:
    frequency_matrix = None  # type: DataFrame
    large_ratio_fn = None  # function
    matrix_rung = None

    def __init__(self, frequency_matrix, large_ratio_fn=None):
        self.frequency_matrix = frequency_matrix  # DataFrame.from_dict(frequency_matrix, orient="index")
        self.discrimination_analysis_handler = DiscriminationAnalysisHandler(large_ratio_fn)

    def get_orthopair_matrix(self):
        # TODO normalize values!!!
        data = {}
        for row_index, row in self.frequency_matrix.items():
            data[row_index] = {}
            for item_index, frequency in row.items():
                positive_discrimination = self.discrimination_analysis_handler.calculate_positive_discrimination(
                    item_index, row)
                negative_discrimination = self.discrimination_analysis_handler.calculate_negative_discrimination(
                    item_index, row)
                data[row_index][item_index] = QROFN(positive_discrimination, negative_discrimination)

        matrix_rung = self.calculate_rung(data)
        return data, matrix_rung

    @staticmethod
    def calculate_rung(orthopair_matrix):
        max_rung = 0
        for row_index, row in orthopair_matrix.items():
            for item_index, number in row.items():
                if number.q > max_rung:
                    max_rung = number.q

        return max_rung


class DiscriminationAnalysisHandler:
    large_ratio_fn = None

    def __init__(self, large_ratio_fn=None):
        if large_ratio_fn:
            self.large_ratio_fn = large_ratio_fn

    @classmethod
    def calculate_positive_discrimination(cls, current_index, row, weight=None):
        total = 0
        fixed_freq = row[current_index]
        for i, freq in row.items():
            if i == current_index:
                continue
            total += cls._get_large_ratio_function()(fixed_freq / row[i])

        if weight is not None:
            total = total * weight

        total = total / ((len(row) - 1) if len(row) > 1 else 1)  # FIXME ?

        return round(total, 2)

    @classmethod
    def calculate_negative_discrimination(cls, current_index, row, weight=None):
        total = 0
        fixed_freq = row[current_index]
        for i, freq in row.items():
            if i == current_index:
                continue
            total += cls._get_large_ratio_function()(row[i] / fixed_freq)

        if weight is not None:
            total = total * weight

        total = total / ((len(row) - 1) if len(row) > 1 else 1)  # FIXME ?

        return round(total, 2)

    @classmethod
    def _get_large_ratio_function(cls):
        return cls.large_ratio_fn or cls._default_large_ratio_function

    @staticmethod
    def _default_large_ratio_function(ratio):
        if ratio > 3:
            return 1

        if ratio < 0.1:
            return 0

        return round(0.34 * ratio - 0.034, 2)
