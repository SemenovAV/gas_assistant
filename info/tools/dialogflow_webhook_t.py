from typing import Optional, Any
from pydantic import Field, BaseModel, root_validator, AnyUrl, PositiveInt


class Text(BaseModel):
    """
    Возвращает текстовый ответ.
    """
    text: Optional[list[str]] = Field(
        description="Список ответов агента",
    )


class Image(BaseModel):
    """
    Изображение.

    """
    image_uri: Optional[AnyUrl] = Field(
        alias='imageUri',
        description="Ссылка на файл изображения.",
    )
    accessibility_text: Optional[str] = Field(
        alias='accessibilityText',
        description='Описание изображения',
    )


class QuickReplies(BaseModel):
    """
    Коллекция быстрых ответов.
    """
    title: Optional[str] = Field(
        description='Название коллекции быстрых ответов',
    )
    quick_replies: Optional[list[str]] = Field(
        description='Коллекция быстрых ответов',
    )


class Button(BaseModel):
    """
    Кнопка
    """
    text: Optional[str] = Field(
        description='Текст кнопки',
    )
    postback: Optional[str] = Field(
        description='Текст или ссылка - ответ серверу. Реакция на нажатие кнопки',
    )


class GoogleActionSimpleResponse(BaseModel):
    """
    Быстрый ответ для Google Action
    """
    text_to_speech: Optional[str] = Field(
        alias='textToSpeech',
        description='Текстовый ответ для произношения голосом.',
    )
    ssml: Optional[str] = Field(
        description='Ответ в формате SSML',
    )
    display_text: Optional[str] = Field(
        alias='displayText',
        description='Текст для показа',
    )

    @root_validator(allow_reuse=True)
    def ssml_or_text_to_speech(cls, values):  # noqa
        if 'ssml' not in values or values['ssml'] is None or 'text_to_speech' not in values or values['text_to_speech'] is None:
            return values
        raise ValueError('One of text_to_speech or ssml must be provided.')


class Card(BaseModel):
    """
    Карточка.
    """
    title: Optional[str] = Field(
        description='Заголовок карточки',
    )
    subtitle: Optional[str] = Field(
        description='Подзаголовок карточки',
    )
    image_uri: Optional[AnyUrl] = Field(
        alias='imageUri',
        description='Ссылка на файл изображения',
    )
    buttons: Optional[list[Button]] = Field(
        description='Коллекция кнопок',
    )


class GoogleActionBasicCard(Card):
    """
    Ответ для Google Action.
    Базовая карточка сообщения. Полезно для отображения информации.
    """
    formatted_text: Optional[str] = Field(
        alias="formattedText",
        description='Текст карточки',
    )

    @root_validator(allow_reuse=True)
    def formatted_text_or_image(cls, values):  # noqa
        if 'formatted_text' not in values or values['formatted_text'] is None and 'image' not in values or values[
                'image'] is None:
            raise ValueError('formatted_text required, unless image is present.')
        return values


class GoogleActionSuggestion(BaseModel):
    """
    Сообщение — подсказка, которое пользователь может нажать, чтобы быстро опубликовать ответ в беседе.
    """
    title: str = Field(
        description='Текст для показа в подсказке',
    )


class GoogleActionLinkOutSuggestion(BaseModel):
    """
    Подсказка — ссылка, которое позволяет пользователю перейти к приложению или веб-сайту, связанному с этим агентом.
    """
    destination_name: str = Field(
        alias='destinationName',
        description='Название приложения или сайта на которое ссылается подсказка.',
    )
    uri: AnyUrl = Field(
        description='URI приложения или сайта, который открывается, когда пользователь нажимает на подсказку.',
    )


class SelectItemInfo(BaseModel):
    """
    Дополнительная информация об этой опции.
    """
    key: str = Field(
        description='Уникальный ключ, который будет отправлен обратно агенту, если будет выбран этот ответ.',
    )
    synonyms: Optional[list[str]] = Field(
        description='Список синонимов, которые также можно использовать для вызова этого элемента в диалоговом окне.',
    )


class SelectItem(BaseModel):
    """
    Элемент списка опций.
    """
    info: SelectItemInfo
    title: str = Field(
        description='Заголовок',
    )
    description: Optional[str] = Field(
        description='Описание опции',
    )
    image: Optional[Image]


class GoogleActionsListSelect(BaseModel):
    """
    Карточка — список опций для Google Action.
    """
    title: Optional[str] = Field(
        description='Заголовок',
    )
    items: list[SelectItem] = Field(
        description='Коллекция элементов списка',
    )
    subtitle: Optional[str] = Field(
        description='Подзаголовок',
    )


class GoogleActionCarouselSelect(BaseModel):
    """
    Карточка - карусель опций.
    """
    items: list[SelectItem] = Field(
        description='Коллекция элементов карусели.',
    )


class Message(BaseModel):
    platform: Optional[str] = Field(
        description='Используемая платформа.',
    )
    text: Optional[Text]
    image: Optional[Image]
    payload: Optional[dict] = Field(
        description='Настраиваемый, специфичный для каждой платформы. ответ.',
    )
    simple_responses: Optional[list[GoogleActionSimpleResponse]] = Field(
        alias='simpleResponses',
        description='Коллекция быстрых ответов для Google Actions',
    )
    basic_card: Optional[GoogleActionBasicCard] = Field(
        alias='basicCard',
    )
    suggestions: Optional[list[GoogleActionSuggestion]] = Field(
        description='Коллекция подсказок для Google Actions',
    )
    link_out_suggestion: Optional[GoogleActionLinkOutSuggestion] = Field(
        alias='linkOutSuggestion',
    )
    list_select: Optional[GoogleActionsListSelect] = Field(
        alias='listSelect',
    )
    carousel_select: Optional[GoogleActionCarouselSelect] = Field(
        alias='carouselSelect',
    )


class OriginalDetectIntentRequest(BaseModel):
    """
    Представляет содержимое исходного запроса, переданного вызову [Streaming] DetectIntent.
    """
    source: Optional[str] = Field(
        description='Источник этого запроса, например, google, facebook, slack. '
                    'Он устанавливается серверами, принадлежащими Dialogflow.',
    )
    version: Optional[str] = Field(
        description='Версия протокола, используемого для этого запроса. Это поле специфично для Google Actions',
    )
    payload: Optional[dict] = Field(
        description='В этом поле устанавливается значение поля QueryParameters.payload, '
                    'переданное в запросе. Некоторые интеграции, которые запрашивают агент Dialogflow,'
                    ' могут предоставлять дополнительную информацию в полезной нагрузке.',
    )


class Intent(BaseModel):
    """
    Намерение.
    """
    name: str = Field(
        description='Уникальный идентификатор намерения.',
    )
    display_name: str = Field(
        alias='displayName',
        description='Название этого намерения.',
    )
    end_interaction: Optional[bool] = Field(
        alias='endInteraction',
        description='Указывает, что это намерение завершает взаимодействие.'
                    ' Некоторые интеграции (например, Actions on Google или телефонный шлюз Dialogflow)'
                    ' используют эту информацию для тесного взаимодействия с конечным пользователем. '
                    'По умолчанию - false.',
    )
    is_fallback: Optional[bool] = Field(
        description='Указывает, является ли это резервным намерением.',
    )


class Context(BaseModel):
    """
    Контекст диалога.
    """
    name: str = Field(
        description='Идентификатор контекста.',
    )
    lifespan_count: Optional[PositiveInt] = Field(
        alias='lifespanCount',
        description='Количество диалоговых запросов,'
                    ' после которых истекает контекст. По умолчанию - 0.'
                    ' Если установлено значение 0, контекст немедленно истекает.'
                    ' Контексты автоматически удаляются через 20 минут,'
                    ' если нет подходящих запросов.',
    )
    parameters: Optional[dict] = Field(
        description='Коллекция извлеченных параметров',
    )


class QueryResult(BaseModel):
    """
    Результат обработки запроса
    """
    action: Optional[str] = Field(
        description='Название действия из совпадающего намерения.',
    )
    parameters: Optional[dict] = Field(
        description='Коллекция извлеченных параметров',
    )
    intent: Intent = Field(
        description='Намерение, которое соответcтвует запросу.',
    )
    all_required_params_present: Optional[bool] = Field(
        alias='allRequiredParamsPresent',
        description='True - если собраны все требуемые значения параметров'
                    ' или если совпадающее намерение не содержит каких-либо'
                    ' обязательных параметров.',
    )
    cancels_slot_filling: Optional[bool] = Field(
        alias='cancelsSlotFilling',
        description='Указывает, вызывает ли диалоговый запрос отмену заполнения слота.',

    )
    query_text: str = Field(
        alias='queryText',
        description='Исходный текст запроса',
    )
    fulfillment_text: str = Field(
        alias='fulfillmentText',
        description='текст, который будет произнесен пользователю или показан на экране. '
                    'Примечание. Это устаревшее поле, предпочтение следует '
                    'отдавать fulfillment_messages.',
    )
    fulfillment_messages: list[Message] = Field(
        alias='fulfillmentMessages',
        description='Коллекция сообщений.',
    )
    webhook_source: Optional[str] = Field(
        alias='webhookSource',
        description='Если запрос был выполнен вызовом веб-перехватчика, '
                    'в этом поле устанавливается значение исходного поля,'
                    ' возвращенного в ответе веб-перехватчика.',
    )
    webhook_payload: Optional[dict] = Field(
        alias='webhookPayload',
        description='Если запрос был выполнен с помощью вызова веб-перехватчика,'
                    ' в этом поле устанавливается значение поля полезной нагрузки,'
                    ' возвращенное в ответе веб-перехватчика.',
    )
    output_contexts: list[Context] = Field(
        alias='outputContexts',
        description='Коллекция контекстов диалога',
    )
    intent_detection_confidence: Optional[float] = Field(
        alias='intentDetectionConfidence',
        description='Уверенность обнаружения намерения.',
        ge=0.0,
        le=1.0,
    )
    diagnostic_info: Optional[dict] = Field(
        alias='diagnosticInfo',
        description='Диагностическая информация',
    )
    language_code: str = Field(
        alias='languageCode',
        description="Код языка",
    )

    class Config:
        extra = 'allow'


class WebhookRequest(BaseModel):
    """
    Запрос от Dialogflow.
    """
    response_id: str = Field(
        alias='responseId',
        description='Уникальный идентификатор ответа.',
    )

    session: str = Field(
        description='Уникальный идентификатор сеанса.',
    )
    original_detect_intent_request: OriginalDetectIntentRequest = Field(
        alias='originalDetectIntentRequest',
    )
    query_result: QueryResult = Field(
        alias='queryResult',
    )


class EventInput(BaseModel):
    """
    События позволяют сопоставлять намерения по имени события вместо ввода на естественном языке.
    Например, input <event: {name: "welcome_event", parameters: {name: "Sam"}}> может вызвать
    персонализированный приветственный ответ. Имя параметра может использоваться агентом в ответе:
    «Здравствуйте, #welcome_event.name! Чем я могу вам помочь сегодня?».
    """
    name: str = Field(
        description='Уникальный идентификатор события.',
    )
    parameters: dict = Field(
        description='Коллекция параметров, связанных с событием.',
    )
    language_code: str = Field(
        description='Язык этого запроса.',
    )


class Entity(BaseModel):
    """
    Сущность
    """
    value: str = Field(
        description='Основное значение, связанное с этой записью объекта. '
                    'Например, если тип объекта - овощ, значением может быть зеленый лук.',
    )
    synonyms: list[str] = Field(
        description='Коллекция синонимов значений. Например, если тип объекта - овощ, '
                    'а значение - томат, синонимом может быть помидор.',
    )


class SessionEntityTypes(BaseModel):
    """

    Сеанс представляет собой беседу между агентом Dialogflow и конечный пользователь.
    Во время сеанса можно создавать специальные сущности, называемые сущностями сеанса.
    Сущности сеансов могут расширять или заменять пользовательские типы сущностей и
    существовать только во время сеанса, для которого они были созданы.
    Все данные сеанса, включая сущности сеансов, хранятся Dialogflow в течение 20 минут.
    """
    name: str = Field(
        description='Уникальный идентификатор этого типа сущности сеанса.',
    )
    entity_override_mode: Any = Field(
        alias='entityOverrideMode',
        description='Указывает, должны ли дополнительные данные заменять '
                    'или дополнять определение настраиваемого типа сущности.',
    )
    entities: list[Entity] = Field(
        description='Коллекция сущностей, связанных с этим типом сущности сеанса.',
    )


class WebhookResponse(BaseModel):
    """

    Ответное сообщение на вызов веб-перехватчика.
    Этот ответ подтверждается сервером Dialogflow.
    Если проверка не удалась, в поле QueryResult.diagnostic_info будет возвращена ошибка.
    Установка в полях JSON пустого значения неправильного типа — распространенная ошибка.

    """
    fulfillment_text: Optional[str] = Field(
        alias='fulfillmentText',
        description='Текстовое ответное сообщение, '
                    'предназначенное для конечного пользователя. '
                    'Вместо этого рекомендуется использовать perform_messages.text.text[0].',
    )
    fulfillment_messages: list[Message] = Field(
        alias='fulfillmentMessages',
        description='Коллекция сообщений с расширенными ответами, '
                    'предназначенные для конечного пользователя. '
                    'Если указано, Dialogflow использует это поле '
                    'для заполнения QueryResult.fulfillment_messages, '
                    'отправленных вызывающей стороне интеграцией или API.',
    )

    source: Optional[str] = Field(
        description='Настраиваемое поле, используемое для определения '
                    'источника веб-перехватчика. Поддерживаются произвольные строки. '
                    'Если указано, Dialogflow использует это поле для заполнения '
                    'QueryResult.webhook_source, отправляемого вызывающей стороне интеграции или API.',
    )
    payload: Optional[dict] = Field(
        description='Это поле можно использовать для передачи пользовательских данных'
                    ' из вашего веб-перехватчика вызывающей стороне интеграции или API.',
    )
    output_contexts: Optional[list[Context]] = Field(
        alias='outputContexts',
        description='Коллекция выходных контекстов, '
                    'которые перезаписывают текущие активные контексты для сеанса '
                    'и сбрасывают их продолжительность жизни. Если указано, '
                    'Dialogflow использует это поле для заполнения QueryResult.output_contexts, '
                    'отправленных вызывающей стороне интеграции или API.',
    )
    followup_event_input: Optional[EventInput] = Field(
        alias='followupEventInput',
        description='Вызывает указанные события. Когда это поле установлено, Dialogflow игнорирует'
                    'fulfillment_text, fulfillment_messages, и payload ',
    )
    live_agent_handoff: Optional[bool] = Field(
        alias='liveAAgentHandoff',
        default=False,
        description='Указывает, что должен быть задействован активный '
                    'агент для обработки взаимодействия с пользователем. '
                    'В большинстве случаев, когда вы устанавливаете этот флаг '
                    'в значение true, вы также можете установить для end_interaction'
                    ' значение true. По умолчанию - false.',
    )
    end_interaction: Optional[bool] = Field(
        alias='endInteraction',
        default=False,
        description='Указывает, что это намерение завершает взаимодействие.'
                    ' Некоторые интеграции (например, Actions on Google или телефонный шлюз Dialogflow)'
                    ' используют эту информацию для тесного взаимодействия с конечным пользователем.'
                    ' По умолчанию - false.',
    )
    session_entity_types: Optional[list[SessionEntityTypes]] = Field(
        alias='sessionEntityTypes',
        description='Дополнительные типы сущностей сеанса для замены или расширения '
                    'типов сущностей разработчика.',
    )
