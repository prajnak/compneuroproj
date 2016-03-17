'''
Originally developed by Chris Ngan with input from Nick Mostowich as part of the SYDE 3B Design Project
'''
import cv2
from PIL import Image
import scipy.misc as misc
import numpy as np
from pubsub import pub
import os
from skimage import exposure
import sys
import getopt
import os
import shutil
import pdb


CASCADE_FILE = "haarcascade_frontalface_alt2.xml"
CASCADE_FILE_LEFT = "haarcascade_lefteye_2splits.xml"
CASCADE_FILE_RIGHT = "haarcascade_righteye_2splits.xml"
IMAGE_OFFSET = 0.1
SHAPE = (160, 160) 
OUTPUT_DIR = 'cropped_images'

def main(arg):
  optlist, args = getopt.getopt(arg, 'hi:o:')
  inputDir = None
  outputDir = None
  for k,v in optlist:
    if k == "-h":
      print "Usage: python image_clean.py [-i INPUT_DIR -o OUTPUT_DIR]"
      return
    elif k == "-i":
      inputDir = v
    elif k == "-o":
      outputDir = v
  if inputDir is None or outputDir is None:
    print "Specify your fucking directories dude"
    print "Usage: python image_clean.py [-i INPUT_DIR -o OUTPUT_DIR]"
    return
  ic = ImageClean(SHAPE)
  for dirpath, dirnames, filenames in os.walk(inputDir):
    count = len(filenames)
    for f in filenames:
      print str(count) + " left"
      count = count - 1
      fs = f.split('.')
      ic.clean_image(dirpath + "\\" + f, OUTPUT_DIR + "\\" + fs[0] + ".pgm")


class ImageClean(): 
    def __init__(self, photo_size):
        self.shape = photo_size
        self.image_offset = IMAGE_OFFSET
        self.cascade = CASCADE_FILE
    
    def clean_image(self, input_path, output_path):
        rects, img = self.__detect(input_path, self.cascade)
        img = self.cropToBiggestFace(rects, img)
        img = self.clean_face_in_memory(img)
        if img is not -1:
          self.save_image(img, output_path)


    def clean_face_in_memory(self, raw_face):
        """
        cleans a face in memory
        takes in an ndarray
        returns an ndarray
        """
        try:
          if len(raw_face) > 0:
            im = Image.fromarray(np.uint8(raw_face)) #get a PIL image
            im = im.resize(self.shape) #resize the image to the given shape
            im = im.convert('L') #grayscale the image
            im_arr = np.array(im)
            im = exposure.equalize_hist(im_arr)
            im = im * 255 #rejigger to rgb space
            return im
          return -1
        except:
          pdb.set_trace()

    def save_image(self, im, path):
        """
        Saves an ndarray as an image using scipy
        """
        misc.imsave(path, im)

    def __detect(self, path, cascade):
        img = cv2.imread(path)
        cascade = cv2.CascadeClassifier(cascade)
        #rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
        rects = cascade.detectMultiScale(
            img,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
            )
        if len(rects) == 0:
            return [], img
        rects[:,2:] += rects[:,:2]
        return [rects, img]

    '''
    Uses left eye to find x1
    '''
    def find_left(self, img):
        cascade = cv2.CascadeClassifier(CASCADE_FILE_LEFT)
        rects = cascade.detectMultiScale(img, 1.3, 4)#, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
        # finds biggest eye 
        max_size = 0
        max_coords = [0,0,0,0]
        x1, y1, x2, y2 = [0,0,0,0]
        for x1, y1, x2, y2 in rects:
            size = (x2-x1)*(y2-y1)
            if size > max_size:
                max_size = size
                max_coords = [x1, y1, x2, y2]
        x1 = max_coords[0]
        y1 = max_coords[1]
        x2 = max_coords[2]
        y2 = max_coords[3]
        misc.imsave('left_eye.jpg',img[y1*0.9:y2*1.1, x1*0.9:x2*1.1])


    def cropToBiggestFace(self, rects, img):
        max_size = 0
        max_coords = [0,0,0,0]
        x1, y1, x2, y2 = [0,0,0,0]
        for x1, y1, x2, y2 in rects:
            size = (x2-x1)*(y2-y1)
            if size > max_size:
                max_size = size
                max_coords = [x1, y1, x2, y2]
        '''
        x1 = max_coords[0]
        y1 = max_coords[1]
        x2 = max_coords[2]
        y2 = max_coords[3]
        '''
        cropped_img = img[y1 - (self.image_offset/2)*(y2-y1): (y1 + (1+self.image_offset/2)*(y2-y1)), x1:(x1 + (1+self.image_offset)*(x2-x1))]
        #cropped_img = img[y1:y2*1.1 , x1*1.1:x2*0.9]

        return cropped_img

if __name__ == '__main__':
  main(sys.argv[1:])
