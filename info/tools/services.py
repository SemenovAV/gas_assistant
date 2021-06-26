from abc import ABC, abstractmethod
from typing import Any
from django.http import HttpRequest

from info.tools.dialogflow_webhook_t import WebhookRequest


class Parameter(ABC):
    """
    Базовый класс. Реализует функционал работы с параметрами.
    """

    def __init__(self):
        self._raw_value = None
        self._value = None

    @property
    @abstractmethod
    def title(self) -> str:
        """
        Возвращает название параметра.
        """

    @property
    def raw_value(self) -> str:
        """
        Возвращает необработанное значение параметра
        """
        return self._raw_value

    @raw_value.setter
    def raw_value(self, value: str) -> None:
        self._raw_value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value


class BaseIntentHandler(ABC):
    """
    Базовый класс. Реализует интерфейс взаимодействия с Dialogflow.
    """

    def is_this_intent(self, name: str) -> bool:
        """
        Определяет возможность обработки сообщения.
        :param name: Название намерения обрабатываемого сообщения.
        :type name: str
        """
        this_name = self._intent_name
        return this_name == name

    @property
    @abstractmethod
    def _intent_name(self) -> str:
        """
        Свойство должно возвращать название намерения обработка которого возможна.
        :return: Название.
        :rtype: str
        """

    @abstractmethod
    def _get_params(self, params: dict) -> dict: # noqa
        """
        Метод должен реализовать обработку параметров сообщения.
        """

    @abstractmethod
    def _get_query_to_db(self) -> str:
        """
        Метод должен реализовать выполнение запросов к базе.
        """

    @abstractmethod
    def _create_response(self) -> str:
        """
        Метод должен реализовать сборку ответа.
        """


def detect_client(msg: dict) -> str:
    detect_intent = msg['original_detect_intent_request']
    if 'source' in detect_intent:
        return detect_intent['source']
    return 'alice'


def messages_handler(request: HttpRequest) -> dict:
    msg = WebhookRequest.parse_raw(request.body).dict(skip_defaults=True)
    detect_client(msg)
    return {}
