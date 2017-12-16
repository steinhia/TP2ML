#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
import pickle

class Ellipse():
    def __init__(self,imageFileName,majorAxisRadius,minorAxisRadius,angle,
                 centerX, centerY):
        self.imageFileName = imageFileName
        self.majorAxisRadius = majorAxisRadius
        self.minorAxisRadius = minorAxisRadius
        self.angle = angle
        self.centerX = centerX
        self.centerY = centerY

    def __str__(self):
        result = self.imageFileName + " "
        result += str(self.majorAxisRadius) + " "
        result += str(self.minorAxisRadius) + " "
        result += str(self.angle) + " "
        result += str(self.centerX) + " "
        result += str(self.centerY)
        return result
    
    @property
    def imageFileName(self):
        return self.imageFileName
    
    @property
    def majorAxisRadius(self):
        return self.majorAxisRadius

    @property
    def minorAxisRadius(self):
        return self.minorAxisRadius

    @property
    def angle(self):
        return self.angle

    @property
    def centerX(self):
        return self.centerX

    @property
    def centerY(self):
        return self.centerY

def parseEllipse(imagePath, line):
    splittedLine = line.split()
    imageFileName = imagePath
    majorAxisRadius = float(splittedLine[0])
    minorAxisRadius = float(splittedLine[1])
    angle = float(splittedLine[2])
    centerX = float(splittedLine[3])
    centerY = float(splittedLine[4])
    return Ellipse(imageFileName, majorAxisRadius, minorAxisRadius, angle, centerX, centerY)

def separateEllipseFileByImages(fileName):
    separateList = []
    with open(fileName,"r") as f:
        allLines = f.readlines()
        numberOfLine = len(allLines)
        currentLine = 0
        dico=dict()
        while currentLine < numberOfLine:
            imagePath = allLines[currentLine]
            if imagePath[-1:] == '\n':
                imagePath = imagePath[:-1]
            currentLine += 1
            numberOfEllipse = allLines[currentLine]
            currentLine += 1
            for i in range(0,int(numberOfEllipse)):
                if imagePath not in dico:
                        dico[imagePath] = []
                dico[imagePath].append(parseEllipse(imagePath,allLines[currentLine]))
                currentLine += 1
    return dico
    
def parseFaceAnnotationIntoEllipseList(folderName):
    dico=dict()
    for elem in listdir(folderName):
        if 'ellipse' in elem:
            d=separateEllipseFileByImages(folderName+"/"+elem)
            dico=dict(dico.items() + d.items())
    return dico

def saveGlobalListIntoFile(nameOfFile):
    with open(nameOfFile,'wb') as f:
        pickle.dump(parseFaceAnnotationIntoEllipseList("FDDB-folds"),f)

def loadGlobalListFromFile(nameOfFile):
    with open(nameOfFile,'rb') as f:
        return pickle.load(f)
    
#saveGlobalListIntoFile("ellipseList.pkl")

