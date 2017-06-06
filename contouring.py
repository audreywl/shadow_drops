
import numpy as np
import cv2


cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    lower_color = np.array([0,0,0], dtype = "uint8")
    upper_color = np.array([110,110,110], dtype = "uint8")


    #ret, thresh_img = cv2.threshold(blur,177,255,cv2.THRESH_BINARY)

    #th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            #cv2.THRESH_BINARY,11,2)

    binary_img = cv2.inRange(blur, lower_color, upper_color)

    kernel = np.ones((5,5), np.uint8)
    img_dilation = cv2.dilate(binary_img, kernel, iterations=1)
    #contours =  cv2.findContours(binary_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
   # for c in contours:
        #cv2.drawContours(binary_img, [c], -1, (0,255,0), 3)

     # Display the resulting frame
    cv2.imshow('frame',img_dilation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#erod and dilateb

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()