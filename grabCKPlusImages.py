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
  all_images = []; #paths to the last image for each subject
  all_subjects = None;
  all_emotions = []; # only 300 or so of the 500 sequences are labeled with an emotion
  gender = 'U'; #no gender info provided for ck+ dataset
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
      #if dirpath.endswith('00'): 
      if len(filenames) != 0 and filenames[len(filenames)-1].endswith('png'):
        all_images.append(os.path.join(dirpath, filenames[len(filenames) - 1]));


  for dirpath, dirnames, filenames in os.walk(emotionsDir): 
    rema = re.search(r'\d+$', dirpath);
    if rema is not None:
      if len(filenames) != 0 and filenames[0].endswith('emotion.txt'):
         emo_filepath = os.path.join(dirpath, filenames[0]);
         all_emotions.append(emo_filepath)
         f = open(emo_filepath, 'r'); 
         emo_code = str(int(float(f.readlines()[0].strip(' ').strip('\n'))))
         f.close()
         print(emotion_map[emo_code], emo_code) 
         subject_number = emo_filepath.split('/')[-1].split('_emotion.txt')[0].split('_')[0].strip('S')
         new_filename = 'C' + gender + subject_number + emotion_map[emo_code] + '.png';
         print(new_filename)
         ## strip out the _emotion.txt and create a new filename for the image
      #shutil.copy(dirpath + "\\" + f, outputDir + "\\" + fs[0][0:2] + "0" + fs[0][2:-1] + "." + fs[1])
if __name__ == '__main__':
  main(sys.argv[1:])
