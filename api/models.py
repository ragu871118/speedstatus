from django.db import models

# Create your models here.


class Location_feed(models.Model):
    origin_id = models.CharField(max_length=100, blank=False, null=False)
    origin_name = models.CharField(max_length=50, blank=False, null=False)
    date_datetime = models.DateTimeField(blank=True, null=True)
    received_datetime = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()
    driver_name = models.CharField(
        max_length=50, blank=True, null=True, default="")
    driver_name_update_time = models.DateTimeField(
        blank=False, null=False, auto_now_add=True)
    # linked_id = models.CharField(max_length=100)
    # linked_name = models.CharField(max_length=50)
    # linked_type = models.CharField(max_length=50)
    zones = models.CharField(max_length=255)
    routes = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    location_lon = models.FloatField(default=0)
    location_lat = models.FloatField(default=0)
    location_speed = models.FloatField(default=0)
    location_altitude = models.FloatField(default=0)
    location_heading = models.FloatField(default=0)
    location_accuracy = models.FloatField(default=0)
    location_age = models.FloatField(default=0)
    location_gc_rd = models.CharField(max_length=50)
    location_gc_rt = models.CharField(max_length=50)
    location_gc_sb = models.CharField(max_length=50)
    location_gc_tw = models.CharField(max_length=50)
    location_gc_pr = models.CharField(max_length=50)
    location_gc_ct = models.CharField(max_length=50)
    location_gc_dc = models.FloatField(default=0)
    location_address = models.CharField(
        max_length=255)
    telemetry_priority = models.FloatField(default=0)
    telemetry_eventId = models.FloatField(default=0)
    telemetry_ignition = models.FloatField(default=0)
    telemetry_moving = models.FloatField(default=0)
    telemetry_motion_start = models.FloatField(
        default=0)
    telemetry_gsm_signal = models.FloatField(
        default=0)
    telemetry_sleep = models.FloatField(default=0)
    telemetry_gnss_status = models.FloatField(
        default=0)
    telemetry_battery_perc = models.FloatField(
        default=0)
    telemetry_sleep_mode = models.FloatField(
        default=0)
    telemetry_pdop = models.FloatField(default=0)
    telemetry_hdop = models.FloatField(default=0)
    telemetry_power_voltage = models.FloatField(
        default=0)
    telemetry_battery_voltage = models.FloatField(
        default=0)
    telemetry_battery_current = models.FloatField(
        default=0)
    telemetry_analog_01 = models.FloatField(default=0)
    telemetry_gsm_code = models.FloatField(default=0)
    telemetry_odometer = models.FloatField(default=0)
    telemetry_movement = models.FloatField(default=0)
    telemetry_hours_00_counter = models.FloatField(
        default=0)
    telemetry_idle_counter = models.FloatField(
        default=0)
    counters_odometer = models.FloatField(default=0)
    counters_hours = models.FloatField(default=0)
    io = models.CharField(max_length=255)
    meta_dsid = models.CharField(max_length=50)
    meta_wshost = models.CharField(max_length=50)
    meta_wsport = models.CharField(max_length=50)
    meta_ecsid = models.CharField(max_length=50)
    meta_tpsq = models.FloatField(default=0)
    object_id = models.CharField(max_length=50, primary_key=True)
    object_name = models.CharField(max_length=50)
    object_type = models.CharField(max_length=50)
    trip_start = models.CharField(max_length=50, blank=True, null=True)
    trip_startAddress = models.CharField(
        max_length=100)
    trip_startLon = models.FloatField(default=0)
    trip_startLat = models.FloatField(default=0)
    trip_distance = models.FloatField(default=0)
    trip_lastLon = models.FloatField(default=0)
    trip_lastLat = models.FloatField(default=0)
    lastMovement_datetime = models.CharField(
        max_length=50, blank=True, null=True)
    privacy = models.CharField(max_length=255)
