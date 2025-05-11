from django.urls import path
from .views import *
# from .views import LocationDataFetchingPageView

urlpatterns = [
    path('api/location-data-from-api', LocationDataFetchingPageView.as_view(),
         name='location-from-api'),
    path('api/fetch-location-data', ApiFetchPageView.as_view(),
         name='api-fetch-location-data'),
]
