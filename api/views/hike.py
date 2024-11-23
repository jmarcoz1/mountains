from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from ..models import Hike, Mountain
from ..serializers import HikeSerializer


@extend_schema(tags=['Hikes'])
class HikeSignupView(CreateAPIView):
    queryset = Hike.objects.all()
    serializer_class = HikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        mountain = Mountain.objects.get(pk=request.data['mountain'])
        hike_data = {
            'participant': request.data['participant'],
            'mountain': mountain.pk,
        }
        serializer = self.get_serializer(data=hike_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Hikes'])
class HikeValidateView(RetrieveAPIView):
    queryset = Hike.objects.all()
    serializer_class = HikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        hike = self.get_object()
        return Response({
            'message': f"Mountain: {hike.mountain}, \
            participant: {hike.participant}, \
            day: {hike.hike_date}, \
            camping: {hike.camping}"
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Hikes'])
class HikeUnrollView(APIView):
    serializer_class = HikeSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, hike_id):
        hike = get_object_or_404(Hike, id=hike_id)
        if hike.participant != request.user:
            return Response(
                {"detail": "You are not authorized to unroll from this hike."},
                status=status.HTTP_403_FORBIDDEN
            )
        mountain = hike.mountain
        mountain.delete()
        hike.save()
        return Response(
            {"detail": f"Successfully unrolled from {self.hike}."},
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=['Mountains'],
    parameters=[
        OpenApiParameter("start_date",
                         OpenApiTypes.DATE,
                         description="Start date for filtering (YYYY-DD-MM)",
                         required=False),
        OpenApiParameter("end_date",
                         OpenApiTypes.DATE,
                         description="End date for filtering (YYYY-DD-MM)",
                         required=False)
    ]
)
class MountainReportView(ListAPIView):
    queryset = Hike.objects.all()
    serializer_class = HikeSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = Hike.objects.all()

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            try:
                start_date = parse_date(start_date)
                end_date = parse_date(end_date)
                queryset = queryset.filter(date__range=[start_date, end_date])
            except ValueError:
                pass

        return queryset
