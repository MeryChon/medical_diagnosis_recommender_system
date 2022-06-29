from django.urls import path
from aggregations.views import generate_discrimination_qrung_matrix

urlpatterns = [
    path('discrimination-qrung-matrix-generation/', generate_discrimination_qrung_matrix)
]
