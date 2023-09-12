import cv2, numpy as np
from PIL import ImageTk, Image
from datetime import datetime

class FaceObject:

    def __init__(self, id ,rect, frame):

        anpha = (rect[3] - rect[1]) // 3
        self.id = id      
        self.img = frame[rect[1] - anpha:rect[3] + anpha ,rect[0] - anpha:rect[2] + anpha ] 
        self.frame_maintained = 1
        self.rect = rect
        self.name = ''
        self.call_again = True 
        self.remove_time = 0
        
    def update_from_detection(self, frame, rect):
        
        anpha = (rect[3] - rect[1]) // 3
        self.img = frame[rect[1] - anpha:rect[3] + anpha ,rect[0] - anpha:rect[2] + anpha ] 
        self.rect = rect
        self.frame_maintained += 1
     
class FaceHistory:

    def __init__(self, face, name, time):

        face = cv2.resize(face, (90,90))
        image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        self.face_view = ImageTk.PhotoImage(image)
        obj_now = datetime.now()
        self.name = name 
        self.time = str(obj_now.hour) + ":" + str(obj_now.minute) + ":" + str(obj_now.second)
        
