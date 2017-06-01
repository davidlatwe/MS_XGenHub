# -*- coding:utf-8 -*-
'''
Created on 2017.05.27

@author: davidpower

This was copied and modified from Autodesk offical xgen module [xgmExternalAPI.py]
'''

import os
import maya.cmds as cmds
import maya.mel as mel
import xgenm as xg
import xgenm.XgExternalAPI as base
import xgenm.xgUtil as xgutil


def setupDescriptionFolder( paletteRoot, palette, newDesc='' ):
	""" create the description folders """
	descrs = None
	if len(newDesc):
		descrs = [newDesc]
	else:
		descrs = base.descriptions( palette )

	for desc in descrs:
		descDir = os.path.join(paletteRoot, desc)
		if not os.path.exists(descDir):
			os.mkdir(descDir)


def setupImportedMap(fileName, palName, descNames, uniqDescNames, nameSpace):
	'''
	When import palette or description, set up attributes with map texture.
	The setup steps include:
	  1, parses the imported file again;
	  2, read the "MapTextures" section;
	  3, for each map, create an attribute for bound geometry; then connect 
		 a texture node to the attribute.
	'''

	# parse the file, get its path of pallete
	fp = open(fileName, 'r')
	for line in fp:
		#print line
		line = line.strip(' \t\r\n') 
		
		if cmp(line, "Description") == 0:
			line = fp.next()
			line = line.strip(' \t\r\n')

			preDescription = line.split('\t', 3)[3]
			curDescription = uniqDescNames[0]
			for i in range(len(descNames)):
				if descNames[i] == preDescription:
					curDescription = uniqDescNames[i]

			line = fp.next()
			line = line.strip(' \t\r\n')
			while line and cmp(line, "endAttrs"):
				if line.startswith("xgDataPath"):
					xgDataPath = line.split("\t")[2]
				elif line.startswith("xgProjectPath"):
					xgProjectPath = line.split("\t")[2]
					palPath = ""
					if xgDataPath.startswith("${PROJECT}"):
						palPath = xgDataPath.replace("${PROJECT}", xgProjectPath)
						# copy description dir
						projRoot = cmds.workspace(query=True, rootDirectory=True)
						curPalDir = os.path.join(projRoot, "xgen", "collections", palName)
						
						srcdir = os.path.join(palPath, preDescription)
						dstdir = os.path.join(curPalDir, curDescription)
						xgutil.copyFolder(srcdir, dstdir)
					else:
						cmds.error( 'Cannot get palette Path.' )
				line = fp.next()
				line = line.strip(' \t\r\n')

		elif cmp(line, "MapTextures") == 0:
			# [David] Not Sure about this area
			geoms = xg.boundGeometry( palName, curDescription )
			
			line = fp.next()
			line = line.strip(' \t\r\n') 
			while line and cmp(line, "endAttrs"):
				segments = line.split("\t")
				
				isColor = cmp(segments[1], "regionMap") == 0
				# create attribute for shape and assign texture
				if isColor:
					shapeAttrName = xg.createMayaAttr( [0.5, 0.5, 0.5], segments[1], palName, curDescription )
				else:
					shapeAttrName = xg.createMayaAttr( [0.5], segments[1], palName, curDescription )

				for geom in geoms:
					texNode = cmds.shadingNode("file", asTexture=True)
					place2dNode = cmds.shadingNode("place2dTexture", asUtility=True)
					mel.eval("fileTexturePlacementConnect( \""+ texNode + "\", \"" + place2dNode + "\" )")
					cmds.connectAttr (place2dNode + ".outUV", texNode + ".uv")
					cmds.connectAttr (place2dNode + ".outUvFilterSize", texNode + ".uvFilterSize")
					
					cmds.setAttr(texNode+".ftn", segments[2], type="string")
					if isColor:
						ip = texNode + ".outColor"
					else:
						ip = texNode + ".outAlpha"
					shapeChildren = cmds.listRelatives( geoms, shapes=True )
					shapeAttrName2 = shapeChildren[0] + "." + shapeAttrName
					cmds.connectAttr (ip, shapeAttrName2)
						
				line = fp.next()
				line = line.strip(' \t\r\n')
	fp.close()