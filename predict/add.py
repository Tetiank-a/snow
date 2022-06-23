from csv import writer
import csv
from math import sqrt
from operator import eq


def add(x, y, z, angle, p1, p2, p3, p4):  # add data from Arduino
    with open('predict2/data.csv', 'a+', newline='') as dataset:
        csv_writer = writer(dataset)
        csv_writer.writerow([x, y, z, angle, p1, p2, p3, p4])


def predict2(x : float, y : float, z : float, angle : int, point_left_front : float, point_left_back : float,
 point_right_front : float, point_right_back : float):
    file = open('predict/data.csv')
    csvreader = csv.reader(file)
    min_dif = 10000
    min_angle = 360
    dif_x = 0
    dif_y = 0
    dif_z = 0

    eq_left = float(point_left_front) / float(point_left_back)
    eq_right = float(point_right_front) / float(point_right_back)

    eq_left_change = 1;
    eq_right_change = 1;
    for data in csvreader:
        dif = sqrt((float(data[0]) - x) * (float(data[0]) - x) +
                   (float(data[1]) - y) * (float(data[1]) - y) +
                   (float(data[2]) - z) * (float(data[2]) - z))
        if dif < min_dif:
            min_dif = dif
            min_angle = data[3]
            dif_x = (float(data[0]) - x) * (float(data[0]) - x)
            dif_y = (float(data[1]) - y) * (float(data[1]) - y)
            dif_z = (float(data[2]) - z) * (float(data[2]) - z)

            eq_left_change = float(eq_left / float(float(data[4]) / float(data[5])))
            eq_right_change = float(eq_right / float(float(data[6]) / float(data[7])))
    
    adv1 = '-'
    adv2 = '-'
    adv3 = '-'
    adv4 = '-'

    print("------------------------------------" + str(dif))
    if (min_dif >= 40):
        if dif_x > dif_y and dif_x > dif_z:
            adv1 = 'decrease horizontal speed - try to push more on the leg that is oposite to your movement side'
        if dif_y > dif_z and dif_y > dif_x:
            adv1 = 'decrease vertical speed - turn your snowboard so that it is closer to the paralel state'
        if dif_z > dif_y and dif_z > dif_x:
            adv1 = 'ALERT! the hill angle may be too sharp - decrease vertical speed - turn your snowboard so that it is closer to the paralel state'

    if eq_left_change > 1:
        adv2 = 'push more on the back of left leg'
    if eq_left_change < 1:
        adv2 = 'push more on the front of left leg'

    if eq_right_change > 1:
        adv3 = 'push more on the back of right leg'
    if eq_right_change < 1:
        adv3 = 'push more on the front of right leg'
    
    s = int(min_angle) - int(angle)
    if s < 0:
        adv4 = '- angle on ' + str(int(s) * -1) + ' degrees'
    else:
        adv4 = '+ angle on ' + str(s) + ' degrees'

    return "1) " + adv1 + ";      2) " + adv2 + ';      3)' + adv3 + ';      4)' + adv4
# predict(1, 2, 3, 4)
