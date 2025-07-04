import cv2
import numpy as np
#from pygame import image 
#import Image_Processing.utils as utils
import utils as utils

import io
import socket
import struct
from PIL import Image
import sys

curve_list = []
avg_val = 10

def get_curve(img, display = 2):
    '''This function returns the curve values'''
    imgResult = img.copy()
    
    img_thres = utils.thresholding(img)
    h, w, c = img.shape
    points = utils.val_trackbar()
    img_warp = utils.warp_img(img_thres, points, w, h)
    img_warped_points = utils.draw_points(img, points)
    
    mid_point, img_hist = utils.get_histogram(img_warp, display=True, percent=0.9, region=4)
    curve_avg, img_hist = utils.get_histogram(img_warp, display=True, percent=0.48)
    curve_raw = curve_avg - mid_point
    
    curve_list.append(curve_raw)
    
    if len(curve_list) > avg_val:
        curve_list.pop(0)
    
    curve = int(sum(curve_list) / len(curve_list))
    
    ## Display fucntion 
    if display != 0:
       imgInvWarp = utils.warp_img(img_warp, points, w, h,inverse= True)
       imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:h//3,0:w] = 0,0,0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
       midY = 450
       cv2.putText(imgResult,str(curve),(w//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
       cv2.line(imgResult,(w//2,midY),(w//2+(curve*3),midY),(255,0,255),5)
       cv2.line(imgResult, ((w // 2 + (curve * 3)), midY-25), (w // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = w // 20
           cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
       #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
       #cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
       imgStacked = utils.stack(0.7,([img,img_warped_points,img_warp],
                                         [img_hist,imgLaneColor,imgResult]))
       cv2.imshow('ImageStack',imgStacked)
    
    elif display == 1:
       cv2.imshow('Resutlt',imgResult)
    

    # cv2.imshow("thres", img_thres)
    # cv2.imshow("wrap", img_warp)
    # cv2.imshow("warp points", img_warped_points)
    # cv2.imshow("warp points", img_hist)
    
    curve = curve/100
    # normalizing the curve 
    
    if curve > 1:
        curve = 1
    if curve < -1:
        curve = -1
    
    return curve
    


if __name__ == "__main__":
    server_socket = socket.socket()
    server_socket.bind((sys.argv[1], int(sys.argv[2])))  
    server_socket.listen(0)
    print("Listening")
    connection = server_socket.accept()[0].makefile('rb')
    
    try:
        img = None
        while True:
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)
            image = Image.open(image_stream)
            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            img = cv2.resize(img, (480, 240))
            curve = get_curve(img)
            cv2.imshow("Vid", img)
            cv2.waitKey(1)
            # Initialize the trackbar once for the incoming stream
            if frameCounter == 0:
                initial_trackbar_val = [131, 176, 85, 240]
                utils.initialize_trackbar(initial_trackbar_val)
            frameCounter += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    finally:
        connection.close()
        server_socket.close()

