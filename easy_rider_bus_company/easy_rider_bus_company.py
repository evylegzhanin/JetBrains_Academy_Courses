import json
import re
import itertools


bus_id = 0

buses_dict = json.loads(input())

error_dict = {'bus_id': 0, 'stop_id': 0, 'stop_name': 0, 'next_stop': 0, 'stop_type': 0, 'a_time': 0}


def format_errors(b_dict):
    stop_name = 0
    stop_type = 0
    a_time = 0
    pat_stop_n = re.compile("[A-Z]{1}[a-z]{1,}\s?\w* (Street$|Boulevard$|Avenue$|Road$)")
    pat_stop_t = re.compile(r"\s\"[S|F|T|O|]\"")
    pat_a_time = re.compile("([01][0-9]|2[0-3]):[0-5][0-9]")
    for ele in b_dict:
        if not re.match(pat_stop_n, ele['stop_name']):
            stop_name += 1
        if not re.match(r"[SFTO]{1,2}|^$", ele['stop_type']) or len(ele['stop_type']) >= 2:
            stop_type += 1
        if not re.match(pat_a_time, str(ele['a_time'])) or len(ele['a_time']) != 5:
            a_time += 1
    total_errors = stop_type + stop_name + a_time
    print(f"Format validation: {total_errors} errors")
    print(f"stop_name: {stop_name}")
    print(f"stop_type: {stop_type}")
    print(f"a_time: {a_time}")


def field_validation(b_dict):
    for ele in buses_dict:
        if not isinstance(ele['bus_id'], int):
            error_dict['bus_id'] += 1
        if not isinstance(ele['stop_id'], int):
            error_dict['stop_id'] += 1
        if (not isinstance(ele['stop_name'], str)) or len(ele['stop_name']) < 2:
            error_dict['stop_name'] += 1
        if not isinstance(ele['next_stop'], int):
            error_dict['next_stop'] += 1
        if (not isinstance(ele['stop_type'], str)) or len(ele['stop_type']) > 1:
            error_dict['stop_type'] += 1
        if (not isinstance(ele['a_time'], str)) or len(ele['a_time']) < 1:
            error_dict['a_time'] += 1
    print(f"Type and required field validation: {sum(error_dict.values())} errors")
    for key in error_dict:
        print(key + ':', error_dict[key])


def bus_lines(b_dict):
    lines = {}
    for entry in b_dict:
        if str(entry['bus_id']) in lines.keys():
            lines[f"{entry['bus_id']}"]["stops"] += 1
        else:
            lines[f"{entry['bus_id']}"] = {"stops": 1}
    print("Line names and number of stops:")
    for k in lines:
        print("bus_id:", f"{k},", str(lines[k]).strip("{}'") )


def check_stops(b_dict):
    lines = {}
    for entry in b_dict:
        i = str(entry['bus_id'])
        if i not in lines.keys():
            #for k, v in lines.items():
            #if v != 2:
            #print(f"There is no start or end stop for the line: {k}.1")
            #return False
            if entry['stop_type'] == "S" or entry['stop_type'] == "F":
                lines[i] = 1
            else:
                lines[i] = 0
        else:
            if entry['stop_type'] == "S" or entry['stop_type'] == "F":
                lines[i] += 1
            else:
                pass
    for k, v in lines.items():
        if v != 2:
            print(f"There is no start or end stop for the line: {k}.2")
            return False


def transfer_stops(b_dict):
    lines = []
    for entry in b_dict:
        i = str(entry["bus_id"])
        name = entry["stop_name"]
        if i not in lines:
            lines.append(i)
            globals()[f'{i}'] = [name]
        else:
            globals()[f'{i}'].append(name)
    comb = []
    transfer = []
    for d in lines:
        comb += globals()[f"{d}"]
    for i in comb:
        if comb.count(i) >= 2:
            transfer.append(i)
            transfer.sort()
    transfer = set(transfer)
    global transfers
    transfers = list(transfer)


def special_stops(b_dict):
    start_stops = {}
    finish_stops = {}
    for entry in b_dict:
        s = str(entry['stop_type'])
        n = entry['stop_name']
        if s == 'S':
            if n in start_stops.keys():
                start_stops[n] = [start_stops[n], entry['bus_id']]
            else:
                start_stops[n] = entry['bus_id']
        if s == 'F':
            if n in finish_stops.keys():
                finish_stops[n] = [finish_stops[n], entry['bus_id']]
            else:
                finish_stops[n] = entry['bus_id']

    print('Start stops:', len(start_stops), sorted(list(start_stops.keys())))
    print('Transfer stops:', len(transfers), sorted(transfers))
    print('Finish stops:', len(finish_stops), sorted(list(finish_stops.keys())))


def check_arrival(dict):
    lines = {}
    errors = {}
    for entry in dict:
        i = str(entry["bus_id"])
        n = entry["stop_name"]
        t = entry["a_time"]
        if i not in lines.keys():
            lines[f"{i}"] = {"time": f"{t}"}
        elif i in lines.keys() and i not in errors.keys():
            if t > lines[f"{i}"]["time"]:
                lines[f"{i}"]["time"] = f"{t}"
            else:
                errors[f"{i}"] = f"{n}"
        else:
            continue
    print("Arrival time test:")
    if len(errors) == 0:
        print("OK")
    else:
        for k, v in errors.items():
            print(f"bus_id line {k}: wrong time on station {v}")




#bus_lines(buses_dict)
#check_stops(buses_dict)
#transfer_stops(buses_dict)
#special_stops(buses_dict)
#format_errors(buses_dict)
check_arrival(buses_dict)