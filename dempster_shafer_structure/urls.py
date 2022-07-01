from django.urls import path

from dempster_shafer_structure.views import get_dempster_shafer_structure_data, run_decision_making_process

urlpatterns = [
    path('structure/', get_dempster_shafer_structure_data),
    path('run/', run_decision_making_process)
]
