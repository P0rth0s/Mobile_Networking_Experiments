import csv
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np


# Finds number of join events in interval
# Params data, interval length,
# Returns tuple first element is array of inteval start times, second is array of number of events
def findNumberEvents(data, interval):
    intervalEnd = data[0]['startTime'] + interval
    interval_index = 0
    events = [0]
    times = [data[0]['startTime']]
    for row in data:
        if(row['startTime'] < intervalEnd):
            events[interval_index] += 1
        else:
            interval_index += 1
            events.append(1)
            times.append(intervalEnd)
            intervalEnd += interval
    return (times, events)

# Return just the prefix of APName without room numbers
def get_location_prefix(row):
    str = ''
    for char in row['APNAME']:
        if(char.isdigit()):
            break
        else:
            str += char
    return str


def main():
    with open('outputwireless-logs-20120409.DHCP_ANON.csv', mode='r') as csv_file:
        csv_input = csv.DictReader(csv_file)
        data = sorted(csv_input, key=lambda row: row['startTime'])
        for row in data:
            row['startTime'] = int(row['startTime'])
            row['endTime'] = int(row['endTime'])
            row['APNAME'] = get_location_prefix(row)
        events = findNumberEvents(data, 60)
        plt.plot(events[0], events[1], 'o', color='black')
        plt.show()

if __name__ == "__main__":
    main()