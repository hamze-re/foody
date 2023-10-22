from django.urls import path

from .views import AssignOrderToEmployee, OrderDelayReport, ReceiveStoreDelayReports

urlpatterns = [
    path(
        "delay-report/<int:order_id>/",
        OrderDelayReport.as_view(),
        name="order-delay-report",
    ),
    path("assign-order/", AssignOrderToEmployee.as_view(), name="assign-order-to-employee"),
    path(
        "receive-delay-reports/",
        ReceiveStoreDelayReports.as_view(),
        name="receive-store-delay-reports",
    ),
]
