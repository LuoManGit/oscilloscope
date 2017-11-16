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
    GetModule("C:\GlobMgr.dll")
import comtypes.gen.VisaComLib as VisaComLib
def do_command(command,myScope):
    myScope.WriteString("%s" % command, True)
    check_instrument_errors(command)

    # =========================================================
    # Send a command and check for errors:
    # =========================================================
def do_command_ieee_block(command, data,myScope):
    myScope.WriteIEEEBlock(command, data, True)

    check_instrument_errors(command)

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
def do_query_string(query,myScope):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadString()
    check_instrument_errors(query)
    return result

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
def do_query_ieee_block_UI1(query,myScope):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadIEEEBlock(VisaComLib.BinaryType_UI1, \
                                   False, True)
    check_instrument_errors(query)
    return result

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
def do_query_ieee_block_I2(query,myScope):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadIEEEBlock(VisaComLib.BinaryType_I2, \
                                   False, True)
    check_instrument_errors(query)
    return result

    # =========================================================
    # Send a query, check for errors, return values:
    # =========================================================
def do_query_number(query,myScope):
    myScope.WriteString("%s" % query, True)

    result = myScope.ReadNumber(VisaComLib.ASCIIType_R8, True)
    check_instrument_errors(query)
    return result
    # =========================================================
    # Send a query, check for errors, return values:
    # =========================================================

def do_query_numbers(query,myScope):
    myScope.WriteString("%s" % query, True)
    result = myScope.ReadList(VisaComLib.ASCIIType_R8, ",;")
    check_instrument_errors(query)
    return result

def check_instrument_errors(command,myScope):
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
def ConnectAndSingle():
    #调用该函数来连接示波器，并且启动首次的single模式。
    #返回值为示波器的标志。

    # 第一次使用需要通过GlobMgr.dll来获得那个模块。
    if not hasattr(sys, "frozen"):
        GetModule("C:\GlobMgr.dll")
    import comtypes.gen.VisaComLib as VisaComLib
    # 链接示波器
    rm = CreateObject("VISA.GlobalRM", \
                      interface=VisaComLib.IResourceManager)
    myScope = CreateObject("VISA.BasicFormattedIO", \
                           interface=VisaComLib.IFormattedIO488)
    myScope.IO = \
        rm.Open("TCPIP0::192.168.1.10::hislip0::INSTR")

    myScope.IO.Clear
    print "Interface cleared."
    # 设置最大连接时长为15s
    myScope.IO.Timeout = 60000  # 15 seconds.
    #确定示波器的连接
    idn_string = do_query_string("*IDN?")
    print "Identification string '%s'" % idn_string


    # 示波器准备
    do_command(":STOP")
    str1 = do_query_string("*OPC?")
    print "设备准备情况："
    print str1
    # 清除寄存器，一切归0
    str2 = do_query_string(":ADER?")
    print "初始寄存器的状态："
    print str2
    # 启动single模式，等待...
    do_command(":SINGle")
    print type(myScope)
    return myScope

def SaveAndSingle(myScope,i):
    # 输出等待状态。
    osci_status = do_query_string(":AER?",myScope)
    print "示波器状态："
    print osci_status
    while "0" in osci_status:
        # time.sleep(0.1)
        osci_status = do_query_string(":AER?",myScope)
        print "示波器状态(循环）："
        print osci_status
    #等待采集结束
    ac_status = do_query_string(":ADER?",myScope)
    print "采集寄存器状态："
    print ac_status
    while "0" in ac_status:
        #time.sleep(0.1)
        ac_status = do_query_string(":ADER?",myScope)
        print "采集寄存器状态（循环）"
        print ac_status
    #保存数据
    j = str(i)  # 用于每次保存生成不同的文件。
    do_command(":DISK:SAVE:WAVeform CHANnel1,'C:\data\ddd\kaishi_"+j+".txt',TXT",myScope)
    do_command(":DISK:SAVE:WAVeform CHANnel2,'C:\data\ddd\jeishu_"+j+".txt',TXT",myScope)
    do_command(":DISK:SAVE:WAVeform CHANnel3,'C:\data\ddd\signal_"+j+".txt',TXT",myScope)
    print "采集数据成功"
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
    time.sleep(0.1)
    do_command(":SINGLE")

if __name__ =='__mainn__':
    myScope = ConnectAndSingle()
    for i in range(1,10000):
        SaveAndSingle(myScope,i)