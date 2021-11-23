from csv import writer
import csv

def add(x, y, z, angle): # add data from Arduino
    with open('predict/data.csv', 'a+', newline='') as dataset:
        csv_writer = writer(dataset)
        csv_writer.writerow([x, y, z, angle])

def predict():
    file = open('predict/data.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    data = next(csvreader)
    return 'decrease angle to ' + str(data[3]) + ' degrees'

# predict(1, 2, 3, 4)

