from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from ..models import Mountain
from ..serializers import MountainSerializer
from ..permissions import IsAdminUserOrReadOnly


@extend_schema(tags=['Mountains'])
class MountainViewSet(ModelViewSet):
    queryset = Mountain.objects.all().order_by('date')
    serializer_class = MountainSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
