# This code is really bad. If you see it please dont judge me

import csv
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import time
import folium
from IPython.display import HTML, display

INTERVAL_LENGTH = 60
TIMEBLOCK = 2

def printDensity(locationData):
    sortedData = sorted(locationData, key=lambda row: row['density'])
    for row in sortedData:
        print(row['name'] + ': ' + str(row['density']))

# Inefficient af but doing something better is work
#Return array of userNames with over 50 events
def topUsers(data, uniqueUsers):
    bigUsers = []
    eventCount = []
    i = 0
    for user in uniqueUsers:
        eventCount.append(0)
        for row in data:
            if row['userMAC'] == user:
                eventCount[i] += 1
        i += 1
    i = 0
    for cnt in eventCount:
        if cnt > 40:
            bigUsers.append(uniqueUsers[i])
        i += 1
    return bigUsers

# This code is also terrible but oh well
def userDensityMap(data, locationData):
    m = folium.Map(
        location=[29.6436, 82.3549],
        zoom_start=12,
        tiles='Stamen Toner'
    )
    tooltip = 'Click Me For Data'
    for loc in locationData:
        loc['density'] = 0
        for event in data:
            if event['APNAME'] == loc['prefix']:
                loc['density'] += 1
        folium.Marker([loc['lat'], loc['lon']], popup=loc['name'] + ': ' + str(loc['density']), tooltip=tooltip).add_to(m)
    m
    
def userDensity(data, locationData):
    for loc in locationData:
        loc['density'] = 0
        for event in data:
            if event['APNAME'] == loc['prefix']:
                loc['density'] += 1
    return locationData

def eventTimeblocks(data):
    sixThirty = 390
    nineThirty = 570
    elevenThirty = 720
    fourteenThirty = 870
    seventeenThirty = 1050
    twentyThirty = 1230
    earlyBirds = []
    munchers = []
    stompers = []
    for row in data:
        if row['startTime'] > sixThirty and row['startTime'] < nineThirty:
            earlyBirds.append(row)
        elif row['startTime'] > elevenThirty and row['startTime'] < fourteenThirty:
            munchers.append(row)
        elif row['startTime'] > seventeenThirty and row['startTime'] < twentyThirty:
            stompers.append(row)
    return (earlyBirds, munchers, stompers)

def getLocationInformation():
    with open('prefix_lat_lon_name_category.csv', mode='r') as csv_file:
        csv_input = csv.DictReader(csv_file)
        locations = []
        for row in csv_input:
            locations.append(row)
        return locations

def getHourEDT(hourGMT):
    hourEDT = hourGMT - 4
    if(hourEDT < 0):
        hourEDT = 24 + hourEDT
    return hourEDT

def question_1(data, userMacList):
    print("Number of records in trace: " + str(len(data)))
    print("Number of unique devices in trace: " + str(len(userMacList)))
    events = findNumberEvents(data, INTERVAL_LENGTH)
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
    stri = ''
    for char in row['APNAME']:
        if(char.isdigit()):
            break
        else:
            stri += char
    return stri

def onlyTheseUsersEvents(users, data):
    events = []
    for row in data:
        for user in users:
            if user == row['userMAC']:
                events.append(row)
    return events

def popularCategories(locationData):
    unknown = 0
    academic = 0
    social = 0
    sports = 0
    admin = 0
    library = 0
    housing = 0
    museum = 0
    for loc in locationData:
        if loc['category'] == 'unknown':
            unknown += loc['density']
        elif loc['category'] == 'academic':
            academic += loc['density']
        elif loc['category'] == 'social':
            social += loc['density']
        elif loc['category'] == 'sports':
            sports += loc['density']
        elif loc['category'] == 'admin':
            admin += loc['density']
        elif loc['category'] == 'library':
            library += loc['density']
        elif loc['category'] == 'housing':
            housing += loc['density']
        elif loc['category'] == 'museums':
            museum += loc['density']
    print('Categories:\n' + 'Unknown: ' + str(unknown) + '\nAcademic: ' + str(academic) + '\nSocial: ' + str(social) + '\nSports: ' + str(sports) + '\nAdmin: ' + str(admin) + '\nLibrary: ' + str(library) + '\nHousing:' + str(housing) + '\nLibrary:' + str(library))


def main():
    with open('outputwireless-logs-20120407.DHCP_ANON.csv', mode='r') as csv_file:
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
        uniqueMacList = np.unique(np.array(userMacList))

        # Question 1 & 2
        #question_1(sortedData, uniqueMacList)

        locationData = getLocationInformation()
        timeblockData = eventTimeblocks(sortedData)

        # Question 3
        #bigUsers = topUsers(timeblockData[TIMEBLOCK], uniqueMacList)
        #print('Top users:')
        #for user in bigUsers:
        #    print(user, end=', ')
        #print('\n---\n\n')
        #bigUsersEvents = onlyTheseUsersEvents(bigUsers, timeblockData[TIMEBLOCK])
        #a = userDensity(bigUsersEvents, locationData)
        #printDensity(a)
        #print('\n+++++\n')
        #popularCategories(a)

        # Question 4
        #printDensity(userDensity(timeblockData[TIMEBLOCK], locationData))
        userDensityMap(timeblockData[TIMEBLOCK], locationData)


if __name__ == "__main__":
    main()