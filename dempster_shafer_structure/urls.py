from django.urls import path

from dempster_shafer_structure.views import run_decision_making_process, \
    DempsterShaferBeliefStructureDataViewSet

urlpatterns = [
    path('structure/', DempsterShaferBeliefStructureDataViewSet.as_view()),
    path('run/', run_decision_making_process)
]
