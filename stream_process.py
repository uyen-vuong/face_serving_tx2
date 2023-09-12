import cv2 
import time 
import logging 
import asyncio
from grpc_libs.ai_client import PersonGrpcClient as PGC
from websockets.sync.client import connect
from utils.helpers import * 
import cv2
import threading
import time
import base64
import json
import requests

from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv('BE_HOST')
API_PORT = os.getenv('BE_PORT')

locked = False
command = "STOP"

class_table = {0:'neutral', 1:'happiness', 2:'surprise', 3:'sadness', 4: 'anger', 
                    5: 'disgust', 6: 'fear', 7: 'contempt'}

async def pipe_process(grpc_client:PGC, frame):
    global locked
    if locked:
        return
    try:
        locked = True
        boxes, _, _ = grpc_client.detection(frame)
        result = {}
        tasks = []
        
        for box in boxes:
            # cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 128, 0), 4)
            crop_image = frame[box[1]:box[3], box[0]: box[2]]
            task = asyncio.create_task(check_emotion(grpc_client=grpc_client, crop_image=crop_image, result = result))
            tasks.append(task)
        await asyncio.gather(*tasks)     
    finally:
        # push into web
        locked = False
        return result
    
 
async def check_emotion(grpc_client, crop_image, result):
    res = grpc_client.check_emotion(crop_image)
    # images.append(crop_image)
    if res[0] in result:
        result[res[0]] += 1
    else:
        result[res[0]] = 1

async def send_result(sessionID, result):

    url = f"http://{API_HOST}:{API_PORT}/manager/emotion/{sessionID}"
    count_emotion = {
        "lessonID": sessionID,
        "neutral": 0,
        "happiness": 0,
        "surprise": 0,
        "sadness": 0,
        "anger": 0,
        "disgust": 0,
        "fear": 0,
        "contempt": 0
    }
    for key in result.keys():
        label = class_table[key]
        count_emotion[label] = result[key]
    json_count_emotion = json.dumps(count_emotion) 

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    _ = requests.patch(url, json_count_emotion, headers = headers)
   
class Camera(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        if url.isdigit():
            self.url = int(url)
        self.cap = cv2.VideoCapture(self.url)
        ret, self.frame = self.cap.read()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 30)
        self.last_frame_time = time.time()
       
    def run(self):
        # print("Started streaming from " + self.url)
        self.frame_n = 0
        while True:
            self.frame_n += 1
            ret, frame = self.cap.read()
            self.last_frame_time = time.time()
            if not ret:
                print("error fetching stream")
                time.sleep(1)
                continue
            frame = cv2.resize(frame, (640, 480))
            retval, buffer_img = cv2.imencode('.jpg', frame)
            self.arr_frame = frame
            self.frame = base64.b64encode(buffer_img)

async def process(args):

    grpc_client = PGC(args.i, args.p, args.c)
    stream = Camera(args.u)
    stream.start()
    last_frame_time = 0
    last_check_time = time.time()
   
    with connect(f"ws://{API_HOST}:{API_PORT}/ws/chat/{args.session}/") as websocket:
        while True:
            if stream.last_frame_time > last_frame_time:
                last_frame_time = stream.last_frame_time
                global locked
                if not locked and time.time() - last_check_time > args.t:
                    task1 = asyncio.create_task(
                        pipe_process(grpc_client=grpc_client, frame=stream.arr_frame))
                    await task1 
                    result = task1.result()
                    asyncio.create_task(send_result(args.session, result)) 
                    last_check_time = time.time()
                try:
                    websocket.send(stream.frame) 
                except:
                    pass
              
if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Process stream data into database & save file')
    parser.add_argument('--i', type=str, help='IP GRPC', default="127.0.0.1")
    parser.add_argument('--p', type=str, help='PORT GRPC', default="51111")
    parser.add_argument('--c', type=str, help='clientId', default="client0")
    parser.add_argument('--u', type=str, help='RTSP URL camera', default="0")
    parser.add_argument('--t', type=int, default=2 ,help='Interval time check')
    parser.add_argument('--session',default=1, type=str, help='Session is working')
    args = parser.parse_args()
    asyncio.run(process(args)) 
    