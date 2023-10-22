from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    delivery_time = models.DateTimeField()

    def __str__(self):
        return f"Order #{self.id} from {self.vendor.name}"


class Trip(models.Model):
    ORDER_STATUS_CHOICES = (
        ("DELIVERED", "Delivered"),
        ("PICKED", "Picked"),
        ("AT_VENDOR", "At Vendor"),
        ("ASSIGNED", "Assigned"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return f"Trip for Order #{self.order.id}"


class DelayReports(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    report_type = models.IntegerField()  # 1 or 2 based on the delay approach
    new_delivery_time = models.DateTimeField()

    def __str__(self):
        return f"Delay Report for Order #{self.order.id}"


class DelayQueue(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delay Queue for Order #{self.order.id}"
