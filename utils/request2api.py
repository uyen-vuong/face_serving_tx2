import json, threading, requests, time
from tkinter import Image
from utils.utils import covert_imgarr2base64, savedic2json, readjson2dic, get_time_current
from utils import prs
import urllib.request
from getmac import get_mac_address as gma

def send_log(id : str, status : str, msg : str):

    """
    Send log about device to bot telegram.
    Parameters:

        -id : identification of device: mac or cameraId ...
        -status : ERROR, WARNING...
        -msg: detail about infor want to show
    """

    if id is None:
        id = prs.mac
        
    def send():
        try:
            url = "http://203.162.88.102:5055/log?id={}&name={}&user={}&delay=1&status={}&detail={}"
            url = url.format(id,'bot', 'device' ,status ,msg )
            _ = requests.get(url)
        except:
            pass 
    
    x = threading.Thread(target=send, args=())
    x.start()

def send_image_recognition(img: str, idx: str):

    """
    Send images to API to recogntion.
    Parameters:

        -list_img: a list image to send to sever.
        -list_idx : with each image will label a idx (timestamp detected face)
    """
    #if prs.classification_blur.predict(img) == True:
    #    return None

    data = {'cameraId' : prs.cameraId, 'organizationId' : prs.organizationId, 'time' : '0'}
    try:
        base64img = covert_imgarr2base64(img)
        if base64img is not None:
            data['image'] = base64img
            data['id'] = idx
            response = requests.post(prs.url_recognition ,json = data, headers= prs.headers)
            json_data = json.loads(response.text)
            return json_data        
    except Exception as e:
        # if has error internet 
        # if str(e).split('(')[0] == 'HTTPConnectionPool':
        #     # save all request to file and process when has internet connect
        #     if prs.start_no_internet is None:
                
        #         prs.start_no_internet = time.time()
            
        #     elif time.time() - prs.start_no_internet > 1.5:
                
        #         data['time'] = str(time.time())
        #         savedic2json(data)
        #         prs.start_no_internet = time.time()

        #     return None 
        send_log( prs.cameraId, 0, "Lỗi diem danh: " + str(e))
       
    return None

def send_image_save2database(list_img: list):

    """
    Send face to sever after get face of new person.
    Parameters:

        -list_img: a list image to send to sever.
        
    """
    data = {'images' : [], 'cameraId' : prs.cameraId, 'organizationId': prs.organizationId}
    
    for i, img in enumerate(list_img):
        data['images'].append({'id': str(i), 'image': img})
        
    # send request to sever 
    try:   
        response = requests.post(prs.url_new_user ,json = data, headers= prs.headers)
        
        if response.status_code >= 200 and response.status_code < 300:
            return True 
        
    except Exception as e:    
        send_log( prs.cameraId, 0, "Lỗi khi lấy ảnh train: " + str(e))
        
    return False

def mac2mode():

    """
    Init device: send request to sever to requirement cameraId
    """
    try:
        respond = requests.get(url = prs.url_mac2mode.format(prs.mac))
        
        if respond.status_code >= 200 and respond.status_code < 222:
           
            data = respond.json()
            print(data)
            prs.cameraId = data['cameraId']
            prs.organizationId = data['organizationId']
           
            if data['endpoint'] != '':
                prs.url_recognition = data['endpoint']
            prs.token = data['token']
            return True

    except Exception as e: 
        send_log( prs.cameraId, 0, "Lỗi khi khoi dọng ung dung: " + str(e))
        return False
    return False

def getMode():

    """
    Request to sever to update mode of application for device
    """
    
    url =  prs.url_mode.format(prs.cameraId)
    try:
        respond =  requests.get(url)
        json_data =  json.loads(respond.text)
        
        if json_data != '' :
            return json_data['mode']
    except Exception as e:
		
        send_log( prs.cameraId, 0, "Không thể lấy được mode: " + str(e))

def send_request_update():

    """
    Send request to sever to report status of device every 10 mins

    {"MAC": "ab:bc:12:12", "version": "1.2"}
    """
    try:
        _ = requests.put(prs.url_cam.format(prs.mac), data ={'serial':'1.2'})

        print('Success update')
    except:
        print("[ERROR]: Send a request to sever ")


def has_internet():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False
   
def send_image_recognition_after_has_internet(json_file):

    """
    When don't has internet, request data will save to .json file. When has connect internet again,
    Device will automatic send request to sever.

    Parameter:
        - json_file: file_json to send
    """

    # read file json
    data = readjson2dic(json_file)

    # check has a internet
    if has_internet():
        try:  
            response = requests.post(prs.url_recognition ,json = data, headers= prs.headers)
            json_data = json.loads(response.text)
            if json_data['status'] == 'OK':

               return True
        
        except Exception as e:
            send_log( prs.cameraId, 0, "Lỗi diem danh: " + str(e))
    
    return False



