from django.views.generic import TemplateView
import requests
import sys
import os
from django.http import JsonResponse
import json
import asyncio
import aiohttp
from .models import *
# from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from datetime import datetime
from django.db.models import Q


class HomePageView(TemplateView):
    template_name = 'home.html'


class LocationDataFetchingPageView(TemplateView):
    def get(self, request, format=None):
        result = Location_feed.objects.filter(~Q(origin_id='')).values()
        data = []

        for row in result:
            origin_id = row["origin_id"]
            active = row["active"]
            location_speed = row["location_speed"]

            date_datetime = row["date_datetime"]
            telemetry_power_voltage = row["telemetry_power_voltage"]
            telemetry_battery_voltage = row["telemetry_battery_voltage"]
            telemetry_battery_current = row["telemetry_battery_current"]

            speed_status = "Unknown"

            if active == False:
                speed_status = "Parked"
            elif active == True and location_speed > 0:
                speed_status = "Moving"
            elif active == True and location_speed <= 0:
                speed_status = "Idle"

            data.append({
                'origin_id': origin_id,
                'active': active,
                'speed_status': speed_status,
                'date_datetime': date_datetime,
            })

        # data = {
        #     'items': [1, 2, 3],
        #     'count': [5, 9, 4],
        # }
        # return JsonResponse(data)

        output = {
            'location': data,
        }

        return JsonResponse(output)


sequence = 0


class ApiFetchPageView(TemplateView):
    api_key = "c40281af.e8cb873c949fffe308bd55169acbc63d375409ecfec0b577a15f1f7793e2e5af67efc38430c490242c4f75317961855b"
    # api_url = 'https://api.staging.kt1.io/fleet/v2'
    api_url = 'https://api.eu1.kt1.io/fleet/v2'

    client_id = "16224b88-5fb7-43d6-8964-cec899d89c70"
    # sequence = 0

    async def get_location_feed(self, client_id: str, sequence: int, offset: int, limit: int) -> dict:
        # path = f"data/feeds/telemetry/{client_id}?sequence={sequence}&offset={offset}&limit={limit}"
        path = f"data/feeds/location/{client_id}?sequence={sequence}&offset={offset}&limit={limit}"
        headers = {
            'x-api-key': self.api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/{path}", headers=headers) as response:
                return await response.json()

    async def poll(self, seq: int = 0) -> dict:
        return await self.get_location_feed(self.client_id, seq, 0, 100)

    async def delay(self, duration_ms: int):
        await asyncio.sleep(duration_ms / 1000)

    # @database_sync_to_async
    @database_sync_to_async
    def add_or_update_items(self, item):
        # https://stackoverflow.com/questions/78146645/django-core-exceptions-synchronousonlyoperation-you-cannot-call-this-from-an-asy
        try:
            origin_id = item["origin"]["id"] if "origin" in item.keys(
            ) and "id" in item["origin"].keys() else ""
            origin_name = item["origin"]["name"] if "origin" in item.keys() and "name" in item["origin"].keys(
            ) else ""
            date_datetime = item["date"] if "date" in item.keys(
            ) else ""
            received_datetime = item["received"] if "received" in item.keys(
            ) else ""
            active = item["active"] if "active" in item.keys(
            ) else False
            linked = item["linked"] if "linked" in item.keys(
            ) else ""
            zones = ""
            routes = ""
            state = ""
            location_lon = item["location"]["lon"] if "location" in item.keys() and "lon" in item["location"].keys(
            ) else 0
            location_lat = item["location"]["lat"] if "location" in item.keys() and "lat" in item["location"].keys(
            ) else 0
            location_speed = item["location"]["speed"] if "location" in item.keys() and "speed" in item["location"].keys(
            ) else 0
            location_altitude = item["location"]["altitude"] if "location" in item.keys() and "altitude" in item["location"].keys(
            ) else 0
            location_heading = item["location"]["heading"] if "location" in item.keys() and "heading" in item["location"].keys(
            ) else 0
            location_accuracy = item["location"]["accuracy"] if "location" in item.keys() and "accuracy" in item["location"].keys(
            ) else 0
            location_age = item["location"]["age"] if "location" in item.keys() and "age" in item["location"].keys(
            ) else 0
            location_gc_rd = item["location"]["gc"]["rd"] if "location" in item.keys() and "rd" in item["location"]["gc"].keys(
            ) else ""
            location_gc_rt = item["location"]["gc"]["rt"] if "location" in item.keys() and "rt" in item["location"]["gc"].keys(
            ) else ""
            location_gc_sb = item["location"]["gc"]["sb"] if "location" in item.keys() and "sb" in item["location"]["gc"].keys(
            ) else ""
            location_gc_tw = item["location"]["gc"]["tw"] if "location" in item.keys() and "tw" in item["location"]["gc"].keys(
            ) else ""
            location_gc_pr = item["location"]["gc"]["pr"] if "location" in item.keys() and "pr" in item["location"]["gc"].keys(
            ) else ""
            location_gc_ct = item["location"]["gc"]["ct"] if "location" in item.keys() and "ct" in item["location"]["gc"].keys(
            ) else ""
            location_gc_dc = item["location"]["gc"]["dc"] if "location" in item.keys() and "dc" in item["location"]["gc"].keys(
            ) else 0
            location_address = item["location"]["address"] if "location" in item.keys() and "address" in item["location"].keys(
            ) else ""
            telemetry_priority = item["telemetry"]["priority"] if "telemetry" in item.keys() and "priority" in item["telemetry"].keys(
            ) else 0
            telemetry_eventId = item["telemetry"]["eventId"] if "telemetry" in item.keys() and "eventId" in item["telemetry"].keys(
            ) else 0
            telemetry_ignition = item["telemetry"]["ignition"] if "telemetry" in item.keys() and "ignition" in item["telemetry"].keys(
            ) else 0
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

            total_found = Location_feed.objects.filter(
                origin_name=origin_name).count()
            if total_found > 0:
                # print("{} is found.".format(origin_name))
                pass
            else:
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
                obj.save()
        except Exception as e:
            output = str(e)
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

    async def start(self):
        try:
            global sequence
            while True:
                resp = await self.poll(sequence)
                # print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                # print(resp)
                count = resp["count"]
                sequence = resp["sequence"]
                items = resp["items"]
                # print(resp["count"])
                # Convert JSON data to a Python object
                # data = json.loads(items)
                # Iterate through the JSON array
                for item in items:
                    await self.add_or_update_items(item)

                    # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    # print(item)
                    # print(item.keys())
                    # for x in item.keys():
                    #     print("{} --- {}".format(x, item[x]))
                # print("===================================================")
                # print("{}".format(count))
                # print("{}".format(sequence))
                # print("{}".format(resp.keys()))
                # print("===================================================")

                # for item in resp.get("items", []):
                #     # print(item)
                #     # process each item
                #     # sql.update(item["origin"]["id"], item)

                sequence = int(sequence)
                if sequence > 0:
                    break

                await self.delay(30000)

        except Exception as e:
            output = str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)
            output = output + \
                "{} --- {} --- {}".format(exc_type,
                                          fname, exc_tb.tb_lineno)

            # print("==========================================================")
            # print(output)
            # print("==========================================================")

    def get(self, request, format=None):
        # print("*******************************************************")
        output = ""
        try:
            asyncio.run(self.start())
            output = "Data fetch successful"
        except Exception as e:
            output = "Data fetch failed"

            output = str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)
            output = output + \
                "{} --- {} --- {}".format(exc_type,
                                          fname, exc_tb.tb_lineno)

            # print("==========================================================")
            # print(output)
            # print("==========================================================")

        # data = {
        #     'items': [1, 2, 3],
        #     'count': [5, 9, 4],
        # }

        data = {'output': output}

        return JsonResponse(data)


class TestPageView2(TemplateView):
    template_name = 'home.html'

    # Optional: Change context data dict
    def get_context_data(self, **kwargs):
        print("*******************************************************")
        response = requests.get("http://api.open-notify.org/astros")
        # print(response.status_code)
        # data = response.json()
        # print(response.json())

        # Checking if the request was successful
        if response.status_code == 200:
            # Printing the retrieved data
            print(response.json())
        else:
            print(f"Failed to retrieve data: {response.status_code}")
        print("*******************************************************")

        context = super().get_context_data(**kwargs)
        context['title'] = ""
        context['headline'] = ""
        context['output'] = "Coming soon..."
        return context

    def get(self, request, format=None):
        output = ''
        print("*******************************************************")
        try:
            response = requests.get("http://api.open-notify.org/astros")
            # print(response.status_code)
            # data = response.json()
            # print(response.json())

            # Checking if the request was successful
            if response.status_code == 200:
                # Printing the retrieved data
                # print(response.json())
                pass
            else:
                # print(f"Failed to retrieve data: {response.status_code}")
                pass

            # HttpResponse("Success")
        except Exception as e:
            output = str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)
            output = output + \
                "{} --- {} --- {}".format(exc_type,
                                          fname, exc_tb.tb_lineno)

            print("==========================================================")
            print(output)
            print("==========================================================")
