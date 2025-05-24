from django.urls import path
from .views import *
# from .views import LocationDataFetchingPageView

# http://127.0.0.1:8000/api/fetch-location-data
# http://127.0.0.1:8000/api/location-data-all-rows
# http://127.0.0.1:8000/api/location-data-vehicles-only

urlpatterns = [
    path('api/fetch-location-data', ApiFetchPageView.as_view(),
         name='fetch-location-data'),
    path('api/location-data-all-rows', LocationDataAllRowsPageView.as_view(),
         name='location-data-all-rows'),
    path('api/location-data-vehicles-only', LocationDataOnlyVehicleRowsPageView.as_view(),
         name='location-data-vehicles-only'),
]

# urlpatterns = [
#     path('api/location-data-from-api', LocationDataFetchingPageView.as_view(),
#          name='location-from-api'),
#     path('api/fetch-location-data', ApiFetchPageView.as_view(),
#          name='fetch-location-data'),
#     path('api/test', ApiFetchPageView.as_view(),
#          name='fetch-location-data'),
# ]
