# -*- coding:utf-8 -*-
'''
Created on 2017.02.21

@author: davidpower
'''
from pymel.core import *
import maya.OpenMaya as om


def getTextureRes(imgPath):
	"""
	"""
	utilWidth = om.MScriptUtil()
	utilWidth.createFromInt(0)
	ptrWidth = utilWidth.asUintPtr()
	utilHeight = om.MScriptUtil()
	utilHeight.createFromInt(0)
	ptrHeight = utilHeight.asUintPtr()
	
	try:
		textureFile = om.MImage()
		textureFile.readFromFile ( imgPath )
		textureFile.getSize(ptrWidth, ptrHeight)
		width = om.MScriptUtil.getUint(ptrWidth)
		height = om.MScriptUtil.getUint(ptrHeight)

		return width, height

	except:
		warning( 'Texture Res error: ' + imgPath )
		
		return None


def resizeTexture(imgPath, newPath, imgSize, preserveAspectRatio= True):
	"""
	"""
	try:
		textureFile = om.MImage()
		textureFile.readFromFile(imgPath)
		textureFile.resize(imgSize[0], imgSize[1], preserveAspectRatio)
		textureFile.writeToFile(newPath, newPath.split('.')[-1])
	except Exception, e:
		warning('image file resize error: ' + imgPath)
		print e
		error('Failed resize image to: ' + newPath)