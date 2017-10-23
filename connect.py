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
myScope.IO.Timeout = 15000 # 15 seconds.

idn_string = do_query_string("*IDN?")
print "Identification string '%s'" % idn_string
print "连接成功"





# wmem_state = do_query_string(":WMEMory4:DISPlay?")
# print "波形存储4的状态：'%s' " % wmem_state
# do_command(":WMEMory4:LOAD D:\oscilloscopedata\key_1_data.txt")
# do_command(":WMEMory4:CLEar") # 清除波形存储4的内容

# do_command(":SINGle") # 启动single模式

#
# for i in range(0,300):
#     idn_string = do_query_string(":OPER?")
#     print " '%s'" % idn_string
#     i = i+1
#     time.sleep(0.5)
# print "Timeout set to 15000 milliseconds."
print "End of program"