# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 20:17:03 2019

@author: BUA
"""

import cv2
from PIL import ImageTk, Image

from imutils import face_utils
import numpy as np
import imutils
import dlib
import math
from skimage.transform import rotate
import scipy.misc
from numpy import array

import matplotlib.pyplot as plt


def facephysio(filepath):
    
    image = cv2.imread(filepath)
    
    
    # initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    # load the input image, resize it, and convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
   
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
    X = []
    for i in range(0,68):
        X.append(shape[i][0])
    height, width, channels = image.shape
    
    Y = []
    for i in range(0,68):
        Y.append(height - shape[i][1])
    
    
    a = math.hypot(X[16]-X[0], Y[16]-Y[0])
    b = math.hypot(X[16]-X[0], Y[16]-Y[16])
    
    if Y[16] < Y[0] :
        im1 = image
        im2 = rotate(im1, math.degrees(math.acos(b/a)), center=(height-Y[16],X[16]))
        # scipy.misc.imsave('ro.jpg', im2)
    else:
        im1 = image
        im2 = rotate(im1, -math.degrees(math.acos(b/a)), center=(height-Y[16],X[16]))
        # scipy.misc.imsave('ro.jpg', im2)
    
    
    # step 2 Crop
    image = im2.copy()
    gray = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_BGR2GRAY)
    print(type(gray))
    rects = detector(gray, 1)
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
    X = []
    for i in range(0,68):
        X.append(shape[i][0])
    height, width, channels = image.shape
    Y = []
    for i in range(0,68):
        Y.append(height - shape[i][1])
    
    #ymax = max(Y)
    x_max = max(X)
    y_max = height - max(Y)
    x_min = min(X)
    y_min = height - min(Y)
    y_max =int(y_max - ((40/100)*(math.fabs(y_max-y_min))))
    cropped_img = image[y_max-50:y_min+50 , x_min-50:x_max+50]
    # scipy.misc.imsave('outfile.jpg', cropped_img)
    
    # step 3 Dectec data
    image = cropped_img.copy() # cv2.imread("outfile.jpg")
    #resize image
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_BGR2GRAY)
    
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
    
    X = []
    for i in range(0,68):
        X.append(shape[i][0])
    height, width, channels = image.shape
    Y = []
    for i in range(0,68):
        Y.append(height - shape[i][1])
        
    
    YUM = []
    for i in range(48,55):
        YUM.append(Y[i])
    for i in range(64,59,-1):
        YUM.append(Y[i])
    YUM.append(Y[48])
    
    YLM = []
    for i in range(54,60):
        YLM.append(Y[i])
    YLM.append(Y[48])
    YLM.append(Y[60])
    for i in range(67,63,-1):
        YLM.append(Y[i])
    YLM.append(Y[54])
    
    #Analysis mouth data
    # slim or thick?
    
    
    F=50
    text='กลุ่มที่ 1 ปากหนา หรือ ปากบาง \n'
    
    Lxl = math.fabs(X[48]-X[54])
    Lylu = max(YUM) - min(YUM) 
    Lyll = Y[66] - min(YLM)
    if ((Lylu+Lyll)/Lxl) < 0.4:
        
        text=text+'\t-ปากบาง ตัดสินใจเร็วเฉียบขาด ใจเย็น วาจาคมกริบ รับผิดชอบดี เชื่อมั่นตัวเองสูง หยิ่งและทรนง\n'
    
        text=text+' \tถ้าประกอบกับหน้าสี่เหลี่ยมจะตัดสินใจเฉียบขาดมาก \n'
        
    elif  ((Lylu+Lyll)/Lxl) > 0.4:
        text=text+'\tปากลักษณะสี่เหลี่ยม ถ้ามีสีแดงสดใส มีฟันเรียงเรียบร้อยและมีประกาย คือปากของคนร่ำรวย \n'
    
        text=text+' \tอดทนฝ่าฟันอุปสรรคได้ดี แสดงถึงสุขภาพที่ดี มีความกระตือรือร้นสูง หากเป็นผู้ชาย  \n'
    
        text=text+'\tเป็นคนขยันทำมาหากิน  มีความกระตือรือร้นสูง หากเป็นผู้ชาย เป็นคนขยันทำมาหากิน \n'
    
    else:
        text=text+'-\n'
    
    
    # wide?
    
    text=text+'กลุ่มที่ 2 ปากกว้าง\n'
    
    CXLE = math.fabs(X[36] + X[39])/2
    CXRE = math.fabs(X[42] + X[45])/2
    XCE = math.fabs(CXLE - CXRE)
    
    if (XCE/Lxl) < 1:
        text=text+'\t-ปากกว้าง หากเป็นผู้หญิง ชีวิตคู่มักไม่ค่อยดี เป็นคนที่มีความมุ่งมั่น รู้จักฉวยโอกาสมุ่งมั่นที่จะเอาสิ่งที่ต้องการ\n'
    
        text=text+'\tหาจังหวะที่ดีมาให้ตนเอง ไม่หวาดกลัวอุปสรรค ทำให้มีโอกาสพบความสำเร็จมากขึ้น เป็นคนกินเก่ง ชอบใช้ชีวิตสุขสำราญ และใจกว้าง\n'
    
    else:
        text=text+'-\n'
    
    
    
    #about thickness
    
    text=text+'กลุ่มที่ 3 ความหนาของปากบนและล่าง\n'
    
    if Lylu/Lyll == 1:
        text=text+'\t-ริมฝีปากบนและล่างเท่ากัน เชื่อมั่นในตัวเองมากจนคิดว่าเวลาทำอะไรก็ถูกไปเสียหมด \n'
    
    elif  Lylu < Lyll:
        text=text+'\t-ปากบนบาง ปากล่างหนา มีอัตตาสูง มีเสน่ห์เล่ห์กล รักง่ายหน่ายเร็ว หากเป็นผู้ชาย \n'
    
        text=text+'\tมักเป็นคนขี้บ่น ชอบใช้ความฉลาดหาประโยชน์ใส่ตัว อาจถึงขั้นฉลาดแกมโกง หากเป็นผู้หญิง \n'
    
        text=text+'\tชอบงานนอกบ้านหรืองานสังสรรค์ จะได้รับการดูแลที่ดีมีความสุขในบั้นปลาย  \n'
    
    elif  Lylu > Lyll:
        text=text+'\t-ปากบนหนา ปากล่างบาง มีนิสัยใจกล้าบ้าบิ่น พูดตรง หากเป็นผู้ชาย เป็นเครื่องหมายความลำบากของชีวิต \n'
    
        text=text+'\tชีวิตหนีความยุ่งยากไม่พ้น หากเป็นผู้หญิงมีโอกาสอาภัพคู่  \n'
  
    return text




# ส่วนเรียกรัน...
# filepath = "upload_images/test.jpg"   
# image = cv2.imread(filepath)
# rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# plt.imshow(rgb)
# plt.show()
# result =  facephysio(filepath)
# print(result)

