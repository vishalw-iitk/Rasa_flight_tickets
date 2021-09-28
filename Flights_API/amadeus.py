import requests
import json
from dotenv import load_dotenv
import argparse
import random
import os
import sys

load_dotenv()

sys.path.append('..')

def get_oauth_headers():
    oauth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return oauth_headers

def get_oauth_keys(grant_type, client_id, client_secret):
    oauth_keys = {
        'grant_type': grant_type,
        'client_id': client_id,
        'client_secret': client_secret
    }
    return oauth_keys

def get_oauth_response(oauth_url, oauth_headers, oauth_keys):
    oauth_response = requests.post(oauth_url, headers=oauth_headers, data=oauth_keys).json()
    return oauth_response

def get_oauth_token(oauth_response, access_token_key):
    access_token = oauth_response[access_token_key]
    return access_token

def get_headers(token):
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    return headers

# def get_from_slot(*args):
    # for argslot in args:
        # something

def get_iata_code(dict_cityname, cityname):
    if len(cityname) == 3:
        return cityname.upper()
    return dict_cityname["data"][cityname.lower()]['code']
def get_city_name(dict_citycode, citycode):
    return dict_citycode["data"][citycode]['city']

def get_api_and_params(opt):
    originLocationCode, destinationLocationCode, departureDate, returnDate, adults, nonStop, maxPrice = \
        opt.originLocationCode, opt.destinationLocationCode, opt.departureDate, opt.returnDate, opt.adults, opt.nonStop, opt.maxPrice
    # api = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'
    # params = (
        # ('origin', 'PAR'),
        # ('maxPrice', '200'),
    # )
    # def get_from_slot(slot_name):
        # slot_value = get_from_actions(slot_name)
        # required_value = get_from_mapping(slot_value)
        # return required_value
    api = 'https://test.api.amadeus.com/v2/shopping/flight-offers'


    # originLocationCode = get_from_slot(from_location)
    # destinationLocationCode = get_from_slot(to_location)
    # departureDate = get_from_slot(departuedate)
    # returnDate = get_from_slot(returndate)
    # adults = get_from_slot(adults)
    # nonStop = get_from_slot(nonstop)
    # maxPrice = get_from_slot(maxprice)

    # args = ('from_location', 'to_location', 'departuredate', 'returndate', 'adults', 'nonstop', 'maxprice')
    # originLocationCode, destinationLocationCode, departureDate,\
    #  returnDate, adults, nonStop, maxPrice\
    #  = get_from_slot(*args)
    

    params = (
        ('originLocationCode', originLocationCode),
        ('destinationLocationCode', destinationLocationCode),
        ('departureDate', departureDate), #YEAR-MONTH-DATE
        ('returnDate', returnDate), #YEAR-MONTH-DATE
        ('adults', adults),
        ('nonStop', nonStop),
        ('maxPrice', maxPrice)
        # ('currencies', 'EUR'),
    )

    return api, params

def get_response(api, headers, params):
    response = requests.get(api, headers=headers, params=params).json()
    # response = requests.get(api+'?origin=PAR&maxPrice=200', headers=headers).json()
    # response = requests.get(api+'?originLocationCode=PAR&destinationLocationCode=MAD&departureDate=2021-11-03&returnDate=2021-11-10&adults=1&nonStop=false&maxPrice=200', headers=headers).json()
    return response

def get_response_data(response, data_key):
    return response[data_key]
def get_flight_code(carrierCode, number):
    return carrierCode + str(number)
def provide_output_to_slots(final_response):
    print(final_response)
def print_length_of_response_firstdataponits(response_data):
    print("number of datapoint : ", len(response_data[0]))
def print_response_firstdatapoint(response_data):
    print(response_data[0])

def add_more_response_manually(gate_number, segment_response):
    segment_response['gate_number'] = gate_number
    seatlist = ['A', 'B', 'C', 'D', 'E', 'F']
    segment_response['seat_number'] = str(random.randint(1,100)) + random.choice(seatlist)
    return segment_response


def to_inr(conv_rate, amount):
    return amount * conv_rate
def to_euro(conv_rate, amount):
    return amount / conv_rate


def get_required_response(opt, dict_citycode, ticket_id, direction, response_data):
    # response_data[i]['itineraries'][j]['segments'][k]
    # i = ticket_id; j = 0 if oneway, 1 if twoway; k = number of stops in a single way
    segment_resp = {"segment" : []}
    # required_response = 
    num_of_segments = len(response_data[ticket_id]['itineraries'][direction]['segments'])
    for segment in range(0, num_of_segments):
        segment_response = {}

        segment_response['origin_iata_code'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['departure']['iataCode']
        segment_response['destination_iata_code'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['arrival']['iataCode']
    
        segment_response['origin'] = dict_citycode["data"][segment_response['origin_iata_code']]['city']
        segment_response['destination'] = dict_citycode["data"][segment_response['destination_iata_code']]['city']

        segment_response['departure_at'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['departure']['at']
        segment_response['departure_date'] = segment_response['departure_at'][:10]
        segment_response['departure_time'] = segment_response['departure_at'][10:]
        segment_response['arrival_at'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['arrival']['at']
        segment_response['arrival_date'] = segment_response['arrival_at'][:10]
        segment_response['arrival_time'] = segment_response['arrival_at'][10:]
        del segment_response['departure_at']
        del segment_response['arrival_at']

        segment_response['price'] = to_inr(opt.conv_rate, float(response_data[ticket_id]['price']['total']))
        segment_response['flight_code'] = get_flight_code(response_data[ticket_id]['itineraries'][direction]['segments'][segment]['carrierCode'], \
                                            response_data[ticket_id]['itineraries'][direction]['segments'][segment]['number'])
        segment_response['aircraft_code'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['aircraft']['code']
        segment_response['duration'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['duration'][2:]
        segment_response['num_of_stops'] = num_of_segments - 1
        segment_response['cabin'] = response_data[ticket_id]['travelerPricings'][0]['fareDetailsBySegment'][segment]['cabin']
        

        segment_response['origin_airportname'] = dict_citycode["data"][segment_response['origin_iata_code']]['airportname']
        segment_response['destination_airportname'] = dict_citycode["data"][segment_response['destination_iata_code']]['airportname']
        segment_response['origin_GMT'] = dict_citycode["data"][segment_response['origin_iata_code']]['gmt']
        segment_response['destination_GMT'] = dict_citycode["data"][segment_response['destination_iata_code']]['gmt']

        segment_response['numberOfBookableSeats'] = response_data[ticket_id]['numberOfBookableSeats']


        gate_number = random.randint(0,50)
        segment_response = add_more_response_manually(gate_number, segment_response)

        segment_resp["segment"].append(segment_response)

    return segment_resp


def parse_opt(known = False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--conv-rate', type=float, default=86.17, help=' EUR to INR currency conversion rate i.e. EUR = conv_rate * INR')
    parser.add_argument('--originLocationName', type=str, default='mumbai', help='origin airport IATA code')
    parser.add_argument('--destinationLocationName', type=str, default='NAGpur', help='destination airport IATA code')
    parser.add_argument('--departureDate', type=str, default='2021-11-10', help='date of onboarding')
    parser.add_argument('--returnDate', type=str, default='2021-11-11', help='date of onboarding')
    parser.add_argument('--adults', type=str, default='1', help='number of tickets')
    parser.add_argument('--nonStop', type=str, default='false', help='requirement of nonStop flight')
    parser.add_argument('--maxPrice', type=str, default='10000', help='maxPrice in INR for the total journey')
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

def run(**kwargs):
    opt = parse_opt(True)
    for k, v in kwargs.items():
        setattr(opt, k, v)
    return main(opt)

def main(opt):
    oauth_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    oauth_headers = get_oauth_headers()
    grant_type = 'client_credentials'
    client_id = os.getenv('API_KEY', 'api key from amadeus')
    client_secret = os.getenv('API_SECRET', 'api secret from amadeus')
    oauth_keys = get_oauth_keys(grant_type, client_id, client_secret)
    oauth_response = get_oauth_response(oauth_url, oauth_headers, oauth_keys)
    print("oauth_response", oauth_response)
    access_token_key = 'access_token'
    token = get_oauth_token(oauth_response, access_token_key)
    print("token", token)
    headers = get_headers(token)

    # with open('dict_cityname.json') as json_file:
    with open('../Flights_API/dict_cityname.json') as json_file:
        dict_cityname = json.load(json_file)
    opt.originLocationCode = get_iata_code(dict_cityname, opt.originLocationName)
    opt.destinationLocationCode = get_iata_code(dict_cityname, opt.destinationLocationName)

    api, params = get_api_and_params(opt)
    response = get_response(api, headers, params)
    # print(response)
    data_key = 'data'
    response_data = get_response_data(response, data_key)

    # with open('dict_citycode.json') as json_file:
    with open('../Flights_API/dict_citycode.json') as json_file:
        dict_citycode = json.load(json_file)

    opt.originLocationName = get_city_name(dict_citycode, opt.originLocationCode)
    opt.destinationLocationName = get_city_name(dict_citycode, opt.destinationLocationCode)

    opt.maxPrice = to_euro(opt.conv_rate, float(opt.maxPrice))

    final_response = {"data" : []}
    num_of_directions = 2 # 1 or 2
    for ticket_id in range(0, int(opt.adults)):
        direction_response = {"direction" : []}
        for direction in range(0, num_of_directions):
            segment_response = get_required_response(opt, dict_citycode, ticket_id, direction, response_data)
            direction_response["direction"].append(segment_response)
        final_response["data"].append(direction_response)
    # print("in amadeus", final_response)
    # provide_output_to_slots(final_response)
    # print(100*"*")
    # print_length_of_response_firstdataponits(response_data)
    # print(100*"*")
    # print_response_firstdatapoint(response_data)

    return final_response


if "__main__" == __name__:
    opt = parse_opt(True)
    main(opt)

# requesting for
# ('originLocationCode', 'BOM'),
# ('destinationLocationCode', 'CCU'),
# ('departureDate', '2021-11-10'), #YEAR-MONTH-DATE
# ('returnDate', '2021-11-11'), #YEAR-MONTH-DATE
# ('adults', '1'),
# ('nonStop', 'false'),
# ('maxPrice', '300'),

# current
# name, mob. no.
# from, to
# date, time

# Hey. Please book a ticket for me from BOM to CCU

# Hey. Please book a ticket for me from BOM to CCU on 12/12/12

# # Hey. Please book a ticket for me from BOM to CCU
# bot: On which date?

# # Hey. Please book a ticket for me from BOM
# bot: to where
# bot: On which date?

# # Hey. Please book a ticket for me from BOM
# bot: to where
# CCU on 12/12/12





# 

# departuredate

# final_response = {
    #     "data" : [
    #         {
    #             "direction" : [
    #                 {
    #                     "segment" : [
    #                         {},
    #                         {}
    #                     ]
    #                 }
    #             ]
    #     }
    #     ]
    # }

# 1 ticket
{
    'data': [
            {
                'direction': [
                    {
                        'segment': [
                            {
                                'numberOfBookableSeats': 9,
                                'departure_at': '2021-11-10T06:10:00',
                                'arrival_at': '2021-11-10T08:50:00',
                                'price': 6903.0787,
                                'flight_code': 'AI675',
                                'aircraft_code': '32A',
                                'duration': '2H40M',
                                'num_of_stops': 1,
                                'cabin': 'ECONOMY',
                                'gate_number': 17,
                                'seat_number': '59D'
                            }
                        ]
                    },
                    {
                        'segment': [
                                {
                                    'numberOfBookableSeats': 9,
                                    'departure_at': '2021-11-11T09:25:00',
                                    'arrival_at': '2021-11-11T12:25:00',
                                    'price': 6903.0787,
                                    'flight_code': 'AI676',
                                    'aircraft_code': '32A',
                                    'duration': '3H',
                                    'num_of_stops': 1,
                                    'cabin': 'ECONOMY',
                                    'gate_number': 17,
                                    'seat_number': '96A'
                                }
                        ]
                    }
                ]
            }
    ]
}
####################################
# 2 tickets
{
    'data': [
        {
            'direction': [
                {
                    'segment': [
                        {
                            'numberOfBookableSeats': 9,
                            'departure_at': '2021-11-10T06:10:00',
                            'arrival_at': '2021-11-10T08:50:00',
                            'price': 13806.1574,
                            'flight_code': 'AI675',
                            'aircraft_code': '32A',
                            'duration': '2H40M',
                            'num_of_stops': 1,
                            'cabin': 'ECONOMY',
                            'gate_number': 9,
                            'seat_number': '7D'
                        }
                    ]
                },
                {
                    'segment': [
                        {
                            'numberOfBookableSeats': 9,
                            'departure_at': '2021-11-11T09:25:00',
                            'arrival_at': '2021-11-11T12:25:00',
                            'price': 13806.1574,
                            'flight_code': 'AI676',
                            'aircraft_code': '32A',
                            'duration': '3H',
                            'num_of_stops': 1,
                            'cabin': 'ECONOMY',
                            'gate_number': 18,
                            'seat_number': '3C'
                        }
                    ]
                }
            ]
        },
        {
            'direction': [
                {
                    'segment': [
                        {
                            'numberOfBookableSeats': 9,
                            'departure_at': '2021-11-10T06:10:00',
                            'arrival_at': '2021-11-10T08:50:00',
                            'price': 13806.1574,
                            'flight_code': 'AI675',
                            'aircraft_code': '32A',
                            'duration': '2H40M',
                            'num_of_stops': 1,
                            'cabin': 'ECONOMY',
                            'gate_number': 38,
                            'seat_number': '24A'
                        }
                    ]
                },
                {
                    'segment': [
                        {
                            'numberOfBookableSeats': 9,
                            'departure_at': '2021-11-11T19:40:00',
                            'arrival_at': '2021-11-11T23:25:00',
                            'price': 13806.1574,
                            'flight_code': 'AI732',
                            'aircraft_code': '32B',
                            'duration': '3H45M',
                            'num_of_stops': 1, 
                            'cabin': 'ECONOMY',
                            'gate_number': 18, 
                            'seat_number': '0D'
                        }
                    ]
                }
            ]
        }
    ]
}

# ############
{
    'data': [
        {
            'direction': [
                {
                    'segment': [
                        {
                            'origin': 'Mumbai',
                            'destination': 'Nagpur',
                            'origin_iata_code': 'BOM',
                            'destination_iata_code': 'NAG',
                            'departure_date': '2021-11-10',
                            'departure_time': 'T19:00:00',
                            'arrival_date': 'T20:35:00',
                            'arrival_time': 'T20:35:00',
                            'price': 4760.8925,
                            'flight_code': 'AI629',
                            'aircraft_code': '321',
                            'duration': '1H35M',
                            'num_of_stops': 1,
                            'cabin': 'ECONOMY',
                            'origin_airportname': 'Chhatrapati Shivaji International',
                            'destination_airportname': 'Dr. Babasaheb Ambedkar International Airport',
                            'origin_GMT': '+5.5',
                            'destination_GMT': '+5.5',
                            'numberOfBookableSeats': 9,
                            'gate_number': 2,
                            'seat_number': '39C'
                        }
                    ]
                },
                {
                    'segment': [
                        {
                            'origin': 'Mumbai',
                            'destination': 'Nagpur',
                            'origin_iata_code': 'BOM',
                            'destination_iata_code': 'NAG',
                            'departure_date': '2021-11-11',
                            'departure_time': 'T07:55:00',
                            'arrival_date': 'T09:20:00',
                            'arrival_time': 'T09:20:00',
                            'price': 4760.8925,
                            'flight_code': 'AI628',
                            'aircraft_code': '32B',
                            'duration': '1H25M',
                            'num_of_stops': 1,
                            'cabin': 'ECONOMY',
                            'origin_airportname': 'Chhatrapati Shivaji International',
                            'destination_airportname': 'Dr. Babasaheb Ambedkar International Airport',
                            'origin_GMT': '+5.5',
                            'destination_GMT': '+5.5',
                            'numberOfBookableSeats': 9,
                            'gate_number': 22,
                            'seat_number': '45C'
                        }
                    ]
                }
            ]
        }
    ]
}