'''
Kinematic Calculations and Servo Values for TTM Technology's SCARA Robot. Name: SCARA6-17
 2019 PSU Senior Mechanical Engineering Capstone, Team 17

 Shawn Richardson:     Programmer and Programming Author/Editor, Designer, CAD, Subgroup Overseer
 Alex Gavin:           Programmer, Designer, Subgroup Overseer
 Chris McCormick:      CAD, Designer, Fabricator, Assembly
 Erik Kolste:          CAD, Designer, FEA, Recorder, Fabricator, Assembly
 John Norris:          Group Leader, Project Planner, Designer, CAD, Assembly
 Quinn Gordon:         CAD, Designer, Assembly

 Start Date:   03/04/19
 End Date:     05/17/19

 Script Object: This script calculates the servo values for Dynamixel MX28 and MX64 servos by using
 geometric inverse kinematics, as all code is carried out in Python.
 The values are than sent to the Dynamixel U2D2 compiler to the first Dynamixel in line out to the
 others which than positions the servos to the desired/programmed coordinates.
 The "grid_formula" came from
 https://math.stackexchange.com/questions/1039482/how-to-evenly-space-a-number-of-points-in-a-rectangle
 inverse kinematics starting from beta to theta2l came from "Modern Robotics"
 the manipulation of the servo values starting at the first v1l through sv2.flatten was developed by Shawn
 Alex put together the grid formula and worked on the move_servo function as well as Shawn
'''

# Python Libraries Imported
# from pydynamixel import dynamixel, registers
import two_link_main
import numpy as np
import grid
import math
import time
import math


def num_pts (width, height, points):

    l_1= 15                     #length from the base to the right                     #length from the base to the left
    w= width - 2
    h= height - 4
    if points <=90:
        pts= points +5
    elif points >90:
        pts= points
    n_x= (math.sqrt(((w / h) * pts) + ((w - h)**2) / (4 * (h ** 2))) - ((w - h)/(2 * h)))
    n_x= round(n_x)

    n_y= pts/n_x

    n_y=round(n_y)
    point=n_y * n_x
    print(point)
    delx = w/(n_x -1)          #the spacing between the x points

    dely = h/(n_y -1)        #the spacing beween the y points

    print(delx)
    print(dely)
    #x = np.zeros(shape=n_x)     #creates an array of zeros with length values = of # of points in x direction

    #y=  np.zeros(shape=n_y)     #creates an array of zeros with length values = of # of points in y direction

    if (w > l_1):
        offset= -(w - l_1)
        x=np.arange(offset,l_1,delx)
        y=np.arange(3,height,dely)
        X,Y = np.meshgrid(x,y)

    elif(w < l_1):
        offset = l_1 - w
        x=np.arange(offset, l_1,delx)
        y=np.arange(1,height,dely)
        X,Y = np.meshgrid(x,y)

    point = x.size * y.size
    print(point)
    return(X,Y)

def ikin(X, Y):
    # Arm Link Lengths: change theses as needed
    a1 = 16
    a2 = 14.5

    beta = np.degrees(np.arccos(((a1 ** 2 + a2 ** 2 - X[:] ** 2 - Y[:] ** 2)/ (2 * a1 * a2))))
    alpha = np.degrees(np.arccos((X[:] ** 2 + Y[:] ** 2 + a1 ** 2 - a2 ** 2) / (2 * a1 * np.sqrt(X[:] ** 2 + Y[:] ** 2))))
    gamma = np.degrees(np.arctan2(Y[:], X[:]))
    theta1r = gamma - alpha
    theta2r = 180 - beta
    theta1l = gamma + alpha
    theta2l = beta - 180
    # Ratio for MX
    r = 4095/360
    # Servo values for left and right elbow orientations based on calculated theta's
    v1l = (theta1l + 90) * r
    v2r = (180 + theta2r) * r
    v1r = (theta1r + 90) * r
    v2l = (180 - abs(theta2l)) * r
    # the values are than rounded to whole number integers
    v1l = np.around(v1l, decimals=0)
    v2r = np.around(v2r, decimals=0)
    v1r = np.around(v1r, decimals=0)
    v2l = np.around(v2l, decimals=0)
    # Every other column is flipped starting with the second to provide better effeciency of robot arm movement
    v1l[:, 1::2] = v1l[::-1, 1::2]
    v2r[:, 1::2] = v2r[::-1, 1::2]
    v1r[:, 1::2] = v1r[::-1, 1::2]
    v2l[:, 1::2] = v2l[::-1, 1::2]
    # The flipped arrays are transformed to a list in order of indexing
    v1l_flat = v1l.flatten('F')
    v2r_flat = v2r.flatten('F')
    v1r_flat = v1r.flatten('F')
    v2l_flat = v2l.flatten('F')
    # this returns indices of the max element, in this case 3000, so the arm can remain in the parameters of the PCB's
    idx = np.argmax(v1l_flat>=3000)
    # those values in V1LA >= 3000 are exchanged for the corresponding values in V1RA
    v1l_flat[idx:] = v1r_flat[idx:]
    v2l_flat[idx:] = v2r_flat[idx:]
    # V1LA and V2LA reshaped to original order with replaced values creating SV1 (Servo Value 1) and SV2
    sv1 = np.reshape(v1l_flat, v1l.shape, order='F')
    sv2 = np.reshape(v2l_flat, v2l.shape, order='F')
    # Servo values are transformed to a list in order to communicate the values appropriately to the Arduino
    sv1 = sv1.flatten('F')
    sv2 = sv2.flatten('F')
    s_values = (sv1, sv2)
    print(sv1)
    print(sv2)
    return(sv1,sv2)


def move(sv1, sv2):
    serial_port = 'dev/ttyUSB0'
    servo1_id = 1
    servo2_id = 2
    servo3_id = 3

    while(i< len(sv1)):
        k=0
        i=0
        servoPos1= int(sv1[k])
        servoPos2= int(sv2[k])
        ser = dynamixel.get_serial_for_url(serial_port)
        dynamixel.setposition(ser,servo1_id,servoPos1)
        dynamixel.setposition(ser,servo2_id,servoPos2)
        dynamixel.send_action_packet(ser)

        print('Success')
        i = i + 1
        k = k + 1
        time.sleep(3)
    return()


def home():
    ser = dynamixel.get_serial_for_url(serial_port)
    dynamixel.setposition(ser, servo1_id, 3071)
    dynamixel.setposition(ser, servo2_id, 1024)
    dynamixel.send_action_packet(ser)
    return()



if __name__ == "__main__":

        bar= grid.num_pts(18,24,20)
        ikin(bar[0],bar[1])
        
