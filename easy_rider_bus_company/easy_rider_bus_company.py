# Write your code here
import json
from collections import defaultdict

json_str = json.loads(input())
dct = defaultdict(int)
keys = []
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


print(f'Type and required field validation: {sum(dct.values())} errors')
for key in pack.keys():
    print(f'{key}: {dct[key]}')


