from django.urls import path
from .views import webhook, index_view, chat_message


app_name = 'info'


urlpatterns = [
    path('', index_view, name='index_view'),
    path('info/chat-message', chat_message, name='chat_message'),
    path('info/webhook', webhook, name='webhook'),
]
