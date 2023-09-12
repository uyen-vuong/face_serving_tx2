import cv2, base64, numpy as np, urllib.request, json
from scipy.spatial import distance
from datetime import date
from datetime import datetime
from utils import prs
def covert_imgarr2base64(img_arr):

    """
    Covert numpy array image to string base64
    Parameters:

        -img_arr: array of image.
    """
    try:
        _, img_encoded = cv2.imencode('.jpg', img_arr)
        jpg_as_text = base64.b64encode(img_encoded).decode('utf-8') 
        return jpg_as_text
    
    except:
        return None

def nomarlize_box(face):
    
    """
    Get square box face.
    Parameters:

        -face: bounding box of face (top_left, down_right) 
    """
    try:
        h, w = face[2] - face[0],face[3] - face[1]
        if h > w:
            return (face[0] - 5,face[1] - (h-w) // 2 - 5, face[2] + 5, face[3] + (h-w) // 2 + 5)
        elif h < w:
            return (face[0] - (w-h) // 2 - 5, face[1] - 5, face[2] + (w-h) // 2 + 5, face[3] + 5)
        else:
            return face
    
    except Exception as e:
        return face

def get_date():

    """
    Get data today of system.
    """
    return date.today()

def bb_intersection_over_union(boxA, boxB):

    """
    Calculator IOU of 2 box.
    Parameters:

        -boxA: bounding box of face (top_left, down_right)
        -boxB: same same box A 
    """
	# determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
    return iou

def overlap(new_faces, old_face):
    
    """
    Find a old face with overlap max with new box
    Parameters:

        -new_faces: list bouding box of face (top_left, down_right) 
        -old_face:  bouding box
    """
    ious = [bb_intersection_over_union(face, old_face.rect) for face in new_faces]    
    return np.argmax(ious), np.max(ious)

def url_to_image(url: str):

    """
    Load image from url to view to tkinter app
    Parameters:

        -url: url of image. 
    """
    try:
        resp = urllib.request.urlopen(url)	
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image 
    except:
        return None
        
def savedic2json(dictionary_data):

    path = prs.path_project + '/' + dictionary_data['time'] + ".json"

    json_file = open(path, "w")
    json.dump(dictionary_data, json_file)
    json_file.close()

def readjson2dic(json_path):

    # Opening JSON file
    with open(json_path) as json_file:
        data = json.load(json_file)
        return data
    
def get_time_current():

    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%Y:%m/%d")
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    return str(current_time)
    
def search_idex_camera():
    """
    Search index camera using with camera. Index from 0 to 3 
    """
    def test_device_already(source):
        cap = cv2.VideoCapture(source) 
        if cap is None or not cap.isOpened():
            return False 
        return True 
    for source in range(0, 4): 
        if test_device_already(source):
            return source 
    
