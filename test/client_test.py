from grpc_libs.ai_client import PersonGrpcClient
import argparse
import cv2, numpy as np
import time 
import random
from sort.sort import *

dict_emotion = {0:'neutral', 1:'happiness', 2:'surprise', 3:'sadness', 4: 'anger', 5: 'disgust', 6: 'fear', 7: 'contempt'}
dict_color = {0:'neutral', 
              1:'happiness', 
              2:'surprise', 
              3:'sadness', 
              4: 'anger', 
              5: 'disgust', 
              6: 'fear', 
              7: 'contempt'}

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
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Face Client')
    parser.add_argument('--ip', default="localhost", type=str,
                      help='Ip address of the server')
    parser.add_argument('--port', default=51111, type=int,
                      help='expose port of gRPC server')
    args = parser.parse_args()
    client = PersonGrpcClient(args.ip, args.port)
    resize = 1
    tracker_mot=Sort()
    hung=[]
    video = cv2.VideoCapture("dependencies/SECURUS CCTV - 2 Megapixel IP Camera with Audio Classroom Solution.mp4")
    cnt = -1
    start_time = time.time()
    frame_count = 0
    while(True):
        cnt += 1
        tic = time.time()
       
        ret, frame = video.read()
        img_new=frame
        size_img = 1024
        shape_img = img_new.shape
        w = shape_img[1]
        h = shape_img[0]
        ratio_img = 1024/max(w,h)
        w = int(w*ratio_img)
        h = int(h*ratio_img)
        # img_new = cv2.resize(img_new, (w,h))
    #print(img_new.shape)
        if not ret:
            print('Reached the end of the video!')
            break
        if cnt%1==0:
            res =  client.detection(img_new)
            boxes, labels, probs = res
         
            history=np.empty((0, 6)) 
            for i,box in enumerate(boxes):
                if probs[i]<0.6:
                    continue
                
                # cv2.rectangle(img_new, (box[0], box[1]), (box[2], box[3]), (255, 128, 0), 4)
                
                crop_image = img_new[box[1]:box[3], box[0]: box[2]]
                print("crop_image",crop_image)
                
                res = client.check_emotion(crop_image)
                predicted_emotion = dict_emotion[int(res)]
                history= np.concatenate((history, np.array([[box[0], box[1], box[2], box[3],probs[i],int(res)]])), axis=0)
                plot_one_box([box[0], box[1], box[2], box[3]] , img_new, color=None, label=None, line_thickness=3)
                cv2.putText(img_new,str(probs[i]), (int(box[0]), int(box[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            hung=tracker_mot.update(history)
            
            elapsed_time = time.time() - start_time
            # Tính FPS
            fps = frame_count / elapsed_time

            # Chuyển đổi FPS thành chuỗi và ghi lên góc trái của video frame
            fps_str = "FPS: {:.2f}".format(fps)
            cv2.putText(img_new, fps_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1 , (0, 255, 0), 2)
            print('net forward time: {:.4f}'.format(time.time() - tic))   
            cv2.imshow("t.jpg",img_new)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            frame_count+=1
                
        else:
            for box in boxes:
                # cv2.rectangle(img_new, (box[0], box[1]), (box[2], box[3]), (255, 128, 0), 4)
                plot_one_box([box[0], box[1], box[2], box[3]] , img_new, color=None, label=None, line_thickness=3)
                crop_image = img_new[box[1]:box[3], box[0]: box[2]]
                #history= np.concatenate((history, np.array([[box[0], box[1], box[2], box[3]]])), axis=0)
                res = client.check_emotion(crop_image)
                predicted_emotion = dict_emotion[int(res)]
                cv2.putText(img_new, predicted_emotion, (int(box[0]), int(box[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            print('net forward time: {:.4f}'.format(time.time() - tic))   
            cv2.imshow("t.jpg",img_new)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            frame_count+=1
            
                
                    
   