# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
# from rasa_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class Actionsayname(Action):

    def name(self) -> Text:
        return "action_sayname"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # text = tracker.latest_message['text']

        current_name = next(tracker.get_latest_entity_values("name"), None)
        print(current_name)

        if not current_name:
            msg = f"Name not recognized. Please enter properly"
            print(msg)
            dispatcher.utter_message(text = msg)
            return []
        
        msg = f"Hey {current_name}. Nice to see you!"
        print(msg)
        dispatcher.utter_message(text = msg)

        return [SlotSet("name", current_name)]
        # return [SlotSet("name", text)]

class Actiondisplay(Action):

    def name(self) -> Text:
        return "action_display"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")

        if not name:
            msg = f"oops. Please enter properly"
            print(msg)
            dispatcher.utter_message(text = msg)
            return []
        
        msg = f"Repeated: Your name is {name}. Nice to see you!"
        print(msg)
        dispatcher.utter_message(text = msg)

        return []


class Actionsetbeginstatustrue(Action):
    def name(self) -> Text:
        return "action_set_begin_status_true"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return[SlotSet("begin_status", True)]

class Actionqueryfresh(Action):

    def name(self) -> Text:
        return "action_query_fresh"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
    