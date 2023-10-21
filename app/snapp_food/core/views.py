from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Agent, DelayQueue, DelayReports, Order, Trip, Vendor
from .serializers import DelayReportsSerializer, OrderSerializer


class OrderDelayReport(APIView):
    def get(self, request, order_id):
        try:
            # Find the order by ID
            order = Order.objects.get(pk=order_id)

            # Check if a trip record exists for the order in ASSIGNED, AT_VENDOR, or PICKED status
            trip = Trip.objects.filter(order=order, status__in=["ASSIGNED", "AT_VENDOR", "PICKED"]).first()

            if trip:
                # Use an external service to get a new estimated delivery time
                # Replace the URL below with the actual URL of the external service
                new_delivery_time = get_new_delivery_time_from_external_service(trip)

                # Update the order's delivery time with the new estimated time
                order.delivery_time = new_delivery_time
                order.save()

                # Create a delay report
                delay_report = DelayReports(order=order, report_type=1, new_delivery_time=new_delivery_time)
                delay_report.save()

                # Serialize the delay report and return it in the response
                serializer = DelayReportsSerializer(delay_report)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If no valid trip record exists, insert the order into the DelayQueue
                delay_queue_entry = DelayQueue(order=order)
                delay_queue_entry.save()

                # If no valid trip record exists, place the order in the delay queue
                # Create a delay report with report_type=2
                # You may implement your own logic for placing orders in the delay queue
                # For this example, we're just creating a report with report_type=2
                delay_report = DelayReports(order=order, report_type=2, new_delivery_time=order.delivery_time)
                delay_report.save()

                serializer = DelayReportsSerializer(delay_report)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response("Order not found", status=status.HTTP_404_NOT_FOUND)


def get_new_delivery_time_from_external_service(trip):
    # Implement logic to make a request to the external service and parse the response
    # You'll need to use libraries like requests to make HTTP requests
    # Replace the URL with the actual URL of the external service
    import requests

    url = "https://run.mocky.io/v3/122c2796-5df4-461c-ab75-87c1192b17f7"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the response to extract the new estimated delivery time
        response_data = response.json()
        new_delivery_time = response_data.get("new_delivery_time")
        return new_delivery_time
    else:
        # Handle errors when the external service request fails
        raise Exception("Error fetching new estimated delivery time")


class AssignOrderToEmployee(APIView):
    def post(self, request, agent_id):
        try:
            # Find the next order in the delay queue in FIFO order
            next_delayed_order = DelayQueue.objects.order_by("created_at").first()

            if next_delayed_order:
                # Check if the order is already assigned to an agent
                if next_delayed_order.agent is not None:
                    return Response(
                        "Order already assigned to an agent",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Get the agent based on the provided agent_id
                agent = Agent.objects.get(pk=agent_id)

                # Assign the order to the agent
                next_delayed_order.agent = agent
                next_delayed_order.save()

                # Serialize the assigned order and return it in the response
                serializer = OrderSerializer(next_delayed_order.order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "No orders in the delay queue to assign",
                    status=status.HTTP_404_NOT_FOUND,
                )
        except DelayQueue.DoesNotExist:
            return Response(
                "No orders in the delay queue to assign",
                status=status.HTTP_404_NOT_FOUND,
            )
        except Agent.DoesNotExist:
            return Response("Agent not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceiveStoreDelayReports(APIView):
    def get(self, request):
        try:
            # Calculate the date one week ago from the current date
            one_week_ago = datetime.now() - timedelta(weeks=1)

            # Query the DelayReports model to count the delay reports
            # for each store within the last week
            store_delay_reports = Vendor.objects.annotate(
                delay_count=Count(
                    "order__delayreports",
                    filter=Q(order__delayreports__new_delivery_time__gte=one_week_ago),
                )
            ).order_by("-delay_count")

            # Serialize the store delay reports and return them in the response
            serialized_data = [
                {"store_name": store.name, "delay_count": store.delay_count} for store in store_delay_reports
            ]
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
