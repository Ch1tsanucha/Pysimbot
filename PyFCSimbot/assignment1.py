#!/usr/bin/python3

import os, platform
if platform.system() in ["Linux", "Darwin"]:
    os.environ["KIVY_VIDEO"] = "ffpyplayer"

from pysimbotlib.core import PySimbotApp, Robot
from kivy.logger import Logger
from kivy.config import Config


Config.set('kivy', 'log_level', 'info')

REFRESH_INTERVAL = 1 / 60
SAFETY_DISTANCE = 30
CLOSED_DISTANCE = 5



class MyRobot(Robot):
    def __init__(self):
        super().__init__()
        self.previous_sensor = 0
        self.current_sensor = 0
        self.escape_angle = 0
      
    def stuckWithYou(self,pow,left,right):
        self.escape_angle += 1
        self.move(5)
        if left < right:
            self.turn(pow + self.escape_angle)
        else:
            self.turn(-pow - self.escape_angle)
        

    def update(self):
        sensor = self.distance()
       
        front, right, left = sensor[0], sensor[1], sensor[7]
        self.current_sensor = (left + front + right)/3    
            
        Logger.info(f"{sensor}")
        
        if(self.escape_angle > 50):
            self.escape_angle = 0
        
        # CASE 1
        if front >= SAFETY_DISTANCE and left >= SAFETY_DISTANCE and right >= SAFETY_DISTANCE :
            self.move(10)
            smell_angle = ((self.smell() + 180) % 360) - 180
            smell_angle = max(-30, min(30, smell_angle))
            
            self.turn(smell_angle)
            if(self.previous_sensor == self.current_sensor):
                self.stuckWithYou(13,left,right)
    
        # CASE 2
        elif front >= SAFETY_DISTANCE and left >= CLOSED_DISTANCE  and right >= CLOSED_DISTANCE :
            self.move(10)
            if(self.previous_sensor == self.current_sensor):
                self.stuckWithYou(13,left,right)
                    
        # CASE 3
        elif front >= SAFETY_DISTANCE:
            self.stuckWithYou(13,left,right)

        # CASE 4
        elif front <= SAFETY_DISTANCE:
            self.stuckWithYou(60,left,right)
            
        self.previous_sensor = (left + front + right)/3

if __name__ == '__main__':
    app = PySimbotApp(robot_cls=MyRobot, num_robots=1,
                      interval=REFRESH_INTERVAL, enable_wasd_control=True)
    app.run()
