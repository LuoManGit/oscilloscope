# -*- coding: utf-8 -*-
import string
import time
import sys
import array
from comtypes.client import GetModule
from comtypes.client import CreateObject
import comtypes.gen.VisaComLib as VisaComLib
# Run GetModule once to generate comtypes.gen.VisaComLib.
if not hasattr(sys, "frozen"):
    GetModule("D:\GlobMgr.dll")

def do_command(command):
    myScope.WriteString("%s" % command, True)
    check_instrument_errors(command)

    # =========================================================
    # Send a command and check for errors:
    # =========================================================
def do_command_ieee_block(command, data):
    myScope.WriteIEEEBlock(command, data, True)

    check_instrument_errors(command)

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
def do_query_string(query):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadString()
    check_instrument_errors(query)
    return result

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
def do_query_ieee_block_UI1(query):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadIEEEBlock(VisaComLib.BinaryType_UI1, \
                                   False, True)
    check_instrument_errors(query)
    return result

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
def do_query_ieee_block_I2(query):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadIEEEBlock(VisaComLib.BinaryType_I2, \
                                   False, True)
    check_instrument_errors(query)
    return result

    # =========================================================
    # Send a query, check for errors, return values:
    # =========================================================
def do_query_number(query):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadNumber(VisaComLib.ASCIIType_R8, True)
    check_instrument_errors(query)
    return result
    # =========================================================
    # Send a query, check for errors, return values:
    # =========================================================

def do_query_numbers(query):
    myScope.WriteString("%s" % query, True)
    result = myScope.ReadList(VisaComLib.ASCIIType_R8, ",;")
    check_instrument_errors(query)
    return result

def check_instrument_errors(command):
    while True:
        myScope.WriteString(":SYSTem:ERRor? STRing", True)
        error_string = myScope.ReadString()
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


rm = CreateObject("VISA.GlobalRM", \
interface=VisaComLib.IResourceManager)
myScope = CreateObject("VISA.BasicFormattedIO", \
interface=VisaComLib.IFormattedIO488)
myScope.IO = \
rm.Open("TCPIP0::192.168.1.10::hislip0::INSTR")

# Clear the interface.
myScope.IO.Clear
print "Interface cleared."
# Set the Timeout to 15 seconds.
myScope.IO.Timeout = 60000 # 15 seconds.

idn_string = do_query_string("*IDN?")
print "Identification string '%s'" % idn_string

#do_command()
#示波器准备
do_command(":STOP")
str1 = do_query_string("*OPC?")
print "设备准备情况："
print str1
#清除寄存器
str2 = do_query_string(":ADER?")
print "初始寄存器的状态："
print str2
#启动single模式
do_command(":SINGle")
for i in range(1,2):
    #示波器准备
    osci_status = do_query_string(":AER?")
    print "示波器状态："
    print osci_status
    while "0" in osci_status:
        time.sleep(0.1)
        osci_status = do_query_string(":AER?")
        print "示波器状态(循环）："
        print osci_status
    #等待采集结束
    ac_status = do_query_string(":ADER?")
    print "采集寄存器状态："
    print ac_status
    while "0" in ac_status:
        time.sleep(0.1)
        ac_status = do_query_string(":ADER?")
        print "采集寄存器状态（循环）"
        print ac_status
    #保存数据
    j = str(i)  # 用于每次保存生成不同的文件。
    do_command(":DISK:SAVE:WAVeform CHANnel2,'C:\data20171012\keyhhh_"+j+"_data.txt',TXT")
    # 另一种保存数据的方式
    # do_command(":WMEMory4:SAVE CHANnel1")
    # do_command(":DISK:SAVE:WAVeform WMEMory4,'C:\data20171012\key_" + j + "_data.txt',TXT")
    # print "采集到数据 %s" %j
    # do_command(":WMEMory4:CLEar")
    # print "清除MEMMORY4的数据"

    #给出采集到数据的信号。写入文档。老师又说不用写了，先用延时。
    # with open("D:\python27\shiboqi\inter.txt", 'w') as f:
    #     f.write(j)
    #     print j
    # time.sleep(2)
    #
    #循环启动single 准备下一次采集
    time.sleep(1)
    i = i+1
    do_command(":SINGLE")

