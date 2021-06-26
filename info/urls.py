from django.urls import path
from .views import webhook, index_view


app_name = 'info'


urlpatterns = [
    path('', index_view, name='index_view'),
    path('info/webhook', webhook, name='webhook'),
]
