import json
from pprint import pprint


def fetch_data(request):
    req = json.loads(request.body)
    result = req.get('queryResult')
    queryText = result.get('queryText')
    intent = result.get('intent')
    param = result.get('parameters')
    meta = result.get('originalDetectIntentRequest',{}).get('payload', {}).get('meta')
    fulfillmentText  = result.get('fulfillmentText')
    fulfillmentMessages = result.get('fulfillmentMessages')
    intent_name = intent.get('displayName')
    allis_user = req.get('originalDetectIntentRequest', {}).get('payload', {}).get('session', {}).get('user')
    client = {
        'client_id':req.get('originalDetectIntentRequest', {}).get('payload', {}).get('meta',{}).get('client_id',{})
    }
    action = result.get('action', {})
    # print(req.get('originalDetectIntentRequest', {}).get('payload', {}))
    print(allis_user, client, 'запрос пользователя:', queryText,"\nответ агента:", fulfillmentText,"\nПараметры", param,'\nЭкшен', action)
