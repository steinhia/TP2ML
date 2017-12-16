#!/usr/bin/python
# -*- coding: utf-8 -*-

from createGlobalEllipseDataBase import Ellipse

WIDER_IMAGE_FOLDER = "WIDER_train/images/"
WIDER_BBOX_FILE = "WIDER_train/wider_face_train_bbx_gt.txt"

class WIDERDatabaseLoader:
    # Private attributes 
    _faceMap = {}

    # Constructor
    def __init__(self):
        lineIndex = 0

        f = open(WIDER_BBOX_FILE, "r")
        filename = f.readline().strip()

        # store everything in a dictionary
        while filename:
            nbFaces = int(f.readline())
            ellipseArray = []
            lineIndex += 2

            for i in range(0,nbFaces):
                data = f.readline().split(" ")
                majorRadius = int(data[2])
                minorRadius = int(data[3])
                angle = 0
                centerX = int(data[0]) + int(data[2])/2
                centerY = int(data[1]) + int(data[3])/2
                ellipse = Ellipse(filename, majorRadius, minorRadius, angle, centerX, centerY)
                ellipseArray.append(ellipse)
            #end for

            self._faceMap[filename] = ellipseArray;

            filename = f.readline().strip()
        #end while
    #end __init__

    # Returns a <string,list<Ellipse>> map 
    def getFacesMap(self):
        return self._faceMap;
    #end getFacesMap

#end WIDERDatabaseLoader

##############################
#loader = WIDERDatabaseLoader()
#for name, faceList in loader.getFacesMap().items():
#    print "************"
#    for ellipse in faceList:
#        print ellipse
#    print "************"
##############################

