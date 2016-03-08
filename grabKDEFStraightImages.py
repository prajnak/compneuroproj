import sys
import getopt
import os
import shutil

"""rootDir = 'D:\\Data Sets\\trippy'
if len(sys.argv) > 1:
  rootDir = sys.argv[1]
  """

def main(arg):
  optlist, args = getopt.getopt(arg, 'hi:o:')
  inputDir = 'D:/Data Sets/trippy/KDEF/KDEF'
  outputDir = 'D:/Data Sets/trippy/StraightKDEF'
  for k,v in optlist:
    if k == "-h":
      print "Usage: python grabKDEFStraightImages.py [-i INPUT_DIR -o OUTPUT_DIR]"
      return
    elif k == "-i":
      inputDir = v
    elif k == "-o":
      outputDir = v
  for dirpath, dirnames, filenames in os.walk(inputDir):
    for f in filenames:
      fs = f.split('.')
      if fs[1] == "JPG" and fs[0].endswith("S"):
        shutil.copy(dirpath + "\\" + f, outputDir + "\\" + fs[0][:-1] + "." + fs[1])

if __name__ == '__main__':
  main(sys.argv[1:])
