import rsk
import numpy as np
from math import sqrt, atan, tan
import time
import threading
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

with rsk.Client(host='192.168.1.36', key='') as client:
    cobaye = client.robots['green'][1]
    x_pose_list = []
    x_time = []
    recording = True
    destination = (0.5, 0, 0)
    value_number = 200


    def record_test(Client, dt):
        if len(x_time) <= value_number:
            x_pose_list.append(cobaye.pose[0])
            x_time.append(x_time[-1] + dt if x_time else 0)
        else:
            return False
        
            
    cobaye.goto((-0.5, 0, 0), wait = True)
    time.sleep(0.5)
    client.on_update = record_test
    while recording:

        cobaye.goto((destination), wait = False)
        #print progress percentage
        progress = (len(x_time)/value_number)*100
        print(round(progress, 3), '%')

        if abs(cobaye.pose[0] - destination[0]) < 0.001:
            destination = (-destination[0], 0, 0)
        if len(x_time) > value_number:
            recording = False
            print('End of recording')
            print(len(x_time))
            print(len(x_pose_list))
            print(x_time)
        
        time.sleep(0.01)
            
        

    x_speed = abs(np.diff(x_pose_list) / np.diff(x_time))

    x_acceleration = abs(np.diff(x_speed) / np.diff(x_time[1:]))
    print(x_acceleration)

    #Data smoothing

    

    x_new_time = np.linspace(x_time[0], x_time[len(x_time)-1], 3000)

    smoothing_speed = make_interp_spline(x_time[1:], x_speed, k=3)

    speed_smooth = smoothing_speed(x_new_time)

    smoothing_acceleration = make_interp_spline(x_time[2:], x_acceleration, k=3)

    #acceleration_smooth = smoothing_acceleration(x_new_time[1:])
    #for i in range(0, len(acceleration_smooth)-1):
     #   if acceleration_smooth[i] > 5:
      #      acceleration_smooth[i] = 0
    #print(acceleration_smooth)

    plt.scatter(x_time, x_pose_list, s=2)
    plt.show()
    plt.scatter(x_new_time, speed_smooth, s=2)
    plt.show()
    #plt.scatter(x_new_time[2:], acceleration_smooth[1:], s=2)
    #plt.show()

    plt.plot(x_time, x_pose_list)
    plt.show()
    plt.plot(x_new_time, speed_smooth)
    plt.show()
    #plt.plot(x_new_time[2:], acceleration_smooth[1:])
    #plt.show()

    
