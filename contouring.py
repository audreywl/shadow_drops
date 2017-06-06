import numpy as np
import cv2
import pymunk


class Contour(object):

    def __init__(self, space):
        self.something = 0
        self.space = space
        self.cap = cv2.VideoCapture(0)
        self.shadow_detected = False

    def create_shadows(self, contours):
        self.remove_shadows()
        for cont in contours:
            if cv2.contourArea(cont) < 50:
                continue
            else:
                body = pymunk.Body(0,0,pymunk.Body.STATIC)
                contour_shape = pymunk.Poly(body, tuple_contours)
                self.space.add(body, contour_shape)
    def update_contours(self):
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
        # kernel = np.ones((5,5), np.uint8)
        # img_erode = cv2.erode(binary_img, kernel, iterations=0)
        # img_dilation = cv2.dilate(img_erode, kernel, iterations=0)

        # contour
        if cv2.__version__.startswith('3.'):
             _, contours, hierarchy= cv2.findContours(img_dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy= cv2.findContours(img_dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        tuple_contours = self.convert_contour(contours)
        self.create_shadows(tuple_contours)

    def kill_video(self):
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def remove_shadows(self):
        for body in self.space.bodies:
            if body.body_type == pymunk.Body.STATIC:
                self.space.remove(body)



    def convert_contour(self, contour_list):
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
    testContour.update_contours()
