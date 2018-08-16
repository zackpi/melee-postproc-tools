import cv2
import numpy as np
import sys

"""
Get frames from a video stream one at a time
@param  vidfile     str   source video filename
@param  offset      int   offset of first frame
@param  nframes     int   number of frames to return (-1==all)
@return frames      list[nparray(uint8,3)]  frames from vidfile
"""
def yield_frames(vidfile, offset=0, nframes=-1):
    vid = cv2.VideoCapture(vidfile)
    assert vid.isOpened(), "Failed to open video stream from: " + str(vidfile)
    
    while offset:
        vid.read()
        offset -= 1
    
    n = 0
    if nframes == -1:
        nframes = sys.maxsize
     
    while vid.isOpened():
        n += 1
        if n > nframes:
            break        
        ret, frame = vid.read()
        if ret:
            yield frame
        else:
            break
    
    if vid.isOpened():
        vid.release()

"""
Get all frames from a video at once (see yield_frames above)
"""
def return_frames(vidfile, **kwargs):
    return list(yield_frames(vidfile, **kwargs))


"""
Return the image with a canny edge detector applied
"""
def edge_detect(img):
    b,g,r = cv2.split(img)
    b = cv2.Canny(cv2.GaussianBlur(b, (5,5), 0), 50, 200)
    g = cv2.Canny(cv2.GaussianBlur(g, (5,5), 0), 50, 200)
    r = cv2.Canny(cv2.GaussianBlur(r, (5,5), 0), 50, 200)
    return cv2.merge((b,g,r))


"""
Return the image with as regions of color
"""
def region_detect(img):
    big = cv2.resize(img, (0,0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(big, cv2.COLOR_BGR2HSV)
    kernel = np.ones((5,5), dtype=np.uint8)
    
    falco1 = cv2.inRange(hsv, (156, 155, 61), (167, 183, 165))
    falco2 = cv2.inRange(hsv, (253, 173, 114), (254, 178, 186))
    falco3 = cv2.inRange(hsv, (17, 89, 28), (58, 183, 48))
    falco = cv2.bitwise_or(cv2.bitwise_or(falco1, falco2), falco3)
    falco = cv2.morphologyEx(falco, cv2.MORPH_OPEN, kernel)
    
    return cv2.resize(falco, (0,0), fx=1/3, fy=1/3)


if __name__=="__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument("video", help="source of frames")
    parser.add_argument("--output", "-o", nargs=1, help="output filename", default="ctrlr_inputs")
    args = parser.parse_args()
    
    
    for frame in yield_frames(args.video, offset=900, nframes=-1):
        cv2.imshow("stream", region_detect(frame))
        if cv2.waitKey(1) == 27:
            break
    
    
