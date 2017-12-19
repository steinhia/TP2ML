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
import time
import pickle

from tp2 import scaleValuesForPlottingScaleFactor
from tp2 import resultTestScaleFactor



with open("resScale.pkl",'rb') as f:
	scale=pickle.load(f)
	print "Plotting scale..."
	xValue = scaleValuesForPlottingTestScaleFactor(scale)
	TPR_scale = resultTestScaleFactor(scale,result="TPR")
	PPV_scale = resultTestScaleFactor(scale,result="PPV")
	F1_scale = resultTestScaleFactor(scale,result="F1")
	plt.plot(xValue, TPR_scale)
	plt.show()
	plt.plot(xValue,PPV_scale)
	plt.show()
	plt.plot(xValue,F1_scale)
	plt.show()



with open("restime.pkl",'rb') as f:
	[times,values]= pickle.load(f)
	plt.plot(values,times)
	print "Plotting time..."
	plt.show()
with open("minN30.pkl",'rb') as f:
	neighbours=pickle.load(f)
	TPR_nb = resultTestScaleFactor(neighbours,result="TPR")
	PPV_nb = resultTestScaleFactor(neighbours,result="PPV")
	F1_nb = resultTestScaleFactor(neighbours,result="F1")

	print "Plotting minN..."
	#plt.plot(xValueNB, TPR_nb)
	#plt.show()
	#plt.plot(xValueNB,PPV_nb)
	#plt.show()
	#plt.plot(xValueNB,F1_nb)
	#plt.show()


with open("resClass.pkl",'rb') as f:
	[neighbours1,neighbours2,neighbours3]=pickle.load(f)

