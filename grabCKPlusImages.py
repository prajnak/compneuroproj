import sys
import getopt
import os
import shutil
import re
"""rootDir = 'D:\\Data Sets\\trippy'
if len(sys.argv) > 1:
  rootDir = sys.argv[1]
  """

def main(arg):
  optlist, args = getopt.getopt(arg, 'hi:o:')
  #inputDir = 'D:/Data Sets/trippy/KDEF/KDEF'
  #outputDir = 'D:/Data Sets/trippy/StraightKDEF'
  inputDir = '/Users/pulsar/Documents/compneuroproj/ck_p'
  outputDir = '/Users/pulsar/Documents/compneuroproj/ck_p_clean'
 
  # each emotion + subject combo in the ck+ dataset has more than one 
  # image. It is a sequence of frames that can vary in length
  # we will just pick the last image out of all of them for now
  # there are about 123 subjects in this dataset
  imagesDir = inputDir + '/extended-cohn-kanade-images'
  emotionsDir = inputDir + '/Emotion'

  emotion_map = {'0': 'NE',
                      '1': 'AN',
                      '2': 'CO',
                      '3': 'DI',
                      '4': 'AF',
                      '5': 'HA',
                      '6': 'SA',
                      '7': 'SU'
  }
  import pdb; pdb.set_trace();
  all_images = []; #paths to the last image for each subject
  all_subjects = None;
  all_emotions = [];
  for k,v in optlist:
    if k == "-h":
      print "Usage: python grabCKPlusImages.py [-i INPUT_DIR -o OUTPUT_DIR]"
      return
    elif k == "-i":
      inputDir = v
    elif k == "-o":
      outputDir = v

  for dirpath, dirnames, filenames in os.walk(imagesDir):
    if len(dirnames) != 0 and dirnames[0].startswith('S'):
      all_subjects = dirnames

    rema = re.search(r'\d+$', dirpath);
    if rema is not None:
      print(rema.groups())
      #if dirpath.endswith('00'): 
      if len(filenames) != 0 and filenames[len(filenames)-1].endswith('png'):
        all_images.append(os.path.join(dirpath, filenames[len(filenames) - 1]));


  for dirpath, dirnames, filenames in os.walk(emotionsDir): 
    rema = re.search(r'\d+$', dirpath);
    if rema is not None:
      if len(filenames) != 0 and filenames[0].endswith('emotion.txt'):
         emo_filepath = os.path.join(dirpath, filenames[0]);
         print(emo_filepath)
    #print(fs)
    #if fs[1] == "txt":
      #print (fs)
      #shutil.copy(dirpath + "\\" + f, outputDir + "\\" + fs[0][0:2] + "0" + fs[0][2:-1] + "." + fs[1])
  import pdb; pdb.set_trace();
if __name__ == '__main__':
  main(sys.argv[1:])
