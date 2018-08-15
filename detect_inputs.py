import cv2
import numpy as np

def to_frames(vidfile, generate=True):
    vid = cv2.VideoCapture(vidfile)
    if !vid.isOpened():
        print()
        sys.exit(1)
    
    while vid.isOpened():
        ret, frame = vid.read()
        if ret:
            if generate:
                yield frame
        else:
            break

def find_regions(img):
    


if __name__=="__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument("video", description="source of frames")
    parser.add_argument("--output", "-o", nargs=1, description="output filename", default="ctrlr_inputs")
    args = parser.parse_args()
    
    
    
    
