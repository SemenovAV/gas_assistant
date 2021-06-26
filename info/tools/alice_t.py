import re
from typing import Optional, Union, Literal

from pydantic import BaseModel, Field, Json, validator, AnyUrl


class Interfaces(BaseModel):
    """
    Интерфейсы, доступные на устройстве пользователя.
    """
    screen: Optional[dict] = Field(
        description='Пользователь может видеть ответ навыка на экране и открывать ссылки в браузере.',
    )
    account_linking: Optional[dict] = Field(
        description='У пользователя есть возможность запросить связку аккаунтов.',
    )
    payments: Optional[dict]


class User(BaseModel):
    """
    Атрибуты пользователя Яндекса, который взаимодействует с навыком.
    Если пользователь не авторизован в приложении, свойства user в запросе не будет.
    """
    user_id: str = Field(
        description='Идентификатор пользователя Яндекса, единый для всех приложений и устройств.'
                    'Этот идентификатор уникален для пары «пользователь — навык»: в разных навыках '
                    'значение свойства user_id для одного и того же пользователя будет различаться.',
    )
    access_token: Optional[Json] = Field(
        description='Токен для OAuth-авторизации, который также передается в заголовке Authorization'
                    ' для навыков с настроенной связкой аккаунтов.',
    )


class Application(BaseModel):
    """
    Данные о приложении, с помощью которого пользователь взаимодействует с навыком.
    """
    application_id: str = Field(
        description='Идентификатор экземпляра приложения, в котором пользователь общается с Алисой.'
                    'Уникален для пары «приложение — навык»',
    )


class Session(BaseModel):
    """
    Данные о сессии.
    Сессия — это период относительно непрерывного взаимодействия пользователя с навыком. Сессия прерывается:

    - когда пользователь запрашивает выход из навыка;
    - когда навык явно завершает работу ("end_session": true);
    - когда от пользователя долго не поступает команд (таймаут зависит от поверхности, минимум несколько минут).
    """
    session_id: str = Field(
        description='Уникальный идентификатор сессии',
        max_length=64,
    )
    message_id: float = Field(
        description='Идентификатор сообщения в рамках сессии. '
                    'Инкрементируется с каждым следующим запросом.',
    )
    skill_id: str = Field(
        description='Идентификатор вызываемого навыка, присвоенный при создании.',
    )
    user_id: Optional[str] = Field(
        description='Свойство перестает поддерживаться — вместо него следует использовать новое, '
                    'полностью аналогичное свойство session.application.application_id.',
    )
    use: Optional[User]
    application: Application
    new: bool = Field(
        description='Признак новой сессии',
    )


class Meta(BaseModel):
    """
    Информация об устройстве, с помощью которого пользователь разговаривает с Алисой.
    """
    locale: str = Field(
        description='Язык в POSIX-формате.',
        max_length=64,
    )
    timezone: str = Field(
        description='Название часового пояса, включая алиасы.',
        max_length=64,
    )
    client_id: str = Field(
        description='Идентификатор устройства и приложения, в котором идет разговор.'
                    'Не рекомендуется к использованию.Интерфейсы, доступные на клиентском устройстве, '
                    'перечислены в свойстве interfaces.',
        max_length=1024,
    )
    interfaces: Interfaces


class Markup(BaseModel):
    """
    Формальные характеристики реплики, которые удалось выделить Яндекс.Диалогам.
    Отсутствует, если ни одно из вложенных свойств не применимо.
    """
    dangerous_context: Optional[bool] = Field(
        description='Признак реплики, которая содержит криминальный подтекст '
                    '(самоубийство, разжигание ненависти, угрозы).',
    )


class Tokens(BaseModel):
    """
    Обозначение начала и конца именованной сущности в массиве слов. Нумерация слов в массиве начинается с 0.
    """
    start: int = Field(
        description='Первое слово именованной сущности.',
    )
    end: int = Field(
        description='Первое слово после именованной сущности.',
    )


class Entities(BaseModel):
    """
    Именованная сущность.
    """
    tokens: Tokens
    elem_type: str = Field(
        description='Тип именованной сущности',
        alias='type',
    )
    value: dict = Field(
        description='Формальное описание именованной сущности.',
    )


class Nlu(BaseModel):
    """
    Слова и именованные сущности, которые Диалоги извлекли из запроса пользователя.
    """
    tokens: list[str] = Field(
        description='Массив слов из произнесенной пользователем фразы.',
    )
    entities: list[Entities] = Field(
        description='Массив именованных сущностей.',
    )


class Request(BaseModel):
    """
    Данные, полученные от пользователя.
    """
    command: Optional[str] = Field(
        description='Служебное поле: запрос пользователя, преобразованный для внутренней обработки Алисы.',
    )
    original_utterance: Optional[str] = Field(
        description='Полный текст пользовательского запроса.',
        max_length=1024,
    )
    elem_type: Union[Literal['SimpleUtterance'], Literal['ButtonPressed']] = Field(
        description='Тип ввода.'
                    '"SimpleUtterance" — голосовой ввод;'
                    '"ButtonPressed" — нажатие кнопки.',
        alias='type',
    )
    markup: Optional[Markup]
    payload: Optional[Json] = Field(
        description='JSON, полученный с нажатой кнопкой от обработчика навыка (в ответе на предыдущий запрос).'
                    'Максимум 4096 байт.',
    )
    nlu: Nlu


class AliceRequest(BaseModel):
    """
    Получив реплику пользователя, Яндекс.Диалоги отправляют POST-запрос на Webhook URL, указанный при публикации.
    """
    meta: Meta
    session: Session
    request: Request
    version: str = Field(
        description='Версия протокола.',
    )


class Button(BaseModel):
    text: Optional[str] = Field(
        description='Текст, который будет отправлен навыку по '
                    'нажатию на изображение в качестве команды пользователя.'
                    'Если свойство передано с пустым значением, свойство request.command в запросе '
                    'будет отправлено пустым.Если свойство не передано в ответе, '
                    'Диалоги используют вместо него свойство response.card.title.',
        max_length=64,

    )
    url: Optional[AnyUrl] = Field(
        description='URL, который должно открывать нажатие по изображению.',
    )
    payload: Optional[Json] = Field(
        description='Произвольный JSON, который Яндекс.Диалоги должны отправить обработчику, '
                    'если пользователь нажмет на изображение. Максимум 4096 байт.',
    )


class AbilityToHideButtonMixin(BaseModel):
    """
    Добавляет возможность скрыть кнопку
    """
    hide: bool = Field(
        description='Признак того, что кнопку нужно убрать после следующей реплики пользователя.',
    )


class AbilityToHideButton(Button, AbilityToHideButtonMixin):
    pass


class Header(BaseModel):
    """
    Заголовок списка изображений.
    """
    text: str = Field(
        description='Текст заголовка.',
        max_length=64,
    )


class Image(BaseModel):
    """
    Изображение
    """
    image_id: Optional[str] = Field(
        description='Идентификатор изображения, который возвращается в ответ на запрос загрузки.',

    )
    title: Optional[str] = Field(
        description='Заголовок для изображения.',
        max_length=128,
    )
    description: Optional[str] = Field(
        description='Описание изображения.',
        max_length=256,
    )
    button: Optional[Button] = Field(
        description='Свойства изображения, на которое можно нажать.',
    )


class ImageCollection(BaseModel):
    """
    Коллекция изображений
    """

    items: list[Image] = Field(
        description='Набор изображений.Игнорируется для типа карточки BigImage.',
    )


class BigImage(Image):
    """
    Карточка — одно большое изображение
    """
    elem_type: Literal['BigImage'] = Field(
        alias='type',
    )


class Footer(BaseModel):
    """
    Кнопки под списком изображений.
    """
    text: str = Field(
        description='Текст первой кнопки.',
        max_length=64,
    )
    button: Optional[Button] = Field(
        description='Дополнительная кнопка для списка изображений.',
    )


class ItemsList(ImageCollection):
    """
    Карточка — список изображений.
    """
    elem_type: Literal['ListItems'] = Field(
        alias='type',
    )
    header: Header = Field(
        description='Заголовок списка изображений.',
    )
    footer: Footer

    @validator('items', allow_reuse=True)
    def check_list_items(cls, v): # noqa
        length = len(v)
        if 1 < length < 5:
            return v
        raise ValueError('ImageGallery: Количество изображений должно быть не больше 5')


class ImageGallery(ImageCollection):
    elem_type: Literal['ImageGallery'] = Field(
        alias='type',
    )

    @validator('items', allow_reuse=True)
    def check_gallery_items(cls, v): # noqa
        length = len(v)
        if 1 < length < 7:
            return v
        raise ValueError('ImageGallery: Количество изображений должно быть не больше 7')


class Response(BaseModel):
    """
    Данные для ответа пользователю.
    """
    text: str = Field(
        description='Текст, который следует показать и сказать пользователю.Не должен быть пустым.',
        max_length=1024,
    )
    tts: Optional[str] = Field(
        description='Ответ в формате TTS (text-to-speech)',
    )
    card: Optional[Union[BigImage, ImageGallery, ItemsList]]
    buttons: list[AbilityToHideButton] = Field(
        description='Кнопки, которые следует показать пользователю.'
                    'Все указанные кнопки выводятся после основного ответа Алисы, '
                    'описанного в свойствах response.text и response.card. '
                    'Кнопки можно использовать как релевантные ответу ссылки '
                    'или подсказки для продолжения разговора.',
    )
    end_session: bool = Field(
        description='Признак конца разговора.',
    )

    @validator('tts', allow_reuse=True)
    def check_tts(cls, value): # noqa
        pattern = re.compile(r'<speaker [\w=\"|\' ]*>')
        s = re.sub(pattern, '', value)
        length = len(s)
        if length > 1024:
            raise ValueError(f'tts: длинна: {length}: Длинна, без учета тегов, не должна превышать 1024. ')
        return value

    @validator('text', allow_reuse=True)
    def check_text(cls, value): # noqa
        if len(value.strip()) == 0:
            raise ValueError('text: Не должно быть пустым.')
        return value


class Event(BaseModel):
    """
    Событие
    """
    name: str = Field(
        description='Название события',
    )
    value: Json = Field(
        description='JSON-объект для многоуровневых событий. '
                    'Допустимо не более пяти уровней вложенности события.'
                    'Многоуровневые события передаются через пары key:value.',
    )


class Analytics(BaseModel):
    """
    Объект с данными для аналитики. Доступен навыкам с подключенным параметром Настройки AppMetrica.
    """
    events: list[Event] = Field(
        description='Массив событий',
    )


class AliceResponse(BaseModel):
    """
    Обработчик навыка должен ответить на полученный от Яндекс.Диалогов запрос.
    Примечание. Время ожидания ответа от навыка — 3 секунды.
    Если Диалоги не получат ответ в течение этого времени,
    сессия навыка завершится.
    Алиса сообщит пользователю, что навык не отвечает.
    """
    response: Response
    analytics: Optional[Analytics]
