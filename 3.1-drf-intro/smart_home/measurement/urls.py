from django.urls import path
from.views import SensorView, SensorDetailView, MeasurementDetailView

urlpatterns = [
    path('sensors/', SensorView.as_view(), name='sensors'),
    path('sensors/<pk>/', SensorDetailView.as_view(), name='sensorinfo'),
    path('measurements/', MeasurementDetailView.as_view(), name='measurements'),
]
