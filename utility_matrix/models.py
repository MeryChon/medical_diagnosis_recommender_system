from django.contrib.auth.models import User
from django.db import models


class UtilityMatrixData(models.Model):
    expert_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="utility_matrices")
    expert_raw_data_json = models.JSONField(null=False)
    discrimination_qrang_matrix_json = models.JSONField(null=True, blank=True)
    utility_collections_matrix = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "utility_matrix_data"
