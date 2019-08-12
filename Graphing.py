import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
from datetime import datetime

data_csv = '/home/ethan/Desktop/Test_csv.csv'
temp = []
hum = []
time = []

with open(data_csv, mode='r') as data:
    csv_reader = csv.DictReader(data, delimiter='\t')
    for row in csv_reader:
        temp.append(float(row['Temp']))
        hum.append(float(row['Humidity']))
        time.append(row['Time'])


def plot_and_humidity(data_csv):
    points = [i for i in range(len(time))]
    lines = plt.plot(points, temp, points, hum)
    plt.show()

def time_converter(times):
    new_times = []
    for time in times:
        time = time.replace('.', '')
        time = list(time)
        time[2] = '.'
        time[5] = ''
        if time[0] is '0': time[0] = ''
        time = float(''.join(time))
        new_times.append(time)

    return new_times



plot_and_humidity('/home/ethan/Desktop/Test_csv.csv')

def scatter(data_csv):

    plt.scatter(temp, hum, 10)
    plt.ylabel('Relative Humidity (%)')
    plt.xlabel('Fridge Temperature (C)')
    plt.show()


def going_higher():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = temp
    z = hum
    y = time_converter(time)
    print(z[0])

    ax.scatter(x, y, z, c='g', marker='o', s=10)

    ax.set_xlabel('Temperature, C')
    ax.set_ylabel('Time, 24hr')
    ax.set_zlabel('Humidity, %')

    plt.show()
going_higher()
