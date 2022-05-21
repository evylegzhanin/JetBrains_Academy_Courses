# Write your code here
import json
from collections import defaultdict
import re


def field_val(json_str):
    dct = defaultdict(int)
    for pack in json_str:
        for key, value in pack.items():
            if key == 'bus_id':
                if not isinstance(value, int):
                    dct[key] += 1
            if key == 'stop_id':
                if not isinstance(value, int):
                    dct[key] += 1
            if key == 'stop_name':
                if not (isinstance(value, str) and len(value) > 0):
                    dct[key] += 1
            if key == 'next_stop':
                if not isinstance(value, int):
                    dct[key] += 1
            if key == 'stop_type':
                if not isinstance(value, str):
                    dct[key] += 1
                else:
                    if len(value) > 1:
                        dct[key] += 1
            if key == 'a_time':
                if not (isinstance(value, str) and len(value) > 0):
                    dct[key] += 1
    return dct, pack


def format_val(json_str):
    dct = defaultdict(int)
    stops_set = '[A-Z].*(Road|Avenue|Boulevard|Street)$'
    for pack in json_str:
        for key, value in pack.items():
            if key == 'stop_name':
                if not re.match(stops_set, value):
                    dct[key] += 1
            if key == 'stop_type':
                if value not in set(['O', 'S', 'F', '']):
                    dct[key] += 1
            if key == 'a_time':
                template = '([0][0-9]|[1][0-9]|[2][0-3]):[0-5][0-9]$'
                if not re.match(template, value):
                    dct[key] += 1
    keys = ['stop_name', 'stop_type', 'a_time']
    return dct, keys


def stops_number(json_str):
    dct = defaultdict(int)
    for pack in json_str:
        dct[pack['bus_id']] += 1
    return dct


json_inp = json.loads(input())
dct_fields, keys = field_val(json_inp)
dct_format, keys_form = format_val(json_inp)
# print(f'Type and required field validation: {sum(dct_fields.values())} errors')
# for key in keys.keys():
#     print(f'{key}: {dct_fields[key]}')
# print(f'Format validation: {sum(dct_format.values())} errors')
# for key in keys_form:
#     print(f'{key}: {dct_format[key]}')
print(f'Line names and number of stops:')
dct_stops = stops_number(json_inp)
print(dct_stops)
# for key, value in sorted(dct_stops.items()):
#     print(f'bus_id: {key}, stops: {dct_format[key]}')


