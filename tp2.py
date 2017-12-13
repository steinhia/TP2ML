#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import math
import cv2
from matplotlib import pyplot as plt
from createGlobalEllipseDataBase import Ellipse
from createGlobalEllipseDataBase import loadGlobalListFromFile


scaleFactor=1.2
minNeighbors=7


def testScaleFactor(ellipseDict):
    minNeighbors=3
    L=[]
    for i in np.arange(1.1,1.2,0.1):
        rate=testDataBase(i,minNeighbors,ellipseDict)
    return rate

def testMinNeighbors(ellipseDict):
    scaleFactor=1.2
    [TP,FP,FN]=[0,0,0]
    for i in range(1,11):
        rate=testDataBase(scaleFactor,i,ellipseDict)
    return rate
        

def testDataBase(scaleFactor,minNeighbors,ellipseDict):
    rate=[0,0,0]
    i=0
    l=len(ellipseList)
    n_images=0
    for ellipses in ellipseDict:
        i+=1
        if(i<100):
            if(i%100==0):
                print str(i) + "/" + str(l)
            ellipseFilename=ellipseDict[ellipses][0].imageFileName       
            res=UnitTest(scaleFactor,minNeighbors,ellipseFilename,False)
            if(res!=-1):
                n_images+=1
                anal=analyseResult(res,ellipseDict[ellipses])
                if(False):#anal[2]-anal[0]>2):
                    print anal
                    print ellipseFilename
                if(anal[0]+anal[1]==0):
                    TPR=0
                else:
                    TPR=anal[0]/(anal[0]+anal[1])
                if(anal[0]+anal[2]==0):
                    PPV=0
                else:
                    PPV=anal[0]/(anal[0]+anal[2])
                F1=2*anal[0]/(2*anal[0]+anal[2]+anal[1])
                #anal=[TPR,PPV,F1]
                rate=[rate[j]+anal[j] for j in range(3)]
    #rate=[rate[j]/n_images for j in range(3)]
    print str(n_images) + " images lues"
    return rate
            
def UnitTest(scaleFactor,minNeighbors,ellipseFilename,trace):
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
    path="originalPics/" + ellipseFilename + ".jpg"
    img = cv2.imread(path)
    res=[]
    #if img is None:
        #print "image None"
        #print path
    if img is not None:
        #print "image OK"
        #print path
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
        res=[]
        for (x,y,w,h) in faces:
            if(trace):
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            else:
                res.append([x+w/2,y+h/2])
        if(trace):
            cv2.imshow('img',img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        res=-1
    return res

def isInsideEllipse(center,ellipse):
        X = (center[0]-ellipse.centerX)*math.cos(ellipse.angle) + (center[1]-ellipse.centerY)*math.sin(ellipse.angle)
        Y = -1*(center[0]-ellipse.centerX)*math.sin(ellipse.angle) + (center[1]-ellipse.centerY)*math.cos(ellipse.angle)
        return((pow(X,2)/pow(ellipse.majorAxisRadius,2)) + (pow(Y,2)/pow(ellipse.minorAxisRadius,2)) <= 1)


def  analyseResult(res,ellipses):
    TP=0
    NFound=len(res)
    NToFind=len(ellipses)
    for i in res:
        for ellipse in ellipses:
            if(isInsideEllipse(i,ellipse)):
                TP+=1
    FN=max(len(ellipses)-TP,0)
    FP=max(len(res)-TP,0)
    return [TP,FN,FP]

ellipseList = loadGlobalListFromFile("ellipseList.pkl")
UnitTest(1.2,5,"2002/08/02/big/img_838",True)
print "TP,FN,FP"
#print(testScaleFactor(ellipseList))
