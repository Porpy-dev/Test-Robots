import rsk
import numpy as np
from math import sqrt, atan, tan
import time
import threading
import os
import matplotlib.pyplot as plt

with rsk.Client(host='192.168.1.36', key='123') as client:
    cobaye = client.robots['green'][1]
    x_pose_list = []
    frame_time = 0.05

    def start_test(repetition, dt):
        count = 0
        test = True
        destination = (1, 0, 0)
        cobaye.goto((-destination[0], destination[1], destination[2]), wait = True)
        while test:
            cobaye.goto(destination, wait = False)
            x_pose_list.append(round(cobaye.pose[0], 4))
            print(round(cobaye.pose[0], 4))
            time.sleep(dt)
            if abs(cobaye.pose[0] - destination[0]) < 0.01:
                destination = (-destination[0], 0, 0)
                count += 1
                if count == repetition:
                    test = False
        


    start_test(2, frame_time)


    x_time = [frame_time * i for i in range(len(x_pose_list))]
    x_speed = abs(np.diff(x_pose_list) / np.diff(x_time))
    print(x_speed)
    x_acceleration = abs(np.diff(x_speed) / np.diff(x_time[1:]))


    print('done')
    plt.plot(x_time, x_pose_list)
    plt.plot(x_time[1:], x_speed)
    plt.plot(x_time[2:], x_acceleration)
    plt.show()

    

    
        

    
