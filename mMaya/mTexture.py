# -*- coding:utf-8 -*-
'''
Created on 2017.02.21

@author: davidpower
'''
import os
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore


class MQImage(QtGui.QImage):
	"""doc"""
	def __init__(self, *args):
		QtGui.QImage.__init__(self, *args)
		self.__imageFilePath = ''
		if type(args[0]) == 'string':
			if os.path.isfile(args[0]):
				self.__imageFilePath = args[0]
	
	def getImageFilePath(self):
		return str(self.__imageFilePath)
	
	def setImageFilePath(self, setImgPath):
		self.__imageFilePath = setImgPath


def __outWARNING(msg):
	"""doc"""
	print '[mTexture]  !  : ' + msg

def __outERROR(msg):
	"""doc"""
	print '[mTexture] !!! : ' + msg


def getImageRes(imgPath):
	"""
	This was wrote in OpenMaya, but Qt is much simpler.
	"""
	imageFile = MQImage(imgPath)
	return imageFile.width(), imageFile.height()


def resizeImage(mqImgSrc, imgSize, keepRatio= True):
	"""
	If pixel in the QImage has rgb value but alpha is 0,
	the rgb value will be lost after scale while alpha still be kept.
	"""
	aspectMode = QtCore.Qt.KeepAspectRatio if keepRatio else QtCore.Qt.IgnoreAspectRatio
	transMode = QtCore.Qt.SmoothTransformation
	return MQImage(mqImgSrc.scaled(imgSize[0], imgSize[1], aspectMode, transMode))


def extendImage(sourceImage, imgSize, bgColor):
	"""
	This was wrote in OpenMaya, but some how make Maya crash almost everytime,
	I think it was memory issue...
	Anyway, this is in Qt now.
	"""
	imgPath = sourceImage.getImageFilePath()
	width = sourceImage.width()
	height = sourceImage.height()
	# check input image has only one side needs to extend
	widthExtend = width < imgSize[0] and height == imgSize[1]
	hightExtend = height < imgSize[1] and width == imgSize[0]
	if not (widthExtend or hightExtend):
		__outWARNING('Image size not matched at all.')
		__outWARNING('Input -> w, h : ' + str([width, height]))
		__outWARNING('extTo -> w, h : ' + str([imgSize[0], imgSize[1]]))
		__outWARNING('Extend stop.')
		return sourceImage
	# create extended image and fill with default color
	cr, cg, cb, ca = bgColor
	if sourceImage.hasAlphaChannel():
		qFormat = QtGui.QImage.Format.Format_ARGB32
	else:
		qFormat = QtGui.QImage.Format.Format_RGB32
	extendImage = MQImage(imgSize[0], imgSize[1], qFormat)
	extendImage.setImageFilePath(imgPath)
	extendImage.fill(QtGui.QColor(cr, cg, cb, ca))
	# write in pixel	
	for x in range(0, imgSize[0]):
		for y in range(0, imgSize[1]):
			if widthExtend:
				extend = (imgSize[0] - width) / 2
				if not (x < extend or x >= width + extend):
					extendImage.setPixel(x, y, sourceImage.pixel(x-extend, y))
			if hightExtend:
				extend = (imgSize[1] - height) / 2
				if not (y < extend or y >= height + extend):
					extendImage.setPixel(x, y, sourceImage.pixel(x, y-extend))
	return extendImage


def paintTextWatermark(mqImg, text, pos, textColor, font= 'Arial', fontSize= 30, bold= True, italic= True):
	"""doc"""
	cr, cg, cb, ca = textColor
	qColor = QtGui.QColor(cr, cg, cb, ca)
	qFont = QtGui.QFont(font, fontSize, 1, italic)
	qFont.setBold(bold)
	# start paint
	painter = QtGui.QPainter()
	painter.begin(mqImg)
	painter.setPen(qColor)
	painter.setFont(qFont)
	painter.drawText(pos[0], pos[1], text)
	painter.end()
	return mqImg
