import cv2
from cv2 import FlannBasedMatcher
import numpy as np

def thresholding(img):
    """This function helps in extracting only the colour specified by lower and upper range rest all portions are black"""
    
    # Here we have converted BGR to HSv fromat because it is required to do thresholding 
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([67,0,153]) #HUE min, VAL min
    upper = np.array([159,255,255]) #HUE max
    masked = cv2.inRange(img_hsv, lower, upper)
    
    return masked


def warp_img(img,points,w,h, inverse = False):
    '''This function takes in the image and points and provides the warped image'''
    #p1 are the points of the 4 red dots in the window they are basically the points on which the perspective change is required 
    pt1 = np.float32(points)
    pt2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    if inverse:
        matrix = cv2.getPerspectiveTransform(pt2, pt1)
    else:    
        matrix = cv2.getPerspectiveTransform(pt1, pt2)
    
    img_warp = cv2.warpPerspective(img, matrix,(w,h))
    
    return img_warp

def nothing(a):
    '''This is just used for passing so that the code can run seamlessly when the tracker values change'''
    pass

def initialize_trackbar(vals, wT = 480, hT = 240):
    '''This function creates the trackbar '''
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", vals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", vals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", vals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", vals[3], hT, nothing)
    
    
def val_trackbar(wT= 480, hT = 240):
    '''This function helps to get the values of points that are used for wraping '''
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    #print(widthTop, heightTop, widthBottom, heightBottom)
    points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop), 
                        (widthBottom, heightBottom), (wT - widthBottom, heightBottom)])

    return points


def draw_points(img, points):
    '''This function helps to draw the points on the image so that it is easy to warp the image'''
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0,0,255), cv2.FILLED)
        
    return img

def get_histogram(img, percent=0.1, display = False, region = 1):
    '''This function performs the pixel summation so that curve can be extracted '''
    
    if region == 1:
        print(img.shape)
        hist_values = np.sum(img, axis=0)
    else:
        # here we do it for the the region so if 2 is value of region height/2 is selected as the start value
        hist_values = np.sum(img[img.shape[0] // region:,:], axis=0)
    print(hist_values)
    max_val = np.max(hist_values)
    min_val = max_val*percent
    index_array = np.where(hist_values >= min_val)
    base_point = int(np.average(index_array))
    # the base point value suggests weather to turn right or left
    # print(base_point)
    if display:
        img_hist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(hist_values):
            cv2.line(img_hist, (x, img.shape[0]), (x, int(img.shape[0] - intensity // 255 //region)), (255, 0, 255), 1)
            cv2.circle(img_hist, (base_point, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return base_point, img_hist

    return base_point

def stack(scale,imgArray):
    '''This is the script that is created for stacking all the output frames into one window'''
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
        
