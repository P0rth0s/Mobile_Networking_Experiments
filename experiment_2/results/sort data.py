from xml.dom import minidom
import csv
import matplotlib.pyplot as plt

print('Gville')

gvilledoc = minidom.parse('emission_output_gville.xml')
steps = gvilledoc.getElementsByTagName('timestep')

timeG = []
fuelPlotG = []
speedG = []

for step in steps:
    time = int(float(step.attributes['time'].value))
    print(time)
    timeG.append(time)

    vehicles = step.getElementsByTagName('vehicle')
    vehicleCount = 0
    totalFuel = 0
    totalSpeed = 0

    for vehicle in vehicles:
        vehicleCount += 1
        totalFuel += float(vehicle.attributes['fuel'].value)
        totalSpeed += float(vehicle.attributes['speed'].value)

    averageFuel = totalFuel/vehicleCount
    averageSpeed = totalSpeed/vehicleCount
    print("average fuel: " + str(averageFuel))
    print("average speed: " + str(averageSpeed))
    fuelPlotG.append(averageFuel)
    speedG.append(averageSpeed)

plt.plot(timeG, fuelPlotG)

print('---------------------------------------------\nCologne6to8')

colognedoc = minidom.parse('emission_ouput_cologne6to8.xml')
steps = colognedoc.getElementsByTagName('timestep')

timeC = []
fuelPlotC = []
speedC = []

for step in steps:

    time = int(float(step.attributes['time'].value)) - 21600
    print(time)
    timeC.append(time)

    vehicles = step.getElementsByTagName('vehicle')
    vehicleCount = 0
    totalFuel = 0
    totalSpeed = 0

    for vehicle in vehicles:
        vehicleCount += 1
        totalFuel += float(vehicle.attributes['fuel'].value)
        totalSpeed += float(vehicle.attributes['speed'].value)

    averageFuel = totalFuel/vehicleCount
    averageSpeed = totalSpeed/vehicleCount
    print("average fuel: " + str(averageFuel))
    print("average speed: " + str(averageSpeed))
    fuelPlotC.append(averageFuel)
    speedC.append(averageSpeed)

plt.plot(timeC, fuelPlotC)

with open('experiment_2.csv', mode='w', newline='') as csv_file:
    fieldnames = ['time', 'fuelG', 'fuelC', 'speedG', 'speedC']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()    

    index = 0
    for time in timeC:
        writer.writerow({'time': time, 'fuelG': fuelPlotG[index], 'fuelC': fuelPlotC[index], 'speedG': speedG[index], 'speedC': speedC[index]})
        index += 1