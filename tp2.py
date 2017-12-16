#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import math
import cv2
from matplotlib import pyplot as plt
from createGlobalEllipseDataBase import Ellipse
from createGlobalEllipseDataBase import loadGlobalListFromFile
from loadWIDERFaces import WIDERDatabaseLoader
from loadWIDERFaces import WIDER_IMAGE_FOLDER
from os import path

TRACE=False
USE_WIDER_DB=False

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
profil_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_profileface.xml')

def scaleValuesForPlottingTestScaleFactor(dico): # prend en entrée le résultat de testScaleFactor
    dicoSorted = sorted(dico.items(), key=lambda t: t[0])
    lengthDico = len(dicoSorted)
    result = []
    for i in range(0,lengthDico):
        result.append(dicoSorted[i][0])
    return result

def resultTestScaleFactor(dico,result="TPR"):
    scaleValue = scaleValuesForPlottingTestScaleFactor(dico);
    resultVector = []

    if result == "TPR":
        index = 0
    elif result == "PPV":
        index = 1
    elif result == "F1":
        index = 2
    else:
        return None

    for value in scaleValue:
        resultVector.append(dico[value][index])

    return resultVector
        
    
def testScaleFactor(ellipseDict):
    minNeighbors=3
    L=[]
    dico=dict()
    for i in np.arange(1.05,1.2,0.1):
        print "Test scale, value=", i
        rate=testDataBase(i,minNeighbors,ellipseDict)
        dico[i]=rate
    return dico

def testMinNeighbours(ellipseDict):
    scaleFactor=1.2
    dico=dict()
    for i in range(1,11):
        print "Test min neighbours, value=", i
        rate=testDataBase(scaleFactor,i,ellipseDict)
        dico[i]=rate
    return dico
        

def testDataBase(scaleFactor,minNeighbors,ellipseDict):
    rate=[0,0,0]
    rateLittle=[0,0,0]
    i=0
    rateBig=[0,0,0]
    n_images=0
    n_imagesLittle=0
    n_imagesBig=0
    for ellipses in ellipseDict:
        i+=1
        if(i<200 and i>=100):
            #if(i%10==0):
            #    print i

            ellipseFilename=ellipseDict[ellipses][0].imageFileName
            res=UnitTest(scaleFactor,minNeighbors,ellipseFilename,TRACE)
            if(res!=-1):
                n_images+=1
                anal=analyseResult(res,ellipseDict[ellipses])
                if(anal[0]+anal[1]==0):
                    TPR=0
                else:
                    TPR=float(anal[0])/float(anal[0]+anal[1])
                if(anal[0]+anal[2]==0):
                    PPV=0
                else:
                    PPV=float(anal[0])/float(anal[0]+anal[2])
                F1=2*float(anal[0])/float(2*anal[0]+anal[2]+anal[1])              
                anal=[TPR,PPV,F1]
                rate=[rate[j]+anal[j] for j in range(3)]
                if(len(ellipseDict[ellipseFilename])<4):
                    rateLittle=[rateLittle[j]+anal[j] for j in range(3)]
                    n_imagesLittle+=1
                if(len(ellipseDict[ellipseFilename])>3):
                    rateBig=[rateBig[j]+anal[j] for j in range(3)]
                    n_imagesBig+=1

    rate=[rate[j]/n_images for j in range(3)]
    rateBig=[rateBig[j]/n_imagesBig for j in range(3)]
    rateLittle=[rateLittle[j]/n_imagesLittle for j in range(3)]
#    print str(n_images) + " images lues"
#    print "rate"
#    print rate
#    print "rateLittle"
#    print rateLittle
#    print "big"
#    print rateBig
    return [rateLittle,rateBig,rate]
            
def UnitTest(scaleFactor,minNeighbors,ellipseFilename,trace):
    if USE_WIDER_DB:
        path=WIDER_IMAGE_FOLDER + ellipseFilename
        #print path
    else:
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
        profiles = profil_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
        res=[]
        for (x,y,w,h) in faces:
            if(trace):
                print "face"
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            else:
                res.append([x+w/2,y+h/2])
        for (x,y,w,h) in profiles:
            if(trace):
                print "profil"	
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            else:
                res.append([x+w/2,y+h/2])
        
        if(trace):
            cv2.imshow('img',img)
            #cv2.imwrite(ellipseFilename+"_detect.jpg",img)
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
    for i in res:
        for ellipse in ellipses:
            if(isInsideEllipse(i,ellipse)):
                TP+=1
    FN=max(len(ellipses)-TP,0)
    FP=max(len(res)-TP,0)
    #if(float(TP)/float(len(ellipses))<1 and len(ellipses)>5):
    #    print TP
    #    print FN
    #    for ellipse in ellipses:
    #        print ellipse
    return [TP,FN,FP]


if USE_WIDER_DB:
    loader = WIDERDatabaseLoader()
    ellipseList = loader.getFacesMap()
else:
    ellipseList = loadGlobalListFromFile("ellipseList.pkl")

#UnitTest(1.2,5,"images_unitaires/profil2.jpg",True)
#UnitTest(1.2,5,"2002/07/19/big/img_576",True)

#print "TP,FN,FP"
scaleFactor=1.2
minNeighbors=3

print "Test scale..."
scale = testScaleFactor(ellipseList)
xValue = scaleValuesForPlottingTestScaleFactor(scale)
TPR_scale = resultTestScaleFactor(scale,result="TPR")
PPV_scale = resultTestScaleFactor(scale,result="PPV")
F1_scale = resultTestScaleFactor(scale,result="F1")

print "Test min neighbours..."
xValueNB = [i for i in range(1,11)]
neighbours = testMinNeighbours(ellipseList)
TPR_nb = resultTestScaleFactor(neighbours,result="TPR")
PPV_nb = resultTestScaleFactor(neighbours,result="PPV")
F1_nb = resultTestScaleFactor(neighbours,result="F1")

print "Plotting..."
plt.plot(xValueNB, TPR_nb)
plt.show()
plt.plot(xValueNB,PPV_nb)
plt.show()
plt.plot(xValueNB,F1_nb)
plt.show()


