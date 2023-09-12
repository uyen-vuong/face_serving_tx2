import tkinter as tk, cv2
from tkinter import *
import utils.prs_app as prs_app
from PIL import ImageTk, Image
from utils.utils import get_date

def header(master):
    
    # sử dụng để show thời gian địa điểm
    header = tk.Frame(master, height = prs_app.header_frame, width = 1024, bg = 'white')
    header.place(x = 0, y = 0)

    # header sẽ show logo và thơi gian có thể thêm thời tiết nếu muốn
    image = cv2.imread('dataset/log.jpg')
    image = cv2.resize(image, (135,  prs_app.header_frame)) 
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image = ImageTk.PhotoImage(image)

    # set hinh nen 
    bg = tk.Label(header, image = image, height=prs_app.header_frame, width = 135, borderwidth=0,compound="center",highlightthickness = 0)
    bg.image = image 
    bg.place(x = 20, y = 0)

    return header

def video_play(master):
    
    video = tk.Frame(master, height=prs_app.image_frame[0], width = 1024, bg = 'white')
    video.place(x = 0, y = 50)

    return video

def history_preview(master):

    history = tk.Frame(master,bg = prs_app.color_history, height = prs_app.history_frame, width = 1024)
    history.place(x = 0, y = prs_app.header_frame + prs_app.image_frame[0] - 1)
    
    title = tk.Label(history, text = 'Lịch sử điểm danh:  {}'.format(get_date()),height=1 ,width= 30, justify ='left', bg = prs_app.color_history,font=("Helvetica", "11", 'bold'), foreground="black")
    title.place(x = 0, y = 3)

    # moi block h1, h2, h3, h4 se gom co 1 anh va 2 text gom ten va time checkin
    pad_left =  15; image_shape = 90; text_shape = 85; padding = 15; height =  25
        
    canvas1 = tk.Canvas(history, width = image_shape, height = image_shape, bg = prs_app.color_history, highlightthickness=0, relief='ridge')
    T1 = tk.Label(history, height=6, width= 11, justify ='left', bg = prs_app.color_history,font=("Helvetica", "10" , "bold"), foreground="red")
    canvas1.place(x = pad_left, y = height)
    x = pad_left + image_shape + padding -5
    T1.place(x = x, y = height)
    x =  x + text_shape + padding

    canvas2 = tk.Canvas(history, width = image_shape, height = image_shape, bg = prs_app.color_history, highlightthickness=0, relief='ridge')
    T2 = tk.Label(history, height=6, width= 11, justify ='left', font=("Helvetica", "10", 'bold'), bg = prs_app.color_history, foreground="black") 
    canvas2.place(x = x, y = height)
    x = x+ image_shape +  padding - 5
    T2.place(x = x, y = height)
    x = x+ text_shape + padding

    canvas3 = tk.Canvas(history, width = image_shape, height = image_shape,bg = prs_app.color_history, highlightthickness=0, relief='ridge')
    T3 = tk.Label(history, height=6, width= 11, justify ='left', font=("Helvetica", "10", 'bold'), bg = prs_app.color_history, foreground="black")
    canvas3.place(x = x, y = height)
    x = x+ image_shape +  padding - 5
    T3.place(x = x, y = height)
    x = x+ text_shape + padding
       
    canvas4 = tk.Canvas(history, width = image_shape, height = image_shape, bg = prs_app.color_history, highlightthickness=0, relief='ridge')
    canvas4.place(x = x, y = height)
    x = x+ image_shape +  padding -5
    T4 = tk.Label(history, height=6, width= 11, justify ='left', font=("Helvetica", "10", 'bold'), bg = prs_app.color_history, foreground="black") 
    T4.place(x = x, y = height)
    x = x+ text_shape + padding
        
    canvas5 = tk.Canvas(history, width = image_shape, height = image_shape, bg = prs_app.color_history, highlightthickness=0, relief='ridge') 
    canvas5.place(x = x, y = height)
    x = x+ image_shape +  padding - 5
    T5 = tk.Label(history, height=6, width= 11, justify ='left', font=("Helvetica", "10", 'bold'), bg = prs_app.color_history, foreground="black")
    T5.place(x = x,  y = height)
    
    canvas1.image, canvas2.image, canvas3.image, canvas4.image, canvas5.image = None, None, None, None, None 

    return history, canvas1, T1, canvas2, T2, canvas3, T3, canvas4, T4, canvas5, T5


