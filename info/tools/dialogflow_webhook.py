import warnings


class WebhookHandler:
    """
    This Class Handles the Parsing of Dialogflow Requests and get details like Intent, Parameters, Session ID etc

    :param request: The Dialogflow Request
    """

    def __init__(self, request_dict):
        self.data = request_dict

    def set_source(self, platform):
        self.data["originalDetectIntentRequest"]["source"] = platform

    def get_intent(self):
        """
        Returns the Intent Dictionary which triggered the Webhook

        :raises TypeError: This Error is Raised if the Intent Dictionary can't be retrieved
        if the Request JSON is Malformed
        :return: Intent Object
        :rtype: dict
        """
        try:
            return self.data["queryResult"]["intent"]
        except KeyError:
            raise TypeError("Malformed Request JSON: Failed to find Intent JSON")

    def get_intent_name(self):
        """
        Returns the Intent Name which triggered the Webhook

        :raises TypeError: This Error is Raised if the Intent Name can't be retrieved if the Request JSON is Malformed
        :return: Intent Name
        :rtype: str
        """
        try:
            return self.data["queryResult"]["intent"]["name"]
        except KeyError:
            raise TypeError("Malformed Request JSON: Failed to find Intent Name")

    def get_intent_display_name(self):
        """
        Returns the Intent Display Name (this is the Intent Name which you would have specified
        in Dialogflow) which triggered the Webhook

        :raises TypeError: This Error is Raised if the Intent Display Name can't be retrieved
        if the Request JSON is Malformed
        :return: Intent Display Name
        :rtype: str
        """
        try:
            return self.data["queryResult"]["intent"]["displayName"]
        except KeyError:
            raise TypeError("Malformed Request JSON: Failed to find Intent Display Name")

    def get_parameters(self):
        """
        Returns a Dictionary of filled Parameter Values

        :return: Parameter Object
        :rtype: dict
        """
        try:
            return self.data["queryResult"]["parameters"]
        except KeyError:
            return {}

    def get_parameter(self, param):
        """
        Returns a Parameter Value by Parameter Name

        :param param: The Parameter name to retrive the Value
        :raises KeyError: This Error is Rasied if the Parameter is not found
        :return: Parameter Value
        :rtype: str
        """
        try:
            return self.data["queryResult"]["parameters"][param]
        except KeyError:
            raise KeyError("Parameter " + param + " not found")

    def get_action(self):
        """
        Returns the Action Name Specified for the Intent

        :return: Action Name
        :rtype: str
        """
        try:
            return self.data["queryResult"]["action"]
        except KeyError:
            return ""

    def get_session_id(self):
        """
        Returns the Session ID of the Dialogflow Session

        :raises TypeError: This Error is Raised if the Session ID can't be retived if the Request JSON is Malformed
        :return: Session ID
        :rtype: str
        """
        try:
            return self.data["session"]
        except KeyError:
            raise TypeError("Malformed Request JSON: Failed to find Session ID")

    def get_context_by_name(self, context_name):
        """
        Returns a Context Dictionary by Context Name

        :param context_name: The Context Name to retrive the Context JSON
        :type context_name: str
        :raises LookupError: This Error is Raised if The Context is not found
        :return: Context Object
        :rtype: dict
        """
        data = {}
        for i in self.data["queryResult"]["outputContexts"]:
            if i["name"].split("/")[len(i["name"].split("/")) - 1] == context_name:
                data = i
                break
        if data == {}:
            raise LookupError("Context with name " + context_name + " not found!")
        else:
            return data

    def get_capabilities(self):
        """
        Returns a list Google Assistant Capabilities for a particular surface
        (eg. Smart Display, Mobile Phone, Chromebook etc.) from where the bot is accessed.

        :return: Capabilities List
        :rtype: list

        .. note:: This Feature is specific only for Google Assistant. This will return an empty
        list if the bot is accessed from platforms which are not Google Assistant
        """
        try:
            retjson = []
            for i in self.data["originalDetectIntentRequest"]["payload"]["surface"]["capabilities"]:
                retjson.append(i["name"])
            return retjson
        except KeyError:
            return []

    def get_payload(self):
        """
        Returns the Platform Specific Payload from where the request originated

        :return: Payload Object
        :rtype: dict
        """
        try:
            return self.data["originalDetectIntentRequest"]["payload"]
        except KeyError:
            return {}

    def get_source(self):
        """
        Returns the source where the request originated

        :return: Source where the request originated
        :rtype: str
        """
        try:
            return self.data["originalDetectIntentRequest"]["source"]
        except KeyError:
            return ""

    def get_fulfillment_text(self):
        try:
            return self.data["queryResult"]["fulfillmentText"]
        except KeyError:
            return ""


class WebhookResponse:
    """
    The Class handles the creation of Dialogflow Responses

    .. note:: There are 2 types of Rich Responses which can be created using this class.
    They are: Generic Rich Responses and Google Assistant Rich Responses.
    Generic Responses work on all platforms except Google Assistant.
    Functions that create generic responses start with 'generic'.
    For Google Assistant, you should use Google Assistant Rich Responses.
    These functions start with 'google_assistant'
    """

    def __init__(self):
        """
        Constructor
        """
        self.card_btn_list = []
        self.g_suggestions_list = []
        self.response_data = []
        self.generic_messages = []
        self.context_list = []
        self.generic_card_index = -1
        self.g_carousel_index = -1
        self.g_table_index = -1
        self.g_permission_available = False
        self.g_end_conversation = None
        self.fulfilment_text_available = False
        self.event_available = False
        self.context_available = False
        self.g_card_added = False
        self.trigger_event_name = None
        self.trigger_event_parameters = None
        self.trigger_lang_code = None
        self.event_available = None
        self.fulfilment_text = None
        self.fulfilment_data = None

    def add_context(self, session_id, context_name, lifespan=0, params=""):
        """
        Adds or Changes a Dialogflow Context
        :param session_id: The Session ID
        :type session_id: str
        :param context_name: The name of the Context to add/edit
        :type context_name: str
        :param lifespan: The  number of conversational turns for which the context remains active, defaults to 0
        :type lifespan: int, optional
        """
        self.context_list.append(
            {"name": session_id + "/contexts/" + context_name, "lifespanCount": lifespan, "parameters": params or {}})
        self.context_available = True

    def trigger_event(self, event, params, lang_code="ru-RU"):
        """
        Triggers a Dialogflow Event

        :param event: The Name of the Event to Trigger
        :type event: str
        :param params: The Dictionary of Parameters
        :type params: dict
        :param lang_code: The Language Code of the Agent, defaults to "ru-RU"
        :type lang_code: str, optional

        .. note:: When the response contains event, other things are ignored (except Contexts)
        """
        self.trigger_event_name = event
        self.trigger_event_parameters = params
        self.trigger_lang_code = lang_code
        self.event_available = True

    def simple_response(self, speech):
        """
        A Generic Text to be displayed or told to the user.

        :param speech: The Text to be displayed or said to the user
        :type speech: str

        .. note:: ``simple_response`` works on all platforms including Google Assistant.
        However, it is recommended to use ``google_assistant_response`` for Google Assistant
        and ``generic_rich_text_response`` for text responses on other platforms.
        """
        self.fulfilment_text = speech
        self.fulfilment_text_available = True

    def generic_rich_text_response(self, text):
        """
        A Generic Rich Text Response to display to the user. Unlike ``generic_response``,
        you can have multiple ``generic_rich_text_response``

        :param text: The Text to be displayed to the user
        :type text: str
        """
        self.generic_messages.append({"text": {"text": [text]}})

    def generic_card(self, title, **kwargs):
        """
        A Generic Card to be displayed to the user

        :param title: The Title of the Card
        :type title: str
        :param subtitle: The Subtitle of the Card
        :type subtitle: str, optional
        :param image_url: The Link of the Image to be displayed on the card
        :type image_url: str, optional
        """
        img_url = kwargs.get("image_url", "")
        subtitle = kwargs.get("subtitle", "")
        if img_url == "":
            data = {
                "card": {
                    "title": title,
                    "subtitle": subtitle,
                },
            }
        else:
            data = {
                "card": {
                    "title": title,
                    "subtitle": subtitle,
                    "imageUri": img_url,
                },
            }
        self.generic_messages.append(data)
        self.generic_card_index = len(self.generic_messages) - 1

    def generic_card_add_button(self, btn_title, btn_link):
        """
        Adds a button to a Generic Card. When clicked, directs to a website

        :param btn_title: The button's title
        :type btn_title: str
        :param btn_link: The link to redirect to on click
        :type btn_link: str
        :raises AttributeError: This Error is Raised if a new button is added before calling ``generic_card``
        """
        if self.generic_card_index == -1:
            raise AttributeError("generic_card is not created")
        else:
            try:
                self.generic_messages[self.generic_card_index]["card"]["buttons"].append({
                    "text": btn_title,
                    "postback": btn_link,
                })
            except KeyError:
                self.generic_messages[self.generic_card_index]["card"]["buttons"] = []
                self.generic_messages[self.generic_card_index]["card"]["buttons"].append({
                    "text": btn_title,
                    "postback": btn_link,
                })

    def generic_add_suggestions(self, suggestion_list, **kwargs):
        """
        Adds Suggestion Chips/Quick Replies to be displayed.

        :param suggestion_list: The List of Suggestions/Quick Replies
        :type suggestion_list: list
        :param title: The title of the Suggestions
        :type suggestion_list: str, optional
        """
        title = kwargs.get("title", "")
        self.generic_messages.append({
            "quickReplies": {
                "title": title,
                "quickReplies": suggestion_list,
            },
        })

    def generic_image(self, image_url, image_alt):
        """
        Sends an Image to the User

        :param image_url: The URL of the Image
        :type image_url: str
        :param image_alt: The Alt Text for the Image
        :type image_alt: str
        """
        self.generic_messages.append({
            "image": {
                "imageUri": image_url,
                "accessibility_text": image_alt,
            },
        })

    def google_assistant_response(self, speech, **kwargs):
        """
        A Google Assistant speech to be said (and displayed) to the user

        :param speech: The Text to be said to the user
        :type speech: str
        :param displayText: The text to be displayed in the chat bubble while telling the speech
        :type displayText: str, optional
        :param endConversation: Specifies wheather this response should end the conversation or not
        :type endConversation: bool

        .. note:: This MUST Before any Google Assistant Rich Response.
        Failing to do so will result in an error in Google Assistant
        """
        tts = speech
        display_text = kwargs.get("displayText", "")
        self.g_end_conversation = kwargs.get("endConversation", False)
        if display_text != "":
            self.response_data.append({
                "simpleResponse": {
                    "textToSpeech": tts,
                    "displayText": display_text,
                },
            })
        else:
            self.response_data.append({
                "simpleResponse": {
                    "textToSpeech": tts,
                },
            })

    def google_assistant_card(self, title, **kwargs):
        """
        A Google Assistant Card to be displayed to the user

        :param title: The Title of the Card
        :type title: str

        :param subtitle: The subtitle of the Card
        :type subtitle: str, optional

        :param formatted_text: The text to be displayed along with the card
        :type formatted_text: str, optional

        :param btnName: The Name of the button to be displayed on the card
        :type btnName: str, optional

        :param btn_link: The link to redirect on button click
        :type btn_link: str, optional

        :param image_url: The URL of the image to be displayed on the card
        :type image_url: str, optional

        :param imageAlt: The Alt Text of the image to be displayed on the card
        :type imageAlt: str, optional

        :param imageDisplayOption: The Display options for the image
        (`Click here For a list of image display options
        <https://developers.google.com/assistant/conversational/webhook/reference/rest/Shared.Types/ImageDisplayOptions>`_)
        :type imageDisplayOption: str, optional
        """
        if self.g_card_added:
            warnings.warn(
                "You can have only one Google Assistant Card. "
                "More than one cards will lead to an error in Google Assistant")
            return
        self.g_card_added = True
        card_title = title
        card_subtitle = kwargs.get("subtitle", "")
        card_text = kwargs.get("formatted_text", "")
        card_button = kwargs.get("btn_name", "")
        card_url = kwargs.get("btn_link", "")
        img_url = kwargs.get("image_url", "")
        image_alt = kwargs.get("image_alt", "")
        image_display_options = kwargs.get("imageDisplayOption", "")
        if card_button == "":
            card = {
                "basicCard": {
                    "title": card_title,
                    "subtitle": card_subtitle,
                    "formattedText": card_text,
                },
            }
        else:
            card = {
                "basicCard": {
                    "title": card_title,
                    "subtitle": card_subtitle,
                    "formattedText": card_text,
                    "buttons": [{
                        "title": card_button,
                        "openUrlAction": {
                            "url": card_url,
                        },
                    }],
                },
            }
        if img_url != "":
            card["basicCard"]["image"] = {
                "url": img_url,
                "accessibilityText": image_alt,
            }
        if image_display_options != "":
            card["basicCard"]["imageDisplayOptions"] = image_display_options
        self.response_data.append(card)

    def google_assistant_new_carousel(self):
        """
        Creates a New Google Assistant Carousel
        """
        if self.g_carousel_index != -1:
            warnings.warn(
                "You can have only one Google Assistant Carousel. "
                "More than one Carousels will lead to an error in Google Assistant")
            return
        self.response_data.append({"carouselBrowse": {"items": []}})
        self.g_carousel_index = len(self.response_data) - 1

    def google_assistant_carousel_add_item(self, title, url, image_url, image_alt, description="", footer=""):
        """
        Adds a new item to a Google Assistant Carousel

        :param title: The title of the carousel item
        :type title: str
        :param url: The URL to redirect to when the Carousel item is clicked
        :type url: str
        :param image_url: The URL of the image to be displayed on the caarousel item
        :type image_url: str
        :param image_alt: The Alt text of the image to be displayed on the caarousel item
        :type image_alt: str
        :param description: The description to be displayed on the carousel item, defaults to ""
        :type description: str, optional
        :param footer: The footer to be displayed on the carousel item, defaults to ""
        :type footer: str, optional
        :raises AttributeError: This Error is raised if a new item is added before calling ``google_assistant_new_carousel``
        """
        try:
            self.response_data[self.g_carousel_index]["carouselBrowse"]["items"].append({
                "title": title,
                "openUrlAction": {
                    "url": url,
                }, "description": description,
                "footer": footer,
                "image": {
                    "url": image_url,
                    "accessibilityText": image_alt,
                },
            })
        except KeyError:
            raise AttributeError("google_assistant_new_carousel is not created")

    def google_assistant_add_suggestions(self, suggestion_list):
        """
        Adds Google Assistant Suggestion Chips to be displayed

        :param suggestion_list: The list containing the suggestions to be displayed
        :type suggestion_list: list
        """
        for i in suggestion_list:
            self.g_suggestions_list.append({"title": i})

    def google_assistant_new_table(self, **kwargs):
        """
        Creates a new Google Assistant Table Card

        :param title: The title of the Table Card
        :type title: str, optional

        :param subtitle: The subtitle of the Table Card
        :type subtitle: str, optional

        :param image_url: The URL of the image to be displayed on the table card
        :type image_url: str, optional

        :param imageAlt: The Alt text of the image to be displayed on the table card
        :type imageAlt: str, optional
        """
        if self.g_table_index != -1:
            warnings.warn("You can have only one Google Assistant Table. "
                          "More than one Tables will lead to an error in Google Assistant")
            return
        img_url = kwargs.get("imageURL", "")
        img_alt = kwargs.get("imageAlt", "")
        tab_title = kwargs.get("title", "")
        tab_subtitle = kwargs.get("subtitle", "")
        card = {
            "tableCard": {
                "rows": [],
                "columnProperties": [],
            },
        }
        if img_url != "":
            image = {
                "url": img_url,
                "accessibilityText": img_alt,
            }
            card["tableCard"]["image"] = image
        if tab_title != "":
            card["tableCard"]["title"] = tab_title
        if tab_subtitle != "":
            card["tableCard"]["subtitle"] = tab_subtitle
        self.response_data.append(card)
        self.g_table_index = self.response_data.index(card)

    def google_assistant_table_add_header_row(self, header_list):
        """
        Adds a Header row to a Google Assistant Table Card

        :param header_list: The list containing the header rows to be added
        :type header_list: list
        :raises AttributeError: This Error is raised if a header row is added before calling ``google_assistant_new_table``
        """
        try:
            for i in header_list:
                self.response_data[self.g_table_index]["tableCard"]["columnProperties"].append({"header": i})
        except KeyError:
            raise AttributeError("google_assistant_new_table is not created")

    def google_assistant_table_add_row(self, cell_list, add_divider):
        """
        Adds a new row to a Google Assistant Table Card

        :param cell_list: The list containing the rows to be added
        :type cell_list: list
        :param add_divider: Specifies if a divider should be added after the row
        :type add_divider: bool
        :raises AttributeError: This Error is raised if a row is added before calling ``google_assistant_new_table``
        """
        try:
            table_list = []
            for i in cell_list:
                table_list.append({"text": i})
            self.response_data[self.g_table_index]["tableCard"]["rows"].append({
                "cells": table_list,
                "dividerAfter": add_divider,
            })
        except KeyError:
            raise AttributeError("google_assistant_new_table is not created")

    def google_assistant_media_response(self, media_url, description, display_name, **kwargs):
        """
        Creates a Google Assistant Media Response to play music

        :param media_url: The URL where the music is located
        :type media_url: str
        :param description: The description of the music
        :type description: str
        :param display_name: The name of the music to display
        :type display_name: str
        :param image_url: The URL of the image to be displayed along with the media response
        :type image_url: str,optional
        :param image_alt: The Alt Text of the image to be displayed along with the media response
        :type image_alt: str,optional
        """
        img_url = kwargs.get("image_url", "")
        img_alt = kwargs.get("image_alt", "")
        self.response_data.append({
            "mediaResponse": {
                "mediaType": "AUDIO",
                "mediaObjects": [{
                    "contentUrl": media_url,
                    "description": description,
                    "icon": {
                        "url": img_url,
                        "accessibilityText": img_alt,
                    },
                    "name": display_name,
                }],
            },
        })

    def google_assistant_ask_permission(self, speech, permission_list):
        """
        Asks for permission from user in Google Assistant to get details like User's real name and address

        :param speech: The reason for the Permisssion Request
        :type speech: str
        :param permission_list: The list of Permissions to get from the user
        :type permission_list: list
        """
        self.permission_data = {
            "intent": "actions.intent.PERMISSION",
            "data": {
                "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                "optContext": speech,
                "permissions": permission_list,
            },
        }
        self.g_permission_available = True

    def create_final_response(self):
        """
        Creates the Final Response JSON to be sent back to Dialogflow

        :raises AttributeError: This error is raised if you try to insert Google Assistant Suggestions
        to a Google Assistant Rich Response with no items
        :return: The Response JSON
        :rtype: Dictionary
        """
        self.fulfilment_data = {}
        if not self.g_end_conversation:
            expectres = True
        else:
            expectres = False

        # Contexts
        if self.context_available:
            self.fulfilment_data["outputContexts"] = self.context_list

        # Event Trigger
        if self.event_available:
            self.fulfilment_data = {
                "followupEventInput": {
                    "name": self.trigger_event_name,
                    "parameters": self.trigger_event_parameters,
                    "languageCode": self.trigger_lang_code,
                },
            }
            return self.fulfilment_data

        # Generic Responses
        if self.fulfilment_text_available:
            self.fulfilment_data = {
                "fulfillmentText": self.fulfilment_text,
            }
        if self.generic_messages:
            self.fulfilment_data["fulfillmentMessages"] = self.generic_messages

        # Google Assistant Responses
        if self.response_data:
            if list(self.response_data[0].keys())[0] != "simpleResponse":
                warnings.warn("google_assistant_response() should have been called before adding a "
                              "Google Assistant Card,Carousel,Table etc. This is a limitation of "
                              "Google Assistant where the first response must be a simple text",
                              )
            self.fulfilment_data["payload"] = {
                "google": {
                    "expectUserResponse": expectres,
                    "richResponse": {
                        "items": self.response_data,
                    },
                },
            }
        if self.g_suggestions_list:
            try:
                self.fulfilment_data["payload"]["google"]["richResponse"]["suggestions"] = self.g_suggestions_list
            except KeyError:
                raise AttributeError(
                    "You are trying to insert suggestions into a Google Assistant Rich Response "
                    "with no items. This will lead to an error in Actions on Google",
                )
        if self.g_permission_available:
            if self.response_data:
                self.fulfilment_data["payload"]["google"]["systemIntent"] = self.permission_data
            else:
                self.fulfilment_data["payload"] = {
                    "google": {
                        "expectUserResponse": expectres,
                        "systemIntent": self.permission_data,
                    },
                }
        return self.fulfilment_data
