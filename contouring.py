import numpy as np
import cv2
import pymunk


class Contour(object):
    """wrapper to hold all the image processing, contour finding operations"""
    def __init__(self, space, camera, height):
        self.space = space
        self.camera = camera
        self.cap = cv2.VideoCapture(self.camera)
        self.height = height

    def update_contours(self):
    	# Capture frame-by-frame
        ret, frame = self.cap.read()
        self.debug_img = frame

        # transform image to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # color thresholds for binary image
        lower_color = np.array([0,0,0], dtype = "uint8")
        upper_color = np.array([90,90,90], dtype = "uint8")

        # create binary image
        binary_img = cv2.inRange(blur, lower_color, upper_color)

        # smooth image using erode and dilate
        # kernel = np.ones((5,5), np.uint8)
        # img_erode = cv2.erode(binary_img, kernel, iterations=0)
        # img_dilation = cv2.dilate(img_erode, kernel, iterations=0)

        # contour
        if cv2.__version__.startswith('3.'): #f*ckin openCV changed this format between versions
             _, contours, hierarchy= cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy= cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(self.debug_img, contours, -1, (240,100,0), 3)
        #imshow(self.debug_img)
        tuple_contours = self.convert_contour(contours)
        return tuple_contours


    def convert_contour(self, contour_list):
        """make the contours a list of tuples that represent points on the screen, and filter out contours that are unlikely to be people based on their size"""
        list_of_contours = []
        for i in contour_list: #i is the individual contour
            if cv2.contourArea(i) < 500 and cv2.contourArea > 1200:
                pass
            else:
                contour_lst_of_tuples = []
                for j in i: #j is the point in the contour, which has an unnecessary dimension for some reason
                    k = np.squeeze(j)
                    x = float(k[0])
                    y = float(k[1])-self.height #because pymunk is negative for some f*cking reason
                    # TODO: fix the scalaing problem here
                    contour_lst_of_tuples.append((x,y))
                list_of_contours.append(contour_lst_of_tuples)
        #print('list of contours')
        #print(list_of_contours)
        return(list_of_contours)


    def kill_video(self):
        """When everything done, release the capture"""
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    testContour = Contour(1)
    testContour.update_contours()
