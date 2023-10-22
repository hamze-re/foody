from django.contrib import admin

from .models import Agent, DelayQueue, DelayReports, Order, Trip, Vendor

admin.site.register(Order)
admin.site.register(Trip)
admin.site.register(Agent)
admin.site.register(Vendor)
admin.site.register(DelayReports)
admin.site.register(DelayQueue)
