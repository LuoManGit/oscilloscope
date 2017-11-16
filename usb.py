#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import time

ser = serial.Serial('0', 250000, timeout=1)
print ser.isOpen()
words="gggggggggggggggg"

while (1):
        print "send 256x\""+words+"\" to remotes"
        startTime = time.time()
        times = 256
        while(times):
                times -= 1
                s = ser.write(words)

        endTime = time.time()
        print "use time: "+str(endTime-startTime)
        print ""
        time.sleep(5)
ser.close()