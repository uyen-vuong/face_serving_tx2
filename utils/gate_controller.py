"""
Connect to controller to control gate in/out if exist 
"""
import time, os , time 

try:
    import serial
except:
    os.system("pip3 uninstall serial")
    os.system("pip3 install pyserial")

    
from utils.request2api import send_log
from utils import prs 

class GateController:

    def __init__(self, port = "/dev/ttyUSB0", baudrate = 9600):
        self.port = port 
        self.baudrate = baudrate 
        self.connected = True 
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            self.ser.write(str.encode('OFF'))
            print("Connected with default port")
        except Exception as e:
            print(e)
            send_log( prs.cameraId, 0, str(e))
            port_checked = self.search_auto()
            if port_checked:
                self.ser = serial.Serial(port_checked, self.baudrate)
            else:
                self.connected = False
        self.time_init =  0  
       
    def send_open_gate(self):
       
        if time.time() - self.time_init > 5 and self.connected:
            try:
                self.ser.write(str.encode('ON'))
                time.sleep(1)
                self.ser.write(str.encode('OFF'))
            except:
                pass 
            self.time_init = time.time()
       
        
    def listen_gate_respond(self):
        while True:
            data = self.ser.readline() 
            if str(data) == "OK":
                print(data) 
    
    def search_auto(self):
        port_format = "/dev/ttyUSB{}"
        for i in range(1,4):
            port = port_format.format(i)
            try:
                serial.Serial(port, self.baudrate)
                self.connected = True 
                print("Connect with serial ID = ", i)
                return port 
            except:
                send_log( prs.cameraId, 0, "Không tìm thấy thiết bị quản lý đóng mở cửa ra vào")
        return None 
