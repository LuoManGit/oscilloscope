# -*- coding: utf-8 -*-
import time
for i in range(1,1000):
    j = str(i)
    with open("D:\python27\shiboqi\inter.txt",'w') as f:
        f.write(j)
        print j
    time.sleep(2)

