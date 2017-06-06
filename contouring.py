import numpy as np
import cv2
import pymunk


class Contour(object):

    def __init__(self, mass):
        self.something = 0
        self.mass = mass
        #self.body = pymunk.Body(mass)
        self.shadow_detected = False

    def video_contour(self):
        cap = cv2.VideoCapture(0)

        while(True):
        	# Capture frame-by-frame
            ret, frame = cap.read()

            # transform image to grayscale and blur
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            blur = cv2.GaussianBlur(gray,(5,5),0)

            # color thresholds for binary image
            lower_color = np.array([0,0,0], dtype = "uint8")
            upper_color = np.array([90,90,90], dtype = "uint8")

            # create binary image
            binary_img = cv2.inRange(blur, lower_color, upper_color)

            # dilate image
            kernel = np.ones((5,5), np.uint8)
            img_erode = cv2.erode(binary_img, kernel, iterations=0)
            img_dilation = cv2.dilate(img_erode, kernel, iterations=0)
            #opening = cv2.morphologyEx(img_dilation, cv2.MORPH_OPEN, kernel)
            cv2.imshow('binary',img_dilation)

            # find thresholds for contouring
            #ret,thresh = cv2.threshold(img_dilation,0,115,cv2.THRESH_BINARY)

            # contour
            if cv2.__version__.startswith('3.'):
                 _, contours, hierarchy= cv2.findContours(img_dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            else:
                contours, hierarchy= cv2.findContours(img_dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            #self.contour_object(contours)
            tuple_contours = self.convert_contour(contours)

            if not self.shadow_detected:
                self.create_contour_objects(tuple_contours)
            # draw contour on the dilated image
            for c in contours:
                cv2.drawContours(frame, [c], -1, (255,0,0), 3)

             # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def create_contour_objects(self, contour_list):
        for contour in contour_list:
            shape = pymunk.Poly(pymunk.Body(0, 0, pymunk.Body.KINEMATIC), contour)
            #print 'shape'
        #print(self.contour)

    def convert_contour(self, contour_list):
        #print contour_list
        list_of_contours = []
        for i in contour_list: #i is the individual contour
            contour_lst_of_tuples = []
            for j in i: #j is the point in the contour, which has an unnecessary dimension for some reason
                k = np.squeeze(j)
                contour_lst_of_tuples.append(tuple(k))
            list_of_contours.append(contour_lst_of_tuples)
        return(list_of_contours)

if __name__ == '__main__':
    testContour = Contour(1)
    testContour.video_contour()
