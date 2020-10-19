import csv
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import time

def getHourEDT(hourGMT):
    hourEDT = hourGMT - 4
    if(hourEDT < 0):
        hourEDT = 24 + hourEDT
    return hourEDT

def question_1(data, userMacList):
    print("Number of records in trace: " + str(len(data)))
    x = np.array(userMacList)
    print("Number of unique devices in trace: " + str(len(np.unique(x))))
    events = findNumberEvents(data, 60)
    print(events[0])
    print('---')
    print(events[1])
    plt.plot(events[0], events[1], 'o', color='black')
    plt.show()

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
        userMacList = []
        data = []
        for row in csv_input:
            data.append(row)
        for row in data:
            t1 = time.gmtime(int(row['startTime']))
            t2 = time.gmtime(int(row['endTime']))
            row['startTime'] = (getHourEDT(t1[3]) * 60) + t1[4]
            row['endTime'] = (getHourEDT(t2[3]) * 60) + t2[4]
            row['APNAME'] = get_location_prefix(row)
            userMacList.append(row['userMAC'])
        sortedData = sorted(data, key=lambda row: row['startTime'])

        # Question 1 & 2
        question_1(sortedData, userMacList)

if __name__ == "__main__":
    main()