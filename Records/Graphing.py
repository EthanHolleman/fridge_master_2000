import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

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
    points = time_converter(time)
    plt.subplot(1, 2, 1)
    plt.plot(points, temp, label='Temperature, C', c='skyblue')
    plt.title('Fridge Temperature Over 8 Hours')
    plt.xlabel('Time in Hours')
    plt.ylabel('Temperature, C')

    plt.subplot(1, 2, 2)
    plt.plot(points, hum, label='Humidity, %', c='tan')
    plt.title('Fridge Humidity Over 8 Hours')
    plt.ylabel('% Humidity')
    plt.xlabel('Time in Hours')
    #plt.legend(loc='upper left')
    #plt.xlabel('Time in Hours')
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

scatter(data_csv)


def going_higher():
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    Y = temp
    Z = hum
    X = time_converter(time)
    X, Y = np.meshgrid(X, Y)
    ax.contour3D(X, Y, Z, 50, cmap='binary')

    ax.set_xlabel('Temperature, C')
    ax.set_ylabel('Time, 24hr')
    ax.set_zlabel('Humidity, %')

    plt.show()

going_higher()
