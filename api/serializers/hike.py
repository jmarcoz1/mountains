from rest_framework import serializers
from ..models import Hike


class MITTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hike
        fields = ['mountain', 'hike_date', 'camping']
        read_only_fields = ['mountain', 'hike_date', 'camping']
