from config.celery import app
from .tools.chatbase import MessageSet
from .tools.dialogflow_webhook import WebhookHandler
from .tools.telegram import TelegramHandler
from .tools.alice import AliceRequest, is_alice
from django.conf import settings

API_KEY = settings.CHATBASE_API_KEY


@app.task
def chatbase_send(data):
    msg = WebhookHandler(data)
    payload = msg.get_payload()
    user_id = ""
    version = "0.1"
    if is_alice(msg):
        msg.set_source('alice')
        m = AliceRequest(payload)
        user_msg = m.command
        user_id = m.uid
    elif msg.get_source() == 'telegram':
        m = TelegramHandler(payload)
        user_id = m.get_uid()
        user_msg = m.get_text()
    else:
        user_msg = ""
    platform = msg.get_source()
    intent = msg.get_intent_display_name()
    session_id = msg.get_session_id()
    agent_msg = msg.get_fulfillment_text()
    action = msg.get_action()
    not_handled = True if action == 'input.unknown' else False
    messages = MessageSet(api_key=API_KEY, platform=platform, version=version, user_id=user_id)
    messages.new_message(intent=intent, message=user_msg, session_id=session_id, msg_type='user', not_handled=not_handled)
    messages.new_message(intent=intent, message=agent_msg, session_id=session_id, msg_type='agent')
    req = messages.send()
    print(req.json())
