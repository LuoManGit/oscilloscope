# -*- coding: utf-8 -*-
import string
import time
import sys
import os
import array
from comtypes.client import GetModule
from comtypes.client import CreateObject
import comtypes.gen.VisaComLib as VisaComLib
# Run GetModule once to generate comtypes.gen.VisaComLib.
if not hasattr(sys, "frozen"):
    GetModule("C:\GlobMgr.dll")
import comtypes.gen.VisaComLib as VisaComLib
class OsciCon(object):
    def __init__(self):
        self.myScope = self.ConnectAndSingle()

    def do_command(self, command):
        self.myScope.WriteString("%s" % command, True)
        self.check_instrument_errors(command)

        # =========================================================
        # Send a command and check for errors:
        # =========================================================
    def do_command_ieee_block(self, command, data):
        self.myScope.WriteIEEEBlock(command, data, True)

        self.check_instrument_errors(command)

        # =========================================================
        # Send a query, check for errors, return string:
        # =========================================================
    def do_query_string(self, query):
        self.myScope.WriteString("%s" % query, True)

        result = self.myScope.ReadString()
        self.check_instrument_errors(query)
        return result

        # =========================================================
        # Send a query, check for errors, return string:
        # =========================================================
    def do_query_ieee_block_UI1(self, query):
        self.myScope.WriteString("%s" % query, True)

        result = self.myScope.ReadIEEEBlock(VisaComLib.BinaryType_UI1,False, True)
        self.check_instrument_errors(query)
        return result

        # =========================================================
        # Send a query, check for errors, return string:
        # =========================================================
    def do_query_ieee_block_I2(self,query):
        self.myScope.WriteString("%s" % query, True)

        result = self.myScope.ReadIEEEBlock(VisaComLib.BinaryType_I2, \
                                       False, True)
        self.check_instrument_errors(query)
        return result

        # =========================================================
        # Send a query, check for errors, return values:
        # =========================================================
    def do_query_number(self,query):
        self.myScope.WriteString("%s" % query, True)

        result = self.myScope.ReadNumber(VisaComLib.ASCIIType_R8, True)
        self.check_instrument_errors(query)
        return result
        # =========================================================
        # Send a query, check for errors, return values:
        # =========================================================

    def do_query_numbers(self,query):
        self.myScope.WriteString("%s" % query, True)
        result = self.myScope.ReadList(VisaComLib.ASCIIType_R8, ",;")
        self.check_instrument_errors(query)
        return result

    def check_instrument_errors(self, command):
        while True:
            self.myScope.WriteString(":SYSTem:ERRor? STRing", True)
            error_string = self.myScope.ReadString()
            if error_string: # If there is an error string value.
                if error_string.find("0,", 0, 2) == -1: # Not "No error".
                    print "ERROR: %s, command: '%s'" % (error_string, command)
                    print "Exited because of error."
                    sys.exit(1)
                else: # "No error"
                    break
            else: # :SYSTem:ERRor? STRing should always return string.
                print "ERROR: :SYSTem:ERRor? STRing returned nothing, command: '%s'"% command
                print "Exited because of error."
                sys.exit(1)
    def ConnectAndSingle(self):
        # 调用该函数来连接示波器，并且启动首次的single模式。
        # 返回值为示波器的标志。

        # 第一次使用需要通过GlobMgr.dll来获得那个模块。
        if not hasattr(sys, "frozen"):
            GetModule("C:\GlobMgr.dll")
        import comtypes.gen.VisaComLib as VisaComLib
        # 链接示波器
        rm = CreateObject("VISA.GlobalRM", \
                          interface=VisaComLib.IResourceManager)
        self.myScope = CreateObject("VISA.BasicFormattedIO", \
                               interface=VisaComLib.IFormattedIO488)
        self.myScope.IO = \
            rm.Open("TCPIP0::192.168.1.10::hislip0::INSTR")

        self.myScope.IO.Clear
        print "Interface cleared."
        # 设置最大连接时长为15s
        self.myScope.IO.Timeout = 60000  # 15 seconds.
        #确定示波器的连接
        idn_string = self.do_query_string("*IDN?")
        print "Identification string '%s'" % idn_string


        # 示波器准备
        self.do_command(":STOP")
        str1 = self.do_query_string("*OPC?")
        print "设备准备情况："
        print str1
        # 清除寄存器，一切归0
        str2 = self.do_query_string(":ADER?")
        print "初始寄存器的状态："
        print str2
        # 启动single模式，等待...
        self.do_command(":SINGle")


    def SaveAndSingle(self,i):
        #用于在每一次single模式后，采集并且存数据。
        # myScope：所连接的示波器。
        # i：第几次采集数据。


        ac_status = self.do_query_string(":ADER?")
        print "采集寄存器状态："
        print ac_status
        while "0" in ac_status:
            #time.sleep(0.1)
            ac_status = self.do_query_string(":ADER?")
            print "采集寄存器状态（循环）"
            print ac_status
        #保存数据
        j = str(i)  # 用于每次保存生成不同的文件。
        self.do_command(":DISK:SAVE:WAVeform CHANnel2,'C:\data\d1117\kaishi_"+j+".txt',TXT")
        self.do_command(":DISK:SAVE:WAVeform CHANnel3,'C:\data\d1117\jeishu_"+j+".txt',TXT")
        self.do_command(":DISK:SAVE:WAVeform CHANnel4,'C:\data\d1117\signal_"+j+".txt',TXT")
        print "采集数据成功"


        # 另一种保存数据的方式
        # do_command(":WMEMory4:SAVE CHANnel1")
        # do_command(":DISK:SAVE:WAVeform WMEMory4,'C:\data20171012\key_" + j + "_data.txt',TXT")
        # print "采集到数据 %s" %j
        # do_command(":WMEMory4:CLEar")
        # print "清除MEMMORY4的数据"
        # time.sleep(0.1)


        while os.path.exists("C:\wenjian\ha.txt"):
             print "文件已存在"
        time.sleep(1)
        j = str(i)
        with open("C:\wenjian\ha.txt", 'w') as f:
            f.write(j)
            print "文件已写入"
        #再次启动single模式。
        self.do_command(":SINGLE")
        return "dr_sun"



if __name__ == '__main__':
    osci = OsciCon()
    osci.ConnectAndSingle()

    for i in range(1,10000):
        str1 = osci.SaveAndSingle(i)
        print str1

