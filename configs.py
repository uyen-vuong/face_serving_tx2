import os
import configparser
# Read local file `config.ini`.
config = configparser.ConfigParser()                                     
config.read('./config.ini')

class Configure:
    
    class GRPC:
        HOST=config.get("GRPC", "HOST")
        PORT=config.get("GRPC", "PORT")
    # CAMERA  = [
    #     config.get("CAMERA", "cam1"),
    #     config.get("CAMERA", "cam2"),
    #     config.get("CAMERA", "cam3"),
    #     config.get("CAMERA", "cam4")
    # ]
    class Mqtt:
        # Source data 
        MQTT_HOST = config.get("MQTT", "MQTT_HOST")
        MQTT_PORT = config.getint("MQTT", "MQTT_PORT")
        MQTT_USERNAME = config.get("MQTT", "MQTT_USERNAME")
        MQTT_PASSWORD = config.get("MQTT", "MQTT_PASSWORD")
    
    NUMBER_OF_SUB_PROCESS=4