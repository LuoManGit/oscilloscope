#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from testformoudleclass import *
import time

#实体化类
osci = OsciCon()
#连接示波器
osci.ConnectAndSingle()
for i in range(1, 10000):
    #保存数据
    str1 = osci.SaveAndSingle(i)
    print str1

