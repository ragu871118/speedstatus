from django.views.generic import TemplateView
from asgiref.sync import sync_to_async
import requests
import sys
import os
from django.http import HttpResponse
from django.http import JsonResponse
import json
import asyncio
import aiohttp
from .models import *
# from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from datetime import datetime
from django.db.models import Q

class DataMapper:
    async def store(self, item):
        print("==============================================================")
        print("==============================================================")
        print("==============================================================")
        print("==============================================================")
        print("==============================================================")
        print(item)
        if item is None:
            return
        
        if item.keys() is None:
            return
        
        # https://stackoverflow.com/questions/78146645/django-core-exceptions-synchronousonlyoperation-you-cannot-call-this-from-an-asy
        print("==============================================================")
        try:
            print('a')
            origin_id = item["origin"]["id"] if "origin" in item.keys(
            ) and "id" in item["origin"].keys() else ""
            print('b')
            origin_name = item["origin"]["name"] if "origin" in item.keys() and "name" in item["origin"].keys(
            ) else ""
            print('c')
            date_datetime = item["date"] if "date" in item.keys(
            ) else ""
            print('d')
            received_datetime = item["received"] if "received" in item.keys(
            ) else ""
            print('e')
            active = item["active"] if "active" in item.keys(
            ) else False
            print('f')
            linked = item["linked"] if "linked" in item.keys(
            ) else ""
            print('g')
            zones = ""
            routes = ""
            state = ""
            print('h')
            location_lon = item["location"]["lon"] if "location" in item.keys() and "lon" in item["location"].keys(
            ) else 0
            print('i')
            location_lat = item["location"]["lat"] if "location" in item.keys() and "lat" in item["location"].keys(
            ) else 0
            print('j')
            location_speed = item["location"]["speed"] if "location" in item.keys() and "speed" in item["location"].keys(
            ) else 0
            print('k')
            location_altitude = item["location"]["altitude"] if "location" in item.keys() and "altitude" in item["location"].keys(
            ) else 0
            print('l')
            location_heading = item["location"]["heading"] if "location" in item.keys() and "heading" in item["location"].keys(
            ) else 0
            print('m')
            location_accuracy = item["location"]["accuracy"] if "location" in item.keys() and "accuracy" in item["location"].keys(
            ) else 0
            print('n')
            location_age = item["location"]["age"] if "location" in item.keys() and "age" in item["location"].keys(
            ) else 0
            print('o')
            location_gc_rd = item["location"]["gc"]["rd"] if "location" in item.keys() and "gc" in item["location"].keys() and item["location"]["gc"] is not None and "rd" in item["location"]["gc"].keys(
            ) else ""
            print('p')
            location_gc_rt = item["location"]["gc"]["rt"] if "location" in item.keys() and "gc" in item["location"].keys() and item["location"]["gc"] is not None and "rt" in item["location"]["gc"].keys(
            ) else ""
            print('q')
            location_gc_sb = item["location"]["gc"]["sb"] if "location" in item.keys() and "gc" in item["location"].keys() and item["location"]["gc"] is not None and "sb" in item["location"]["gc"].keys(
            ) else ""
            print('r')
            location_gc_tw = item["location"]["gc"]["tw"] if "location" in item.keys() and "gc" in item["location"].keys() and item["location"]["gc"] is not None and "tw" in item["location"]["gc"].keys(
            ) else ""
            print('s')
            location_gc_pr = item["location"]["gc"]["pr"] if "location" in item.keys() and "gc" in item["location"].keys() and item["location"]["gc"] is not None and "pr" in item["location"]["gc"].keys(
            ) else ""
            print('t')
            location_gc_ct = item["location"]["gc"]["ct"] if "location" in item.keys() and "gc" in item["location"].keys() and item["location"]["gc"] is not None and "ct" in item["location"]["gc"].keys(
            ) else ""
            print('u')
            location_gc_dc = item["location"]["gc"]["dc"] if "location" in item.keys() and "gc" in item["location"].keys() and item["location"]["gc"] is not None and "dc" in item["location"]["gc"].keys(
            ) else 0
            print('v')
            location_address = item["location"]["address"] if "location" in item.keys() and "gc" in item["location"].keys() and "address" in item["location"].keys(
            ) else ""
            print('w')
            telemetry_priority = item["telemetry"]["priority"] if "telemetry" in item.keys() and "priority" in item["telemetry"].keys(
            ) else 0
            print('x')
            telemetry_eventId = item["telemetry"]["eventId"] if "telemetry" in item.keys() and "eventId" in item["telemetry"].keys(
            ) else 0
            print('y')
            telemetry_ignition = item["telemetry"]["ignition"] if "telemetry" in item.keys() and "ignition" in item["telemetry"].keys(
            ) else 0
            print('z')
            telemetry_moving = item["telemetry"]["moving"] if "telemetry" in item.keys() and "moving" in item["telemetry"].keys(
            ) else 0
            telemetry_motion_start = item["telemetry"]["motion_start"] if "telemetry" in item.keys() and "motion_start" in item["telemetry"].keys(
            ) else 0
            telemetry_gsm_signal = item["telemetry"]["gsm_signal"] if "telemetry" in item.keys() and "gsm_signal" in item["telemetry"].keys(
            ) else 0
            telemetry_sleep = item["telemetry"]["sleep"] if "telemetry" in item.keys() and "sleep" in item["telemetry"].keys(
            ) else 0
            telemetry_gnss_status = item["telemetry"]["gnss_status"] if "telemetry" in item.keys() and "gnss_status" in item["telemetry"].keys(
            ) else 0
            telemetry_battery_perc = item["telemetry"]["battery_perc"] if "telemetry" in item.keys() and "battery_perc" in item["telemetry"].keys(
            ) else 0
            telemetry_sleep_mode = item["telemetry"]["sleep_mode"] if "telemetry" in item.keys() and "sleep_mode" in item["telemetry"].keys(
            ) else 0
            telemetry_pdop = item["telemetry"]["pdop"] if "telemetry" in item.keys() and "pdop" in item["telemetry"].keys(
            ) else 0
            telemetry_hdop = item["telemetry"]["hdop"] if "telemetry" in item.keys() and "hdop" in item["telemetry"].keys(
            ) else 0
            telemetry_power_voltage = item["telemetry"]["power_voltage"] if "telemetry" in item.keys() and "power_voltage" in item["telemetry"].keys(
            ) else 0
            telemetry_battery_voltage = item["telemetry"]["battery_voltage"] if "telemetry" in item.keys() and "battery_voltage" in item["telemetry"].keys(
            ) else 0
            telemetry_battery_current = item["telemetry"]["battery_current"] if "telemetry" in item.keys() and "battery_current" in item["telemetry"].keys(
            ) else 0
            telemetry_analog_01 = item["telemetry"]["analog_01"] if "telemetry" in item.keys() and "analog_01" in item["telemetry"].keys(
            ) else 0
            telemetry_gsm_code = item["telemetry"]["gsm_code"] if "telemetry" in item.keys() and "gsm_code" in item["telemetry"].keys(
            ) else 0
            telemetry_odometer = item["telemetry"]["odometer"] if "telemetry" in item.keys() and "odometer" in item["telemetry"].keys(
            ) else 0
            telemetry_movement = item["telemetry"]["movement"] if "telemetry" in item.keys() and "movement" in item["telemetry"].keys(
            ) else 0
            telemetry_hours_00_counter = item["telemetry"]["hours_00_counter"] if "telemetry" in item.keys() and "hours_00_counter" in item["telemetry"].keys(
            ) else 0
            telemetry_idle_counter = item["telemetry"]["idle_counter"] if "telemetry" in item.keys() and "idle_counter" in item["telemetry"].keys(
            ) else 0
            counters_odometer = item["counters"]["odometer"] if "counters" in item.keys() and "odometer" in item["counters"].keys(
            ) else 0
            counters_hours = item["counters"]["hours"] if "counters" in item.keys() and "hours" in item["counters"].keys(
            ) else 0
            io = ""
            meta_dsid = item["meta"]["dsid"] if "meta" in item.keys() and "dsid" in item["meta"].keys(
            ) else ""
            meta_wshost = item["meta"]["wshost"] if "meta" in item.keys() and "wshost" in item["meta"].keys(
            ) else ""
            meta_wsport = item["meta"]["wsport"] if "meta" in item.keys() and "wsport" in item["meta"].keys(
            ) else ""
            meta_ecsid = item["meta"]["ecsid"] if "meta" in item.keys() and "ecsid" in item["meta"].keys(
            ) else ""
            meta_tpsq = item["meta"]["tpsq"] if "meta" in item.keys() and "tpsq" in item["meta"].keys(
            ) else 0
            object_id = item["object"]["id"] if "object" in item.keys() and "id" in item["object"].keys(
            ) else ""
            object_name = item["object"]["name"] if "object" in item.keys() and "name" in item["object"].keys(
            ) else ""
            object_type = item["object"]["type"] if "object" in item.keys() and "type" in item["object"].keys(
            ) else ""
            trip_start = item["trip"]["start"] if "trip" in item.keys() and "start" in item["trip"].keys(
            ) else ""
            trip_startAddress = item["trip"]["startAddress"] if "trip" in item.keys() and "startAddress" in item["trip"].keys(
            ) else ""
            trip_startLon = item["trip"]["startLon"] if "trip" in item.keys() and "startLon" in item["trip"].keys(
            ) else 0
            trip_startLat = item["trip"]["startLat"] if "trip" in item.keys() and "startLat" in item["trip"].keys(
            ) else 0
            trip_distance = item["trip"]["distance"] if "trip" in item.keys() and "distance" in item["trip"].keys(
            ) else 0
            trip_lastLon = item["trip"]["lastLon"] if "trip" in item.keys() and "lastLon" in item["trip"].keys(
            ) else 0
            trip_lastLat = item["trip"]["lastLat"] if "trip" in item.keys() and "lastLat" in item["trip"].keys(
            ) else 0
            lastMovement_datetime = item["lastMovement"] if "lastMovement" in item.keys(
            ) else ""
            privacy = str(
                item["privacy"]) if "privacy" in item.keys() else ""

            # datetime_format = "%d-%b-%Y-%H:%M:%S"
            # date_datetime = datetime.strptime(date_datetime, datetime_format)
            # received_datetime = datetime.strptime(
            #     received_datetime, datetime_format)
            # trip_start = datetime.strptime(trip_start, datetime_format)
            # lastMovement_datetime = datetime.strptime(
            #     lastMovement_datetime, datetime_format)

            # if date_datetime == "":
            #     print("date_datetime is empty.")
            # elif received_datetime == "":
            #     print("received_datetime is empty.")
            # elif trip_start == "":
            #     print("trip_start is empty.")
            # elif lastMovement_datetime == "":
            #     print("lastMovement_datetime is empty.")

            # def update_option_value(self, option_name, option_value):
            #     total_found = Option_list.objects.filter(
            #         option_name=option_name).count()
            #     if total_found > 0:
            #         Option_list.objects.filter(option_name=option_name).update(
            #             option_value=option_value)
            #     else:
            #         obj = Option_list()
            #         obj.option_name = option_name
            #         obj.option_value = option_value
            #         obj.save()

            # total_found = Location_feed.objects.filter(
            #     origin_name=origin_name).count()
            # if total_found > 0:
            #     # print("{} is found.".format(origin_name))
            #     pass
            # else:
            obj = Location_feed()
            obj.origin_id = origin_id
            obj.origin_name = origin_name
            obj.date_datetime = date_datetime
            obj.received_datetime = received_datetime
            obj.active = active
            # obj.linked_id = linked_id
            # obj.linked_name = linked_name
            # obj.linked_type = linked_type
            obj.zones = zones
            obj.routes = routes
            obj.state = state
            obj.location_lon = location_lon
            obj.location_lat = location_lat
            obj.location_speed = location_speed
            obj.location_altitude = location_altitude
            obj.location_heading = location_heading
            obj.location_accuracy = location_accuracy
            obj.location_age = location_age
            obj.location_gc_rd = location_gc_rd
            obj.location_gc_rt = location_gc_rt
            obj.location_gc_sb = location_gc_sb
            obj.location_gc_tw = location_gc_tw
            obj.location_gc_pr = location_gc_pr
            obj.location_gc_ct = location_gc_ct
            obj.location_gc_dc = location_gc_dc
            obj.location_address = location_address
            obj.telemetry_priority = telemetry_priority
            obj.telemetry_eventId = telemetry_eventId
            obj.telemetry_ignition = telemetry_ignition
            obj.telemetry_moving = telemetry_moving
            obj.telemetry_motion_start = telemetry_motion_start
            obj.telemetry_gsm_signal = telemetry_gsm_signal
            obj.telemetry_sleep = telemetry_sleep
            obj.telemetry_gnss_status = telemetry_gnss_status
            obj.telemetry_battery_perc = telemetry_battery_perc
            obj.telemetry_sleep_mode = telemetry_sleep_mode
            obj.telemetry_pdop = telemetry_pdop
            obj.telemetry_hdop = telemetry_hdop
            obj.telemetry_power_voltage = telemetry_power_voltage
            obj.telemetry_battery_voltage = telemetry_battery_voltage
            obj.telemetry_battery_current = telemetry_battery_current
            obj.telemetry_analog_01 = telemetry_analog_01
            obj.telemetry_gsm_code = telemetry_gsm_code
            obj.telemetry_odometer = telemetry_odometer
            obj.telemetry_movement = telemetry_movement
            obj.telemetry_hours_00_counter = telemetry_hours_00_counter
            obj.telemetry_idle_counter = telemetry_idle_counter
            obj.counters_odometer = counters_odometer
            obj.counters_hours = counters_hours
            obj.io = io
            obj.meta_dsid = meta_dsid
            obj.meta_wshost = meta_wshost
            obj.meta_wsport = meta_wsport
            obj.meta_ecsid = meta_ecsid
            obj.meta_tpsq = meta_tpsq
            obj.object_id = object_id
            obj.object_name = object_name
            obj.object_type = object_type
            obj.trip_start = trip_start
            obj.trip_startAddress = trip_startAddress
            obj.trip_startLon = trip_startLon
            obj.trip_startLat = trip_startLat
            obj.trip_distance = trip_distance
            obj.trip_lastLon = trip_lastLon
            obj.trip_lastLat = trip_lastLat
            obj.lastMovement_datetime = lastMovement_datetime
            obj.privacy = privacy
            
            print('before')
            await sync_to_async(obj.save)()
            print('after')
        except Exception as e:
            output = str(e)
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)
            output = output + \
                "{} --- {} --- {}".format(exc_type,
                                          fname, exc_tb.tb_lineno)

            output = output + "\n\n{} --- {} --- {} --- {}".format(
                date_datetime, received_datetime, trip_start, lastMovement_datetime)

            # print("==========================================================")
            # print(output)
            # print("==========================================================")