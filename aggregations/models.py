from django.db import models

from utility_matrix.models import UtilityMatrixData


class AggregationType(models.TextChoices):
    weighted_average = "weighted_average"
    ordered_weighted_average = "ordered_weighted_average"
    dempster_extreme_expectations = "dempster_extreme_expectations"
    choquet_integral = "choquet_integral"
    discrimination_analysis = "discrimination_analysis"


class Aggregation(models.Model):
    utility_matrix_data = models.ForeignKey(UtilityMatrixData, on_delete=models.CASCADE, related_name='aggregations')
    aggregation_type = models.CharField(choices=AggregationType.choices, max_length=64)
    aggregated_data_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aggregations'
