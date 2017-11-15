# -*- coding: utf-8 -*-
import time
import os
for i in range(1, 1000):

    while os.path.exists("F:\gitcode\oscilloscope\oscilloscope\ha.txt"):
        print "文件已存在"
        time.sleep(2)
    j = str(i)
    with open("F:\gitcode\oscilloscope\oscilloscope\ha.txt", 'w') as f:
        f.write(j)
        print "文件已写入"


