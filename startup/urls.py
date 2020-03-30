from django.urls import path
from .views import index, update_session

urlpatterns = [
    path('', index, name='index_view'),
    path('update_session', update_session, name="update_session")
]