import cv2
import numpy as np

cap = cv2.VideoCapture('Video.mp4')

min_width_react = 80
min_height_react = 80
cout_line_position = 550
# Object detection from Stable camera
algo = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=800)
def center_handle(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x + x1
    cy = y + y1
    return cx, cy

detect = []
offset = 6
counter = 0

while True:
    ret, frame = cap.read()
    
    #roi = frame[]
    
    if not ret:
        break
    
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 0)
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilates = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilates = cv2.morphologyEx(dilates, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(dilates, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame, (25, cout_line_position), (1200, cout_line_position), (255, 127, 0), 2)
    
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w >= min_width_react and h >= min_height_react:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Vehicle Counter: " + str(counter), (x, y - 20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 244, 0), 2)
            
            center = center_handle(x, y, w, h)
            detect.append(center)
            cv2.circle(frame, center, 4, (0, 0, 255), -1)
            
            for (x_c, y_c) in detect:
                if y_c < (cout_line_position + offset) and y_c > (cout_line_position - offset):
                    counter += 1
                    print("Vehicle Counter: " + str(counter))
                cv2.line(frame, (25, cout_line_position), (1200, cout_line_position), (0, 127, 255), 2)
                detect.remove((x_c, y_c))
                
    cv2.putText(frame, "Vehicle Counter: " + str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    
    cv2.imshow('Original Video', frame)
    cv2.imshow('Detector', dilates)
  
    if cv2.waitKey(1) == 13: 
        break

cv2.destroyAllWindows()
cap.release()
