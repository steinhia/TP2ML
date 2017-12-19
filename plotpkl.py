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

with open("resScale.pkl",'rb') as f:
	scale=pickle.load(f)
	print(scale)
with open("restime.pkl",'rb') as f:
	[times,values]= pickle.load(f)
	print(times)
	print(values)
with open("minN30.pkl",'rb') as f:
	minN=pickle.load(f)
	print(minN)
with open("resClass.pkl",'rb') as f:
	[neighbours1,neighbours2,neighbours3]=pickle.load(f)
	print(neighbours1)
	print(neighbours2)
	print(neighbours3)

