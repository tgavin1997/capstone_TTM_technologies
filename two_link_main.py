'''
Background:
    This is the main script that encompusses the functions for TTM's two link serial manipulator that
    takes the place of manual copper thickness probing with that of a Fischer Scope.

    The project was carried on by a one of PSU's 2019 Senior Mechanical Engineering Capstones, Team 17

    The robot was given the name SCARA6-17, SCARA (Selective Compliance Articulated Robot Arm),
    6 because we are a team of six, and 17 because corresponding to our end date. 

Alex Gavin:           Programmer, Designer, Subgroup Overseer
Chris McCormick:      CAD, Designer, Fabricator, Assembly
Erik Kolste:          CAD, Designer, FEA, Recorder, Fabricator, Assembly
John Norris:          Group Leader, Project Planner, Designer, CAD, Assembly
Shawn Richardson:     Programmer and Programming Author/Editor, Designer, CAD, Subgroup Overseer
Quinn Gordon:         CAD, Designer, Assembly

Start Date:   03/04/19
End Date:     05/17/19

Script Object:
    This script works in accordance with GUI named app.py that was created by Geoffrey Olson,
    a Computer Science undergraduate at PSU. The GUI is setup where the user can select TTM's standard size
    panel labeled such as small, medium, or large which corresponds to their three standard panel sizes of
    18"x24", 22"x24", or 24"x28". The GUI also has the option to put in a custom length and width, however
    no matter the case, the user has to put in the defined number of points that are needed in order to
    collect the data.

    From there the sizes and number of points carry through over to the num_pts function which calculates
    the corrdinates over which the robot is to move to probe, the nx and ny formula came from Stack Exchange,
    https://math.stackexchange.com/questions/1039482/how-to-evenly-space-a-number-of-points-in-a-rectangle.
    However due to the algorithm of this formula what the user inputs in the GUI for the number of points
    could perhaps not be the actual number of points calculated in the formula. The reason for this is not
    known as it was not evaluated due to project completion time.
    
    The inverse kinematics are than calculated using trigonometeric functions, obtained from
    Modern Robotics: Mechanics, Planning, and Control, 2017, pgs. 187-188.

    After using kinematics and finding servo values for servo 1 and 2 they are than forced to move using
    pydynamixel found on GIT HUB, https://pypi.org/project/pydynamixel/. The contents of the move function
    came from the Motion Example found on the pydynamixel link pasted above. 

    The robot than returns to its home position the robot than returns to its home postion which than it
    waits for its next undertaking. 
'''

# Python Libraries Imported
from pydynamixel import dynamixel, registers
import PythonLibMightyZap as mighty
import two_link_main as tlm
import numpy as np
import math as mt
import time as t    
import sys
        
dynamixel.BAUDRATE = 200000

def num_pts (length, width, points):
        l = length
        w = width
        n = points
        xoffset = 16.125
        yoffset = 3
        nx = mt.sqrt(((l*n)/w) + (((l - w)**2)/(4*w**2))) - ((l - w)/(2*w))
        ny = n/nx
        del_x = l/(nx - 1)
        del_y = w/(ny - 1)
        rd_nx = round(nx)
        rd_ny = round(ny)
        x, y = np.meshgrid(((np.linspace(1, l - 1, rd_nx))), np.linspace(1, w - 1, rd_ny))
        print('x: ' + str(x))
        print('y: ' + str(y)) 
        X = xoffset - x
        Y = yoffset + y
        print('X: ' + str(X))
        return(X, Y)   
      

def ikin(X, Y):
    # Arm Link Lengths: change theses as needed
    a1 = 16.25
    a2 = 16.5
    # Inverse kinematics
    beta = np.degrees(np.arccos(((a1 ** 2 + a2 ** 2 - X[:] ** 2 - Y[:] ** 2)/ (2 * a1 * a2))))
    alpha = np.degrees(np.arccos((X[:] ** 2 + Y[:] ** 2 + a1 ** 2 - a2 ** 2) / (2 * a1 * np.sqrt(X[:] ** 2 + Y[:] ** 2))))
    gamma = np.degrees(np.arctan2(Y[:], X[:]))
    theta1r = gamma - alpha
    theta2r = 180 - beta
    theta1l = gamma + alpha
    theta2l = beta - 180
    # Ratio for MX64/28
    r = 4095/360
    # Servo values for left and right elbow orientations
    S1L = 80   #offset for the left hand solution of servo 1
    S2L = 26   #offset for the left hand solution of servo 2    
    S1R =7     #offset for right hand solution of servo 1   
    S2R =110   #offset for right hand solution of servo 2    
    v1l = (theta1l + 90) * r + S1L
    print('v1l: ' + str(v1l))
    v2r = (180 + theta2r) * r + S2R 
    v1r = (theta1r + 90) * r + S1R
    v2l = (180 - abs(theta2l)) * r - S2L
    print('v2l: ' + str(v2l))
    # Values rounded to whole number integers
    v1l = np.around(v1l, decimals = 0)
    v2r = np.around(v2r, decimals = 0)
    v1r = np.around(v1r, decimals = 0)
    v2l = np.around(v2l, decimals = 0)
    # Every other column flipped for effeciency 
    v1l[:, 1::2] = v1l[::-1, 1::2]
    v2r[:, 1::2] = v2r[::-1, 1::2]
    v1r[:, 1::2] = v1r[::-1, 1::2]
    v2l[:, 1::2] = v2l[::-1, 1::2]
    # Transformed to a list
    v1l_flat = v1l.flatten('F')
    v2r_flat = v2r.flatten('F')
    v1r_flat = v1r.flatten('F')
    v2l_flat = v2l.flatten('F')
    # Returns indices of the max element >= 3000
    # so whole arm can remain in workspace
    idx = np.argmax(v1l_flat>=3000)
    # Values >= 3000 in v1l are exchanged for the corresponding values in v1r
    v1l_flat[idx:] = v1r_flat[idx:]
    v2l_flat[idx:] = v2r_flat[idx:]
    # v1l and v2l reshaped to create sv1 and sv2
    sv1 = np.reshape(v1l_flat, v1l.shape, order='F')
    sv2 = np.reshape(v2l_flat, v2l.shape, order='F')
    # sv1 and sv2 transformed to a list
    sv1 = sv1.flatten('F')
    sv2 = sv2.flatten('F')
    s_values = (sv1, sv2)
    print(sv1)
    print(sv2)
    return(sv1, sv2)


def move(sv1, sv2):
        
    serial_port = '/dev/ttyUSB0'
    servo1_id = 1
    servo2_id = 2
    k=0
    i=0
    ser = dynamixel.get_serial_for_url(serial_port)
    dynamixel.set_velocity(ser,servo1_id,70)
    dynamixel.set_velocity(ser,servo2_id,125)
    while(i< len(sv1)):        
        if mt.isnan(sv1[k]) == False and mt.isnan(sv2[k]) == False:
            servoPos1= int(sv1[k])
            servoPos2= int(sv2[k]) 
        dynamixel.set_position(ser,servo1_id,servoPos1)
        dynamixel.set_position(ser,servo2_id,servoPos2)
        dynamixel.send_action_packet(ser)
        if k==0:
           t.sleep(0.5)
           tlm.zap1(0)
           t.sleep(2)
           tlm.zap(0)
           t.sleep(0.5)
        ismoving=1        
        while(ismoving == 1):
            move_1=dynamixel.get_is_moving(ser,servo1_id)
            move_2=dynamixel.get_is_moving(ser,servo2_id)               
            if move_1 == False or move_2 == False:
                ismoving=0
                t.sleep(1)
                tlm.zap(0.6)     # the variable argument is actuation length in inches
                t.sleep(2)
                tlm.zap(0)
                t.sleep(0.75)
                print('Success')
        
        i = i + 1
        k = k + 1
        
    return()


def home():
    serial_port = '/dev/ttyUSB0'
    servo1_id = 1
    servo2_id = 2
    ser = dynamixel.get_serial_for_url(serial_port)
    dynamixel.set_position(ser, servo1_id, 3071)
    dynamixel.set_position(ser, servo2_id, 1010)
    dynamixel.send_action_packet(ser)
    tlm.zap(0)
    mighty.CloseMightyZap
    return()

def zap_ping ():
    mighty.CloseMightyZap    
    mighty.OpenMightyZap('/dev/ttyUSB0',200000)
    mighty.goalPosition(0,0)    
    return(port)
def zap1 (length):
    mighty.OpenMightyZap('/dev/ttyUSB0',200000)    
    value = 3863.2 * length
    print(value)
    servo_id=0
    mighty.goalPosition(servo_id,int(value))
    return()
def zap (length):
      
    value = 3863.2 * length
    print(value)
    servo_id=0
    mighty.goalPosition(servo_id,int(value))
    return()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        length = int(sys.argv[1])
        width = int(sys.argv[2])
        points = int(sys.argv[3])
    else:
        print("Instruction: $ python " + sys.argv[0] + " <length> <width> <points>")
        exit()
    bar = tlm.num_pts(length, width, points)
    bar1 = tlm.ikin(bar[0],bar[1])
    tlm.move(bar1[0], bar1[1])
    tlm.home()

