from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
import json
from datetime import datetime
from .webhook import fetch_data
from .models import CountWells, Urgg, Employee, Task, Incident, OilField, Mining


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
    fetch_data(request)
    return JsonResponse({}, safe=False)
