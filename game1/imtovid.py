import os
import cv2
import re
from math import ceil

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    
def get_frame_rate(n_images, duration):
    nf = float(n_images)
    fps = (float(nf)/duration)
    
    if fps < 1:
        fps = 1
    return fps 


def make_movie(path_to_images, duration, output_name='output.mp4'):     
    
    if not output_name.endswith('.mp4'):
        output_name += '.mp4'
        
    images = []
    
    dir_path = path_to_images
    
    for f in os.listdir(dir_path):
        images.append(f)
    
    sort_nicely(images)
    
    im_path = os.path.join(dir_path, images[0])
    frame = cv2.imread(im_path)
    
    height, width, channels, = frame.shape
    
    try: 
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    except:
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
    
    n_images = len(images)
    
    fps = get_frame_rate(n_images, duration)
    
    print "Frame Rate: {0}".format(fps)
    print "Movie Duration: {0}".format(float(n_images)/fps)
    
    out = cv2.VideoWriter(output_name, fourcc, fps, (width, height))
    
    for i in images:
        im_path = os.path.join(dir_path, i)
        frame = cv2.imread(im_path)
        
        out.write(frame)
        
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
        
    out.release()
    cv2.destroyAllWindows()
