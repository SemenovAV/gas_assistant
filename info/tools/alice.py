import json


def is_alice(msg):
    source = msg.get_source()
    payload = msg.get_payload()
    return source == '' and 'meta' in payload and 'client_id' in payload['meta']


class AliceRequest(object):
    def __init__(self, request_dict):
        self._request_dict = request_dict

    @property
    def uid(self):
        return f'{self.application_id[0:9]}-{self.client_id}'

    @property
    def client_id(self):
        return self._request_dict['meta']['client_id']

    @property
    def locale(self):
        return self._request_dict['meta']['locale']

    @property
    def timezone(self):
        return self._request_dict['meta']['timezone']

    @property
    def interfaces(self):
        return self._request_dict['interfaces']

    @property
    def version(self):
        return self._request_dict['version']

    @property
    def session(self):
        return self._request_dict['session']

    @property
    def application_id(self):
        return self.session['application']['application_id']

    @property
    def session_id(self):
        return self.session['session_id']

    @property
    def user_id(self):
        return self.session['user']['user_id'] if 'user' in self.session else '00000000000'

    @property
    def is_new_session(self):
        return bool(self.session['new'])

    @property
    def command(self):
        return self._request_dict['request']['command']

    def __str__(self):
        return str(self._request_dict)


class AliceResponse(object):
    def __init__(self, alice_request):
        self._response_dict = {
            "version": alice_request.version,
            "session": alice_request.session,
            "response": {
                "end_session": False
            }
        }

    def dumps(self):
        return json.dumps(
            self._response_dict,
            ensure_ascii=False,
            indent=2
        )

    def set_text(self, text):
        self._response_dict['response']['text'] = text[:1024]

    def set_buttons(self, buttons):
        self._response_dict['response']['buttons'] = buttons

    def end(self):
        self._response_dict["response"]["end_session"] = True

    def __str__(self):
        return self.dumps()
