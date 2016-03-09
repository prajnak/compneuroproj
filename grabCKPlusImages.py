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
  outputDir = '/Users/pulsar/Documents/compneuroproj/StraightImages1'
 
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
                      '7': 'SU',
                      '8': 'NA'
  }
  all_images = []; #paths to the last image for each subject
  all_subjects = None;
  all_emotions = []; # only 327 or so of the 500 sequences are labeled with an emotion
  gender = 'U'; #no gender info provided for ck+ dataset
  
  new_imagenames = [] 
  for k,v in optlist:
    if k == "-h":
      print "Usage: python grabCKPlusImages.py [-i INPUT_DIR -o OUTPUT_DIR]"
      return
    elif k == "-i":
      inputDir = v
    elif k == "-o":
      outputDir = v

  for dirpath, dirnames, filenames in os.walk(emotionsDir): 
    rema = re.search(r'\d+$', dirpath);
    if rema is not None:
      if len(filenames) != 0 and filenames[0].endswith('emotion.txt'):
         emo_filepath = os.path.join(dirpath, filenames[0]);
         f = open(emo_filepath, 'r'); 
         emo_code = str(int(float(f.readlines()[0].strip(' ').strip('\n'))))
         f.close()
         #print(emotion_map[emo_code], emo_code) 
         subject_number = emo_filepath.split('/')[-1].split('_emotion.txt')[0].split('_')[0].strip('S')
         new_filename = 'C' + gender + subject_number + emotion_map[emo_code] + '.png';
         
         ## strip out the directory path from emotion and onwards and also strip _emotion.txt and create a new filename for the image
         all_emotions.append((''.join(emo_filepath.split('Emotion/')[1]).split('_emotion.txt')[0], 
                              new_filename))
         print(all_emotions[-1])
  print(len(set(all_emotions)), len(all_emotions))
  all_emotions = dict(all_emotions)
  #import pdb; pdb.set_trace()
  for dirpath, dirnames, filenames in os.walk(imagesDir):
    if len(dirnames) != 0 and dirnames[0].startswith('S'):
      all_subjects = dirnames

    rema = re.search(r'\d+$', dirpath); #look for folders ending in digits
    if rema is not None:
      #if dirpath.endswith('00'): 
      if len(filenames) != 0 and filenames[len(filenames)-1].endswith('png'):
        all_images.append(os.path.join(dirpath, filenames[len(filenames) - 1]));
        img_filepath = os.path.join(dirpath, filenames[-1]);
        search_term = ''.join(img_filepath.split('/cohn-kanade-images/')[1]).split('.png')[0]
        #import pdb; pdb.set_trace()
        new_filename = 'oops'
        try: 
          new_filename = all_emotions[search_term]
        except KeyError:
          # this means this image sequence does not have an emotion label 
          subject_number = img_filepath.split('/')[-1].split('.png')[0].split('_')[0].strip('S')
          new_filename = 'C' + gender + subject_number + emotion_map['8'] + '.png' 
        new_fullpath = os.path.join(outputDir, new_filename)
        if new_fullpath not in new_imagenames:
          new_imagenames.append(new_fullpath)
        print(new_fullpath)
        shutil.copy(img_filepath, new_fullpath)

  from collections import Counter
  print(len(set(new_imagenames)), len(new_imagenames))
  # print([len(x) != 1 for x in Counter(new_imagenames)])
  print(Counter(new_imagenames))
if __name__ == '__main__':
  main(sys.argv[1:])
