from django.urls import path
from .views import webhook, index_view, chat_message


app_name = 'demo'


urlpatterns = [
    path('', index_view, name='index_view'),
    path('demo/chat-message', chat_message, name='chat_message'),
    path('demo/webhook/', webhook, name='webhook'),
]
