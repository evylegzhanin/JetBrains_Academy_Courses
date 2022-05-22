import json

data = json.loads(input())
bus_lines_id = sorted(set([item['bus_id'] for item in data]))


all_stops = []
start_stops = []
finish_stops = []

for bus in bus_lines_id:
    first_last_stops = []  # temporary list for every bus

    for item in data:
        if item['bus_id'] == bus:
            all_stops.append(item['stop_name'])
            if item['stop_type'] == "S":
                first_last_stops.append('S')
                start_stops.append(item['stop_name'])
            elif item['stop_type'] == "F":
                first_last_stops.append('F')
                finish_stops.append(item['stop_name'])
    if first_last_stops == ['F', 'S'] or first_last_stops == ['S', 'F']:
        continue
    else:
        print(f'There is no start or end stop for the line: {bus}.')
        exit()

transfer_stops = set([item for item in all_stops if all_stops.count(item) > 1])


print(f'''
Start stops: {len(set(start_stops))} {sorted(set(start_stops))}
Transfer stops: {len(transfer_stops)} {sorted(transfer_stops)}
Finish stops: {len(set(finish_stops))} {sorted(set(finish_stops))}
''')