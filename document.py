# -*- coding: utf-8 -*-
import time
k = 1
for i in range(1, 1000):
    if k >= 10:
        k = 1
    j = str(k)
    with open("F:\gitcode\oscilloscope\oscilloscope\ha.txt",'w') as f:
        f.write(j)
        print j
    time.sleep(2)
    k = k+1

