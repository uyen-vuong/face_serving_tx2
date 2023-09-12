import subprocess
import asyncio
import time
import schedule
import json
import asyncio_mqtt as aiomqtt
from configs import Configure as CFG
from utils.helpers import *
from getmac import get_mac_address as gma
STOP = False

async def healthy_check(list_proc, sessionId):
    def check(list_proc):
        for i,proc in enumerate(list_proc):
            if list_proc[i].poll() is not  None:
                print(f"Failed run process {i}. Trying again!")
                # The process has problem or is not running need to restart 
                new_proc = subprocess.Popen(["python3", "stream_process.py", "--p" , f"{CFG.GRPC.PORT}",
                                "--i" , f"{CFG.GRPC.HOST}", "--c" , f"{i+1}", "--u" , f"{CFG.CAMERA[i]}"
                                "--session", f"{sessionId}"], 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                list_proc[i] = new_proc
                print("Start done a process at: ", i)
    TIME_RECHECK = 10
    print("Running heathy check process")
    # manage process each 5 seconds
    schedule.every(TIME_RECHECK).seconds.do(lambda: check(list_proc=list_proc))
    global STOP
    while True:
        schedule.run_pending()
        if STOP:
            break
        time.sleep(1)

def create_pro(urls, sessionId):
   
    list_proc = {}
    for i in urls:
        try:
            proc = subprocess.Popen(["python3", "stream_process.py", "--p" , f"{CFG.GRPC.PORT}",
                            "--i" , f"{CFG.GRPC.HOST}", "--u" , f"{i}",
                            "--session", f"{sessionId}"], 
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            list_proc[i] = proc
        except FileNotFoundError as exc:
            print(f"Process failed because the executable could not be found.\n{exc}")
            list_proc[i]= None 
        except subprocess.CalledProcessError as exc:
            print(
                f"Process failed because did not return a successful return code. "
                f"Returned {exc.returncode}\n{exc}"
            )
            list_proc[i] = None 
        except subprocess.TimeoutExpired as exc:
            print(f"Process timed out.\n{exc}")
            list_proc[i] = None 
    save_pid_is_running(list_proc=list_proc)
    return list_proc

async def main():
    """
    Pipe process of each message: Receive -> Save into file (option) -> Save mongo DB -> Response msg
    """
    reconnect_interval = 5  # In seconds
    # logger.info(f"Running process: {args.process_id}")
    mac = gma()
    while True:
        try:
            print("Connect MQTT Broken...")
            print(CFG.Mqtt.MQTT_HOST,  # The only non-optional parameter
                            CFG.Mqtt.MQTT_PORT,
                            CFG.Mqtt.MQTT_USERNAME,
                            CFG.Mqtt.MQTT_PASSWORD)
            async with aiomqtt.Client( 
                            hostname=CFG.Mqtt.MQTT_HOST,  # The only non-optional parameter
                            port=CFG.Mqtt.MQTT_PORT,
                            username=CFG.Mqtt.MQTT_USERNAME,
                            password=CFG.Mqtt.MQTT_PASSWORD) as client:
                async with client.messages() as messages:
                    print(f"Finish start a process")
                    await client.subscribe(f"{mac}")
                    async for message in messages:
                        try:
                            payload = json.loads(message.payload.decode())
                            print(payload)
                            global STOP
                            if payload['command'] == "START":
                                if not STOP:
                                    sessionId = payload['lesson']
                                    kill_all_old_process()
                                    list_proc = create_pro(payload["urls"], sessionId)
                                    asyncio.create_task(healthy_check(list_proc, sessionId))
                                else:
                                    print("Process is already running")
                            elif payload['command'] == "STOP":
                                kill_all_old_process()
                                STOP = True
                            else:
                                pass 
                        except Exception as e:
                            print("Error process a msg: ", e)
        except Exception as error:
            """
            Try connect to MQTT each 5 seconds
            """
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
            await asyncio.sleep(reconnect_interval)

if __name__ == "__main__":
    asyncio.run(main())  
   