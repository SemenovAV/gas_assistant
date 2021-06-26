from __future__ import annotations
from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class NameMixin(BaseModel):
    first_name: Optional[str] = Field(
        description='Имя бота или пользователя',
    )
    last_name: Optional[str] = Field(
        description='Фамилия бота или пользователя',
    )


class UsernameMixin(BaseModel):
    username: Optional[str] = Field(
        description='Username пользователя или бота',
    )


class User(NameMixin, UsernameMixin):
    """
    Этот объект представляет бота или пользователя Telegram.
    """
    uid: int = Field(
        description='Уникальный идентификатор пользователя или бота',
        alias='id',
    )


class ChatType(str, Enum):
    """
    Тип чата
    """
    privat = 'privat'
    group = 'group'
    supergroup = 'supergroup'
    channel = 'channel'


class Chat(NameMixin, UsernameMixin):
    """
    Этот объект представляет собой чат.
    """
    uid: int = Field(
        description='Уникальный идентификатор чата.',
        alias='id',
        le=1e13,
        ge=0,
    )
    elem_type: str = Field(
        alias='type',
    )
    title: Optional[str] = Field(
        description='Название для каналов или групп',
    )
    all_members_are_administrators: Optional[bool] = Field(
        description='True, если все участники чата являются администраторами',
    )


class MessageEntityType(str, Enum):
    """
    Тип сущности.
    """
    mention = 'mention'
    hashtag = 'hashtag'
    bot_command = 'bot_command'
    url = 'url'
    email = 'email'
    bold = 'bold'
    italic = 'italic'
    code = 'code'
    pre = 'pre'
    text_link = 'text_link'


class MessageEntity(BaseModel):
    """
    Этот объект представляет одну из особых сущностей в текстовом сообщении.
    Например: хештеги, имена пользователей, ссылки итд.
    """
    elem_type: MessageEntityType = Field(
        alias='type',
    )
    offset: int = Field(
        description='Смещение в единицах кода UTF-16 до начала объекта',
    )
    length: int = Field(
        description='Длина объекта в кодовых единицах UTF-16',
    )
    url: Optional[str] = Field(
        description='Только для «text_link»: URL, который будет открыт после того,'
                    ' как пользователь нажмет на текст.',
    )


class File(BaseModel):
    file_id: str = Field(
        description='Уникальный идентификатор файла',
    )
    file_size: Optional[int] = Field(
        description='Размер файла',
    )


class MimeMixin(File):
    mime_type: Optional[str] = Field(
        description='MIME файла, заданный отправителем',
    )


class SizeMixin(BaseModel):
    width: int = Field(
        description='Ширина фото',
    )
    height: int = Field(
        description='Высота фото',
    )


class ThumbsMixin(BaseModel):
    thumb: Optional[PhotoSize]


class DurationMixin(BaseModel):
    duration: int = Field(
        description='Продолжительность звука в секундах, определенная отправителем',
    )


class Audio(DurationMixin, MimeMixin, File):
    """
    Информация об аудиофайле
    """

    performer: Optional[str] = Field(
        description='Исполнитель аудио, определенный отправителем или аудио тегами',
    )
    title: Optional[str] = Field(
        description='Название аудио, как определено отправителем или аудио тегами',
    )


class PhotoSize(SizeMixin, File):
    """
    Этот объект представляет изображение определённого размера или превью файла/стикера.
    """


class Document(MimeMixin, ThumbsMixin, File):
    """
    Этот объект представляет файл, не являющийся фотографией, голосовым сообщением или аудиозаписью.
    """

    file_name: Optional[str] = Field(
        description='Исходное имя файла, определенное отправителем',
    )


class Sticker(SizeMixin, ThumbsMixin, File):
    """
    Этот объект представляет стикер.
    """


class Video(MimeMixin, SizeMixin, DurationMixin, ThumbsMixin, File):
    """
    Этот объект представляет видеозапись.
    """


class Voice(MimeMixin, DurationMixin, File):
    """
    Этот объект представляет голосовое сообщение.
    """


class Contact(NameMixin):
    """
    Этот объект представляет контакт с номером телефона.
    """
    phone_number: str = Field(
        description='Номер телефона',
    )
    user_id: Optional[int] = Field(
        description='Идентификатор пользователя в Telegram',
    )


class Location(BaseModel):
    """
    Этот объект представляет точку на карте.
    """
    longitude: float = Field(
        description='Долгота, заданная отправителем',
    )
    latitude: float = Field(
        description='Широта, заданная отправителем',
    )


class Venue(BaseModel):
    """
    Этот объект представляет объект на карте.
    """
    location: Location = Field(
        description='Координаты объекта',
    )
    title: str = Field(
        description='Название объекта',
    )
    address: str = Field(
        description='Адрес объекта',
    )
    foursquare_id: Optional[str] = Field(
        description='Идентификатор объекта в Foursquare',
    )


class Message(BaseModel):
    """
    Этот объект представляет собой сообщение.
    """
    message_id: int = Field(
        description='Уникальный идентификатор сообщения',
    )
    from_user: Optional[User] = Field(
        alias='from',
        description='Отправитель. Может быть пустым в каналах.',
    )
    date: datetime = Field(
        description='Дата отправки сообщения',
    )
    chat: Chat = Field(
        description='Диалог, в котором было отправлено сообщение',
    )
    forward_from: Optional[User] = Field(
        description='Для пересланных сообщений: отправитель оригинального сообщения',
    )
    forward_date: Optional[datetime] = Field(
        description='Для пересланных сообщений: дата отправки оригинального сообщения',
    )
    reply_to_message: Optional[dict] = Field(
        description='Для ответов: оригинальное сообщение.',
    )
    text: Optional[str] = Field(
        description='Для текстовых сообщений: текст сообщения',
        min_length=0,
        max_length=4096,
    )
    entities: Optional[MessageEntity] = Field(
        description='Для текстовых сообщений: особые сущности в тексте сообщения.',
    )
    audio: Optional[Audio] = Field(
        description='Информация об аудиофайле',
    )
    document: Optional[Document] = Field(
        description='Информация о файле',
    )
    photo: Optional[list[PhotoSize]] = Field(
        description='Доступные размеры фото',
    )
    sticker: Optional[Sticker] = Field(
        description='ДИнформация о стикере',
    )
    video: Optional[Video] = Field(
        description='Информация о видеозаписи',
    )
    voice: Optional[Voice] = Field(
        description='Информация о голосовом сообщении',
    )
    caption: Optional[str] = Field(
        description='Подпись к файлу, фото или видео',
        min_length=0,
        max_length=200,
    )
    contact: Optional[Contact] = Field(
        description='Информация об отправленном контакте',
    )
    location: Optional[Location] = Field(
        description='Информация о местоположении',
    )
    venue: Optional[Venue] = Field(
        description='Информация о месте на карте',
    )
    new_chat_member: Optional[User] = Field(
        description='Информация о пользователе, добавленном в группу',
    )
    left_chat_member: Optional[User] = Field(
        description='Информация о пользователе, удалённом из группы',
    )
    new_chat_title: Optional[str] = Field(
        description='Название группы было изменено на это поле',
    )
    new_chat_photo: Optional[list[PhotoSize]] = Field(
        description='Фото группы было изменено на это поле',
    )
    delete_chat_photo: Optional[bool] = Field(
        description='Сервисное сообщение: фото группы было удалено',
    )
    group_chat_created: Optional[bool] = Field(
        description='Сервисное сообщение: группа создана',
    )
    supergroup_chat_created: Optional[bool] = Field(
        description='Сервисное сообщение: супергруппа создана',
    )
    channel_chat_created: Optional[bool] = Field(
        description='Сервисное сообщение: канал создан',
    )
    migrate_to_chat_id: Optional[int] = Field(
        description='Группа была преобразована в супергруппу с указанным идентификатором.',
        le=1e13,
    )
    migrate_from_chat_id: Optional[int] = Field(
        description='Супергруппа была создана из группы с указанным идентификатором.',
        le=1e13,
    )
    pinned_message: Optional[dict] = Field(
        description='Указанное сообщение было прикреплено.',
    )
