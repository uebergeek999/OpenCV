import cv2
import numpy as np
import sys
import time

folder = 'mpi/'

haar_path = 'C:/Users/tlsha/Anaconda3/Library/etc/haarcascades/'
faceCL = cv2.CascadeClassifier(haar_path+'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)
reader1 = cv2.VideoCapture('vid1.avi')
reader2 = cv2.VideoCapture('vid2.avi')
ret, frame = cap.read()

fourcc = cv2.VideoWriter_fourcc(*'XVID')

writer1 = cv2.VideoWriter(folder+'vid1.avi', fourcc, 20, (640,480), True)
writer2 = cv2.VideoWriter(folder+'vid2.avi', fourcc, 20, (640,480), True)


def read1_write2(frame_capture):
    '''Read from vid1.avi and write passed frame to vid2.avi'''
    global reader1, writer2
    ret, frame_read = reader1.read()
    
    writer2.write(frame_capture)
    if ret:
##        cv2.imshow("vid1.avi Display", frame_read)
##        cv2.moveWindow("vid1.avi Display", 700,10)
        return frame_read
    else:
        return np.zeros_like(frame_capture)

def read2_write1(frame_capture):
    '''Read from vid2.avi and write passed frame to vid1.avi'''
    global reader2, writer1
    ret, frame_read = reader2.read()

    writer1.write(frame_capture)
    if ret:
##        cv2.imshow("vid2.avi Display", frame_read)
##        cv2.moveWindow("vid2.avi Display", 700,500)
        return frame_read
    else:
        return np.zeros_like(frame_capture)

def init_read2_write1():
    '''Stop reading from vid1.avi
    Stop writing to vid2.avi
    then start reading from vid2.avi
    and start writing to vid1.avi
    '''
    global reader1, reader2, writer1, writer2
    
    print("\tclosing: r1, w2")
    reader1.release()
    writer2.release()

    print("\topening: r2, w1")
    writer1 = cv2.VideoWriter(folder+'vid1.avi', fourcc, 20, (640,480), True)
    reader2 = cv2.VideoCapture(folder+'vid2.avi')

def init_read1_write2():
    '''Stop reading from vid2.avi
    Stop writing to vid1.avi
    then start reading from vid1.avi
    and start writing to vid2.avi
    '''
    global reader1, reader2, writer1, writer2

    print("\tclosing: r2, w1")
    reader2.release()
    writer1.release()

    print("\topening: r1, w2")
    writer2 = cv2.VideoWriter(folder+'vid2.avi', fourcc, 20, (640,480), True)
    reader1 = cv2.VideoCapture(folder+'vid1.avi')
    
    

switch = False
newFace = False
noface_counter = 0
noface_buffer = 5 #frames
faces = []

while True:
    #standard live capture
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_read = np.zeros_like(frame)

    faces = faceCL.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        x,y = (faces[0][0], faces[0][1])
        w,h = (faces[0][2], faces[0][3])
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0))

        noface_counter = 0
        newFace = False
    else:
        noface_counter += 1
        print("no face for %d frames" %noface_counter)

    
    if noface_counter == noface_buffer:
        newFace = True


    if newFace: #this if decides WHEN to switch files
        print("switching")
        if switch:
            init_read2_write1()
        else:
            init_read1_write2()
        switch = not switch
        newFace = False

    if switch and not newFace:
        frame_read = read1_write2(frame) #FIXME: frame_read = None
    elif not switch and not newFace:
        frame_read = read2_write1(frame) #FIXME: frame_read = None

    #frame_read = np.zeros_like(frame) #FIXME: remove when above fixme's are fixed
    frame_blend = cv2.addWeighted(frame, 0.5, frame_read, 0.5, 0)

    cv2.imshow("LIVE CAPTURE - for reference", frame_blend)
    cv2.moveWindow("LIVE CAPTURE - for reference", 10,10)
    if cv2.waitKey(33) == 27:
        break



    
cap.release()
reader1.release()
reader2.release()
writer1.release()
writer2.release()

cv2.destroyAllWindows()
print("fin")
