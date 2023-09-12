import cv2

def draw_fancy_box(img, pt1, pt2, color = (0, 255, 0), thickness = 2):
    '''
    To draw some fancy box around founded faces in stream
    Parameters:

        -img: image to paint box
        -pt1: top_left point
        -pt2: down_right point
        -color: color to paint defalt: (0, 255, 0)
        -thickness: font weight  
    '''
    x1, y1 = pt1
    x2, y2 = pt2
    d = abs(x2 - x1) // 4

    # Top left
    cv2.line(img, (x1, y1), (x1+ d, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1+ d), color, thickness)
    # cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2, y1), (x2- d, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1+ d), color, thickness)
    # cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1, y2), (x1+ d, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2- d), color, thickness)
    # cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2, y2), (x2- d, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - d), color, thickness)
    # cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)