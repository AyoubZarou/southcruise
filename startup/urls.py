from django.urls import path
from .views import index, country_view, contact_us_view

urlpatterns = [
    path('', index, name='index_view'),
    path('country/', country_view, name="country_view"),
    path('contact_us', contact_us_view, name='contact_us')
]