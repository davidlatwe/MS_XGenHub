# -*- coding:utf-8 -*-
'''
Created on 2017.02.21

@author: davidpower
'''
from pymel.core import *
import maya.OpenMaya as om
import PySide.QtGui as QtGui



def getImageRes(imgPath):
	"""
	This was wrote in OpenMaya, but Qt is much simpler.
	"""
	imageFile = QtGui.QImage(imgPath)
	return imageFile.width(), imageFile.height()


def resizeImage(imgPath, newPath, imgSize, keepRatio= True):
	"""doc"""
	imageFile = om.MImage()
	imageFile.readFromFile(imgPath)
	imageFile.resize(imgSize[0], imgSize[1], keepRatio)
	imageFile.writeToFile(newPath, newPath.split('.')[-1])


def extendImage(imgPath, imgSize, bgColor):
	"""
	This was wrote in OpenMaya, but some how make Maya crash almost everytime,
	I think it was memory issue...
	Anyway, this is in Qt now.
	"""
	sourceImage = QtGui.QImage(imgPath)
	width = sourceImage.width()
	height = sourceImage.height()
	# check input image has only one side needs to extend
	widthExtend = width < imgSize[0] and height == imgSize[1]
	hightExtend = height < imgSize[1] and width == imgSize[0]
	if not (widthExtend or hightExtend):
		return
	# create extended image and fill with default color
	cr, cg, cb, ca = bgColor
	qFormat = QtGui.QImage.Format.Format_ARGB32
	extendImage = QtGui.QImage(imgSize[0], imgSize[1], qFormat)
	extendImage.fill(QtGui.QColor(cr, cg, cb, ca))
	# write in pixel
	def setPix(shift_x, shift_y, x, y):
		"""get source pixel with alpha 255 and set to extended image"""
		px = QtGui.QColor(sourceImage.pixel(shift_x, shift_y))
		px.setAlpha(255)
		extendImage.setPixel(x, y, px.rgba())
	
	for x in range(0, imgSize[0]):
		for y in range(0, imgSize[1]):
			if widthExtend:
				extend = (imgSize[0] - width) / 2
				if not (x < extend or x >= width + extend):
					setPix(x - extend, y, x, y)
			if hightExtend:
				extend = (imgSize[1] - height) / 2
				if not (y < extend or y >= height + extend):
					setPix(x, y - extend, x, y)
	# write out
	extendImage.save(imgPath)
