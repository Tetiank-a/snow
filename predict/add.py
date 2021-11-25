from csv import writer
import csv
from math import sqrt


def add(x, y, z, angle):  # add data from Arduino
    with open('predict/data.csv', 'a+', newline='') as dataset:
        csv_writer = writer(dataset)
        csv_writer.writerow([x, y, z, angle])


def predict(x : float, y : float, z : float, angle : int):
    file = open('predict/data.csv')
    csvreader = csv.reader(file)
    min_dif = 10000
    min_angle = 360
    for data in csvreader:
        dif = sqrt((float(data[0]) - x) * (float(data[0]) - x) +
                   (float(data[1]) - y) * (float(data[1]) - y) +
                   (float(data[2]) - z) * (float(data[2]) - z))
        if dif < min_dif:
            min_dif = dif
            min_angle = data[3]
            
    s = int(min_angle) - int(angle)
    if s < 0:
        return '- angle on ' + str(int(s) * -1) + ' degrees'
    else:
        return '+ angle on ' + str(s) + ' degrees'

# predict(1, 2, 3, 4)
