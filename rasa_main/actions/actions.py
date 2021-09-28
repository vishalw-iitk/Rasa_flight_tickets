# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import sys
import numpy as np
sys.path.append('../..')
from Flights_API import amadeus

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

class Actionshowpreview(Action):
    def name(self) -> Text:
        return "action_show_preview"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        all_names = tracker.get_slot("full_name")
        contact_number = tracker.get_slot("contact_number")
        originLocationName = tracker.get_slot("from_location")
        destinationLocationName = tracker.get_slot("to_location")
        departureDate = tracker.get_slot("departureDate")
        returnDate = tracker.get_slot("returnDate")
        adults = num_tickets = tracker.get_slot("adults")
        nonStop = tracker.get_slot("nonStop")
        budget = tracker.get_slot("maxPrice")
        num_of_tickets = adults
        
        # originLocationName= 'BOM'
        # destinationLocationName= 'CCU'
        # departureDate= '2021-11-10' #YEAR-MONTH-DATE
        # returnDate= '2021-11-11' #YEAR-MONTH-DATE
        # adults='1'
        # nonStop= 'false'
        # maxPrice= '300' 


        final_response = amadeus.run(originLocationName, destinationLocationName, departureDate,\
                                returnDate, adults, nonStop, budget)
        
        final_response['data'][0]['direction'][0 and 1]['segment']['all']
        
        # seg_res = final_response['data'][ticket_id]['direction'][direction]['segment'][segment_number]
        
        # seg_res['origin']
        # seg_res['destination']
        # seg_res['origin_iata_code']
        # seg_res['destination_iata_code']
        # seg_res['departure_date']
        # seg_res['departure_time']
        # seg_res['arrival_date']
        # seg_res['arrival_time']
        # np.round(seg_res['price'], 1)
        # seg_res['flight_code']
        # seg_res['aircraft_code']
        # seg_res['duration']
        # seg_res['num_of_stops']
        # seg_res['cabin']
        # seg_res['origin_airportname']
        # seg_res['destination_airportname']
        # seg_res['origin_GMT']
        # seg_res['destination_GMT']
        # seg_res['numberOfBookableSeats']
        # seg_res['gate_number']
        # seg_res['seat_number']

        preview_message = f'We have received the info for {num_of_tickets} tickets as requested by you\n'
        preview_message += 'These are names of ticket holders\n'
        all_names = all_names.split(';')
        for name in all_names:
            preview_message += f'{name}\n'
        preview_message += 'Here is the preview for the complete journey of any one of you\n'
        # #for loop
        # for ticket_id in range(0, num_of_tickets):
        for ticket_id in range(0,1):
            num_of_directions = len(final_response['data'][ticket_id]['direction'])
            for direction in range(num_of_directions):
                num_of_segments = len(final_response['data'][ticket_id]['direction'][direction]['segment'])
                for segment in range(num_of_segments):
                    segment_response = final_response['data'][ticket_id]['direction'][direction]['segment'][segment]
                    sr = segment_response
                    origin, destination, origin_iata_code, destination_iata_code, departure_date, departure_time, \
                        arrival_date, arrival_time, price, flight_code, aircraft_code, duration, \
                            num_of_stops, cabin, origin_airportname, destination_airportname, origin_GMT, destination_GMT, \
                                numberOfBookableSeats, gate_number, seat_number = \
                    sr['origin'], sr['destination'], sr['origin_iata_code'], sr['destination_iata_code'], sr['departure_date'], sr['departure_time'], \
                        sr['arrival_date'], sr['arrival_time'], np.round(sr['price'], 1), sr['flight_code'], sr['aircraft_code'], sr['duration'], \
                            sr['num_of_stops'], sr['cabin'],sr['origin_airportname'], sr['destination_airportname'], sr['origin_GMT'], sr['destination_GMT'], \
                                sr['numberOfBookableSeats'], sr['gate_number'], sr['seat_number']
                                
                    preview_message += f'contact number : {contact_number}\n'
                    preview_message += f'contact number : {origin}\n'
                    preview_message += f'contact number : {destination}\n'
                    preview_message += f'contact number : {origin_iata_code}\n'
                    preview_message += f'contact number : {destination_iata_code}\n'
                    preview_message += f'contact number : {departure_date}\n'
                    preview_message += f'contact number : {departure_time}\n'
                    preview_message += f'contact number : {arrival_date}\n'
                    preview_message += f'contact number : {arrival_time}\n'
                    preview_message += f'contact number : {price}\n'
                    preview_message += f'contact number : {flight_code}\n'
                    preview_message += f'contact number : {aircraft_code}\n'
                    preview_message += f'contact number : {duration}\n'
                    preview_message += f'contact number : {num_of_stops}\n'
                    preview_message += f'contact number : {cabin}\n'
                    preview_message += f'contact number : {origin_airportname}\n'
                    preview_message += f'contact number : {destination_airportname}\n'
                    preview_message += f'contact number : {origin_GMT}\n'
                    preview_message += f'contact number : {destination_GMT}\n'
                    preview_message += f'contact number : {numberOfBookableSeats}\n'
                    preview_message += f'contact number : {gate_number}\n'
                    preview_message += f'contact number : {seat_number}\n'
                    preview_message += f'contact number : {contact_number}\n'
                    preview_message += f'contact number : {contact_number}\n'
        #             # ---------
        # preview_message += 'Let me know if should confirm this\n'
        # preview_message += 'Tickets for all of you will be booked\n'

        # preview_message += 'Total number of stops in direction {} : {}\n' #for loop
        # preview_message += 'Total duration for direction {} : {}\n' #for loop
        # preview_message += 'Your grand total is {}\n'
        
        dispatcher.utter_message(text=preview_message)
        
        confirm_message = "Congrats.!!! Your ticket is booked successfully"

        return[SlotSet('confirm_message', confirm_message)]


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
    

class Actiongetnames(Action):
    def name(self) -> Text:
        return "action_get_names"
    def update_name(self, traveller_name):
        self.name_list = []
        self.ticket_number = 0
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        num_of_tickets = tracker.get_slot("adults")
        name = tracker.get_slot("full_name")
        self.ticket_number += 1
    
        if len(self.name_list) < num_of_tickets:
            dispatcher.utter_message(text=f"Provide the name of passenger {self.ticket_number}")
            self.name_list.append(name)
            return[SlotSet("full_name", None)]
        else:
            all_names = ''
            for name in self.name_list:
                all_names += name+';'
            all_names = all_names[:-1]
            return[SlotSet("full_name", all_names)]

        # return [AllSlotsReset()]
# class Actiongetcontact(Action):
#     def name(self) -> Text:
#         return "action_get_contact"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        