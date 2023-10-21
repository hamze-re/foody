from rest_framework import serializers

from .models import DelayQueue, DelayReports, Order, Trip, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class DelayReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DelayReports
        fields = "__all__"


class DelayQueue(serializers.ModelSerializer):
    class Meta:
        model = DelayQueue
        fields = "__all__"
