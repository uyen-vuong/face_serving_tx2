from grpc_libs.ai_client import PersonGrpcClient
import argparse
import cv2, numpy as np
import time 
import random
from sort import *
import json
import torch
import numpy as np
import time
import requests
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_HOST = os.getenv('BE_HOST')
API_PORT = os.getenv('BE_PORT')

url = f"http://{API_HOST}:{API_PORT}/manager/emotion/1"

dict_emotion = {0:'neutral', 1:'happiness', 2:'surprise', 3:'sadness', 4: 'anger', 5: 'disgust', 6: 'fear', 7: 'contempt'}
dict_color = {0:(255, 255, 255), 
              1:(0, 255, 255), 
              2:(255, 200, 0), 
              3:(255, 128, 0), 
              4: (0, 0, 255), 
              5: (255, 0, 150), 
              6: (0, 255, 0), 
              7: (116, 185, 252)}

async def send_request_emotion(data):
    pass

def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [0, 0, 0], thickness=tf, lineType=cv2.LINE_AA)

async def check_emotion(grpc_client, crop_image, result):

    res = grpc_client.check_emotion(crop_image)
    if res[0] in result:
        result[res[0]] += 1
    else:
        result[res[0]] = 1

def run_main_thread(args):

    client = PersonGrpcClient(args.ip, args.port)
    video = cv2.VideoCapture(args.input)
    history_boxes = []
    cnt = 0
    frame_count = 0
    tracker_mot=Sort()
    start_time = time.time() 
    label_text = "neural"

    while(True):
      
            ret, frame = video.read()
            if not ret:
                print('Reached the end of the video!')
                break

            if cnt % 40 == 0:
                #testing begin
                img_raw = frame
                img_raw = cv2.resize(img_raw, (640,360))
                res=client.detection(img_raw)
                boxes, _, probs = res
                history = np.empty((0, 5))
                for i,b in enumerate(boxes):
                    if probs[i]<0.6:
                        continue
                    history = np.concatenate(( history, np.array([[b[0], b[1], b[2], b[3],probs[i]]])), axis=0)
                    
                history_boxes = tracker_mot.update(history)
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time

                fps_str = "FPS: {:.2f}".format(fps)
                cv2.putText(img_raw, fps_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1 , (0, 255, 0), 2)

                for bbox in history_boxes:
                    # crop_image = img_raw[int(bbox[1]):int(bbox[3]), int(bbox[0]): int(bbox[2])]
                    # res = client.check_emotion(crop_image)
                    # if isinstance(res,list):
                    #     res = res[0]
                    # predicted_emotion = dict_emotion[int(res)]
                    # if frame_server % 20 == 0:
                    #     count_emotion[predicted_emotion] += 1
                    #     sum += 1
                    # label_text = f" {bbox[4]} {predicted_emotion}"
                    res = 0
                    plot_one_box([bbox[0], bbox[1], bbox[2], bbox[3]] , img_raw, color=dict_color[int(res)], label=label_text, line_thickness=1)

            else:
                for bbox in history_boxes:
                    # crop_image = img_raw[int(bbox[1]):int(bbox[3]), int(bbox[0]): int(bbox[2])]
                    # res = client.check_emotion(crop_image)
                    # predicted_emotion = dict_emotion[int(res)]
                    # label_text = f" {int(bbox[4])} {predicted_emotion}"
                    res = 0
                    plot_one_box([bbox[0], bbox[1], bbox[2], bbox[3]] , img_raw,color=dict_color[int(res)], label=label_text, line_thickness=1)
            cnt += 1
            frame_count += 1
            cv2.imshow("video_stream", img_raw)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Face Client')
    parser.add_argument('--ip', default="localhost", type=str,
                        help='Ip address of the server')
    parser.add_argument('--port', default=51111, type=int,
                        help='expose port of gRPC server')
    parser.add_argument('--input', default="dependencies/a.mp4", type=str,
                        help='Input to read frame')
    parser.add_argument('--lesson', default=1, type=int,
                        help='Lesson to stream data')
    
    args = parser.parse_args()

    run_main_thread(args)

   
#     tracker_mot=Sort()
#     hung=[]
#     video = cv2.VideoCapture("dependencies/a.mp4")
   
#     cnt = -1
#     frame_count = 0
#     start_time = time.time() 
#     sum = 0 
#     frame_server = 0
#     count_emotion = {
#         "lessonID": 1,
#         "neutral": 0,
#         "happiness": 0,
#         "surprise": 0,
#         "sadness": 0,
#         "anger": 0,
#         "disgust": 0,
#         "fear": 0,
#         "contempt": 0
#     }

#     while(True):
#         cnt += 1
#         tic = time.time()
#         ret, frame = video.read()
#         if not ret:
#             print('Reached the end of the video!')
#             break
#         if cnt % 40 == 0:
#             #testing begin
#             img_raw = frame
#             img_raw = cv2.resize(img_raw, (640,360))
#             res=client.detection(img_raw)
#             boxes, labels, probs = res
#             history=np.empty((0, 5))
#             for i,b in enumerate(boxes):
#                 if probs[i]<0.6:
#                     continue
#                 history= np.concatenate(( history, np.array([[b[0], b[1], b[2], b[3],probs[i]]])), axis=0)
                 
#             hung=tracker_mot.update(history)
#             # Tính thời gian đã trôi qua
#             elapsed_time = time.time() - start_time

#             # Tính FPS
#             fps = frame_count / elapsed_time

#             # Chuyển đổi FPS thành chuỗi và ghi lên góc trái của video frame
#             fps_str = "FPS: {:.2f}".format(fps)
#             cv2.putText(img_raw, fps_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1 , (0, 255, 0), 2)
            
#             for bbox in hung:
#                 label = f"{bbox[4]}"
#                 crop_image = img_raw[int(bbox[1]):int(bbox[3]), int(bbox[0]): int(bbox[2])]
#                 # history= np.concatenate((history, np.array([[box[0], box[1], box[2], box[3]]])), axis=0)
#                 res = client.check_emotion(crop_image)
#                 # print("res: ", res)
#                 if isinstance(res,list):
#                     res = res[0]
#                 predicted_emotion = dict_emotion[int(res)]
#                 if frame_server % 20 == 0:
#                     count_emotion[predicted_emotion] += 1
#                     sum += 1
#                 label_text = f" {bbox[4]} {predicted_emotion}"
#                 plot_one_box([bbox[0], bbox[1], bbox[2], bbox[3]] , img_raw, color=dict_color[int(res)], label=label_text, line_thickness=1)
#         else:
#             for bbox in hung:
#                 label = f"{bbox[4]}"
#                 crop_image = img_raw[int(bbox[1]):int(bbox[3]), int(bbox[0]): int(bbox[2])]
#                 #history= np.concatenate((history, np.array([[box[0], box[1], box[2], box[3]]])), axis=0)
#                 res = client.check_emotion(crop_image)
#                 predicted_emotion = dict_emotion[int(res)]
#                 if frame_server % 20 == 0:
#                     count_emotion[predicted_emotion] += 1
#                     sum += 1
#                 label_text = f" {int(bbox[4])} {predicted_emotion}"
#                 plot_one_box([bbox[0], bbox[1], bbox[2], bbox[3]] , img_raw,color=dict_color[int(res)], label=label_text, line_thickness=1)
        
#         # Count fps
#         frame_count += 1
#         # Count frames to reset request
#         frame_server += 1
#         # total_count = sum(count_emotion.values())
#         if frame_server % 20 == 0 and sum > 0:
#             json_count_emotion = json.dumps(count_emotion) 
#             print(json_count_emotion)
#             headers = {
#                 "Content-Type": "application/json",
#                 "Accept": "application/json"
#             }
#             response = requests.patch(url,json_count_emotion, headers = headers)
#             print(response.text)
#             for emotion in count_emotion.keys():
#                 if emotion != "lessonID":
#                     count_emotion[emotion]  = 0
#             sum = 0
#         cv2.imshow("t.jpg",img_raw)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
            
# video.release()
# cv2.destroyAllWindows()