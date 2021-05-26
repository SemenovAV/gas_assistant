class TelegramHandler(object):

    def __init__(self, payload):
        self.data = payload['data']

    def get_uid(self):
        return f"{self.get_user_id()}-{self.get_lang_code()}.telegram_client"

    def get_date(self):
        return self.data['date']

    def get_chat_id(self):
        return self.data['chat']['id']

    def get_chat_type(self):
        return self.data['chat']['type']

    def get_user_first_name(self):
        return self.data['from']['first_name']

    def get_user_last_name(self):
        return self.data['from']['last_name']

    def get_user_id(self):
        return self.data['from']['id']

    def get_username(self):
        return self.data['from']['username']

    def get_lang_code(self):
        return self.data['from']['language_code']

    def get_message_id(self):
        return self.data['from']['message_id']

    def get_text(self):
        return self.data['text']
