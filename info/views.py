import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.http import JsonResponse
from datetime import datetime

from .tasks import chatbase_send
from .tools.services import messages_handler


def convert_str_date(value):
    if value:
        d = datetime.fromisoformat(value)
        return d.strftime('%Y-%m-%d')
    return datetime.strftime(datetime.now(), '%Y-%m-%d')


@require_http_methods(['GET'])
def index_view(request): # noqa
    return redirect('https://console.dialogflow.com/api-client/demo/embedded/e150236a-3743-4bc5-9987-e85cbc58d00e')


@csrf_exempt
@require_http_methods('POST')
def webhook(request):
    data = json.loads(request.body)
    chatbase_send.delay(data)
    response = messages_handler(request)
    print(request)
    return JsonResponse(response, safe=False)
