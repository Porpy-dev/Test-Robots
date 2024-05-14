import rsk
import numpy as np
from math import sqrt, atan, tan
import time
import threading
import os
import matplotlib.pyplot as plt

with rsk.Client(host='192.168.1.36', key='') as client:
    cobaye = client.robots['green'][1]
    x_pose_list = []
    x_time = []
    recording = True
    destination = (1, 0, 0)
    value_number = 100


    def record_test(Client, dt):
        if len(x_time) <= value_number:
            x_pose_list.append(round(cobaye.pose[0], 8))
            x_time.append(round(dt*len(x_time) + dt, 8))
            print(round(x_pose_list[len(x_pose_list)-1]-x_pose_list[len(x_pose_list)-2], 4), round(x_time[len(x_time)-1], 4))
        else:
            return False
        
            
            

        

    cobaye.goto((-1, 0, 0), wait = True)

    while recording:

        client.on_update = record_test
        cobaye.goto((destination), wait = False)
        if abs(cobaye.pose[0] - destination[0]) < 0.01:
            destination = (-destination[0], 0, 0)
        if len(x_time) > value_number:
            recording = False
            print('End of recording')
            print (len(x_time))
            print (len(x_pose_list))
            
        

    x_speed = abs(np.diff(x_pose_list) / np.diff(x_time))
    print(x_speed)


    x_acceleration = abs(np.diff(x_speed) / np.diff(x_time[1:]))

    plt.scatter(x_time, x_pose_list, s=2)
    plt.show()
    plt.scatter(x_time[1:], x_speed, s=2)
    plt.show()
    plt.scatter(x_time[2:], x_acceleration, s=2)
    plt.show()

    

    
        

    
