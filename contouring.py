import numpy as np
import cv2
import pymunk


class Contour(object):

    def __init__(self, space, camera, height):
        self.something = 0
        self.space = space
        self.camera = camera
        self.shadow_detected = False
        self.cap = cv2.VideoCapture(self.camera)
        self.height = height
        #self.img = cv2.imread('/home/audrey/Software_of_Summer/shadow_drops/square.png')


    def update_contours(self):
    	# Capture frame-by-frame


        ret, frame = self.cap.read()
        img = frame
        #self.img = cv2.imread('/home/audrey/Software_of_Summer/shadow_drops/squares.png')
        #frame = self.img
        #print self.img

        # transform image to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # color thresholds for binary image
        lower_color = np.array([0,0,0], dtype = "uint8")
        upper_color = np.array([90,90,90], dtype = "uint8")

        # create binary image
        binary_img = cv2.inRange(blur, lower_color, upper_color)
        #cv2.imshow('binary',binary_img)

        # dilate image
        # kernel = np.ones((5,5), np.uint8)
        # img_erode = cv2.erode(binary_img, kernel, iterations=0)
        # img_dilation = cv2.dilate(img_erode, kernel, iterations=0)

        # contour
        if cv2.__version__.startswith('3.'):
             _, contours, hierarchy= cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy= cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #self.contours_img = binary_img
        #print contours
        #for c in contours:
        cv2.drawContours(img, contours, -1, (240,100,0), 3)
        self.contours_img = img
        tuple_contours = self.convert_contour(contours)
        #self.create_shadows(tuple_contours)
        return tuple_contours

    def kill_video(self):
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()



    def convert_contour(self, contour_list):
        list_of_contours = []
        for i in contour_list: #i is the individual contour
            if cv2.contourArea(i) < 500 and cv2.contourArea > 1200:
                #print 'small'
                pass
            else:
                #print cv2.contourArea(i)
                #print 'found valid contour'
                contour_lst_of_tuples = []
                for j in i: #j is the point in the contour, which has an unnecessary dimension for some reason
                    k = np.squeeze(j)
                    x = float(k[0])
                    y = float(k[1])-self.height
                    contour_lst_of_tuples.append((x,y))
                list_of_contours.append(contour_lst_of_tuples)
        return(list_of_contours)

if __name__ == '__main__':
    testContour = Contour(1)
    testContour.update_contours()
