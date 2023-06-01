from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementDetailSerializer


class SensorView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
       
    
class SensorDetailView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()    
    serializer_class = SensorDetailSerializer
    
    
class MeasurementDetailView(ListCreateAPIView):
    queryset = Measurement.objects.all()    
    serializer_class = MeasurementDetailSerializer