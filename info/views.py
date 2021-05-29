from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime
from .tasks import chatbase_send


def convert_str_date(value):
    if value:
        d = datetime.fromisoformat(value)
        return d.strftime('%Y-%m-%d')
    return datetime.strftime(datetime.now(), '%Y-%m-%d')


@require_http_methods(['GET'])
def index_view(request):
    return render(request, 'info/home.html')


@require_http_methods('POST')
def chat_message():
    pass


@csrf_exempt
def webhook(request):
    data = json.loads(request.body)
    chatbase_send.delay(data)
    return JsonResponse({}, safe=False)
