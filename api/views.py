from django.views.generic import TemplateView
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
from django.utils import timezone
from django.db.models import Q

from .kinesisproapi import KinesisProApi
from .processor import Processor
from .datamapper import DataMapper

from asgiref.sync import sync_to_async


class HomePageView(TemplateView):
    template_name = 'home.html'


class LocationDataAllRowsPageView(TemplateView):
    def get(self, request, format=None):
        result = Location_feed.objects.filter(~Q(origin_id='')).values()
        data = []

        for row in result:
            object_name = str(row["object_name"]).strip().upper()
            object_id = row["object_id"]
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

            if active == True:
                active = "Active"
            else:
                active = "Inactive"

            item_type = ""
            if object_name.startswith('T/'):
                item_type = "Trailer"
            else:
                item_type = "Vehicle"

            driver_name = ""

            data.append({
                'object_id': object_id,
                'object_name': object_name,
                "item_type": item_type,
                "driver_name": driver_name,
                'is_active': active,
                'speed_status': speed_status,
                'power_voltage': telemetry_power_voltage,
                'date_datetime': date_datetime,
            })

        # data = {
        #     'items': [1, 2, 3],
        #     'count': [5, 9, 4],
        # }
        # return JsonResponse(data)

        # return JsonResponse(data, safe=False)
        # return json.dumps(data, default=str)
        # return JsonResponse(data, safe=False, )

        response = HttpResponse(json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')
        return response


class LocationDataOnlyVehicleRowsPageView(TemplateView):
    def get(self, request, format=None):
        result = Location_feed.objects.filter(~Q(origin_id='')).values()
        data = []

        for row in result:
            object_name = str(row["object_name"]).strip().upper()

            # =========================================================Gavin:
            # the "object" is the vehicle
            # the "origin" is the device
            # vehicle === asset

            # just ignore any records where the "object"'s name starts with `T/`

            # you could use a regex like:  /T\/[0-9A-Z]+$/i
            # if the regex matches, its a trailer, if not, its a vehicle

            # Tanzil: So, I should count only the values that does not start with "T/", right?

            # Gavin: correct=========================================================

            if not object_name.startswith('T/'):
                object_id = row["object_id"]
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

                if active == True:
                    active = "Active"
                else:
                    active = "Inactive"

                item_type = ""
                if object_name.startswith('T/'):
                    item_type = "Trailer"
                else:
                    item_type = "Vehicle"

                data.append({
                    'object_id': object_id,
                    'object_name': object_name,
                    "item_type": item_type,
                    'is_active': active,
                    'speed_status': speed_status,
                    'power_voltage': telemetry_power_voltage,
                    'date_datetime': date_datetime,
                })

        # data = {
        #     'items': [1, 2, 3],
        #     'count': [5, 9, 4],
        # }
        # return JsonResponse(data)

        # return JsonResponse(data, safe=False)
        # return json.dumps(data, default=str)
        # return JsonResponse(data, safe=False, )

        response = HttpResponse(json.dumps(
            data, indent=4, sort_keys=True, default=str), content_type='application/json')
        return response


# kinesis_pro_api_url = 'https://api.staging.kt1.io/fleet/v2'
# kinesis_pro_api_url = 'https://api.staging.kt1.io/fleet/v2'
kinesis_pro_api_url = 'https://api.eu1.kt1.io/fleet/v2'
kinesis_pro_api_key = "c40281af.e8cb873c949fffe308bd55169acbc63d375409ecfec0b577a15f1f7793e2e5af67efc38430c490242c4f75317961855b"
kinesis_pro_client_id = "16224b88-5fb7-43d6-8964-cec899d89c70"
asset_count = 500  # should always be more than the real count, but not so much more that you make requests for vehicles that aren't there
count_per_group = 300

kinesis_pro_api = KinesisProApi(
    kinesis_pro_api_url, kinesis_pro_api_key, kinesis_pro_client_id)
data_mapper = DataMapper()
processor = Processor(kinesis_pro_api, data_mapper,
                      asset_count, count_per_group)


class UpdateDriverNamePageView(TemplateView):
    async def get(self, request, format=None):
        # print("*******************************************************")
        output = "N/A"
        try:
            # await processor.poll()
            # driver_name_update_time = datetime.now()
            driver_name_update_time = timezone.now()
            # location_items = await sync_to_async(Location_feed.objects.order_by(
            #     'driver_name_update_time')[:1])
            # for location_item in location_items:

            async for location_item in Location_feed.objects.order_by(
                    'driver_name_update_time')[:5]:
                object_id = location_item.object_id

                driver_name = ""
                path = f"entities/assets/{object_id}"
                headers = {
                    'x-api-key': kinesis_pro_api_key
                }
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{kinesis_pro_api_url}/{path}", headers=headers) as response:
                        # await response.json()
                        response_data = await response.json()
                        driver_name = response_data["fields"]["driversname"] if "fields" in response_data.keys(
                        ) and "driversname" in response_data["fields"].keys() else ""

                obj = await Location_feed.objects.aget(object_id=object_id)
                obj.driver_name = driver_name
                obj.driver_name_update_time = driver_name_update_time
                await sync_to_async(obj.save)()
            output = "Driver name update was successful"
        except Exception as e:
            output = "Driver name update failed"

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


class ApiFetchPageView(TemplateView):
    async def get(self, request, format=None):
        # print("*******************************************************")
        output = ""
        try:
            await processor.poll()
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
