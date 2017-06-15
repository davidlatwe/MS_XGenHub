# -*- coding:utf-8 -*-
'''
Created on 2017.06.07

@author: davidpower
'''
import pymel.core as pm
import xgenm as xg



def getHairCurves(descHairSysName):
	"""
	List out curves which output from descHairSysName
	"""
	# since we had our nHairSystem well named, we can search it by name
	hsysList = pm.ls(descHairSysName)
	curves = []
	if hsysList and hsysList[0].getShape().type() == 'hairSystem':
		# find curves
		hsys = hsysList[0].getShape()
		follicles = pm.listConnections(hsys.inputHair, sh= True, type= 'follicle')
		for foll in follicles:
			curve = pm.listConnections(foll.outCurve, sh= True, type= 'nurbsCurve')
			curves.extend(curve)
	return curves


def nRigidRename(meshPatch, nRigidNameVar):
	"""doc"""
	# rename rigid body
	renameDict = {}
	for rigid in pm.ls(type= 'nRigid'):
		shp = rigid.inputMesh.listConnections(sh= 1)
		if shp and shp[0].type() == 'mesh':
			meshName = shp[0].getParent().name()
			if meshName in meshPatch:
				print rigid.name()
				renameDict[rigid.name()] = meshName
	for rigidName in renameDict:
		rigid = pm.ls(rigidName)
		if rigid:
			rigid[0].getParent().rename(nRigidNameVar % renameDict[rigidName])


def exportCurvesMel(palName, descName, fxmName):
	"""doc"""
	# setup
	value = xg.getAttr('exportDir', palName, descName, fxmName)
	xg.setAttr('exportDir', str(value), palName, descName, fxmName)
	xg.setAttr('exportCurves', 'true', palName, descName, fxmName)
	#
	# Need to fill in the export faces to correct value
	#
	xg.setAttr('exportFaces', '', palName, descName, fxmName)
	# export clumpCurves.mel
	pm.mel.xgmNullRender(descName, percent= 0)
	# get clumpCurves.mel file path
	curvesMelPath = xg.getAttr('_fullExportDir', palName, descName, fxmName)
	# remove clumpCurves.mel's last cmd : "xgmMakeCurvesDynamic;"
	print 'Reading curves mel. -> ' + curvesMelPath
	curvesMel = open(curvesMelPath, 'r').readlines()
	cmdIndex = curvesMel.index('xgmMakeCurvesDynamic;\n')
	curvesMel[cmdIndex] = ''
	# execute it, and we will run our MakeCurvesDynamic later
	pm.mel.eval(''.join(curvesMel))
	# restore
	xg.setAttr('exportCurves', 'false', palName, descName, fxmName)
	xg.setAttr('exportFaces', '', palName, descName, fxmName)
	

def xgmMakeCurvesDynamic(descHairSysName, collide):
	"""
	Create nHairSystem with good name before MakeCurvesDynamic
	and without optionBox UI
	"""
	keepSele = pm.ls(sl= 1)
	# find hair holding mesh for later rigid body rename
	meshPatch = []
	for dag in keepSele:
		if dag.getShape().type() == 'mesh':
			meshPatch.append(dag.name())
	# create the first time we hit a valid curve
	hsys = pm.createNode('hairSystem')
	hsys.getParent().rename(descHairSysName)
	# we want uniform stiffness because the curves
	# are initially point locked to both ends 
	pm.removeMultiInstance(hsys.stiffnessScale[1], b= True)
	hsys.clumpWidth.set(0.00001)
	hsys.hairsPerClump.set(1)
	pm.connectAttr('time1.outTime', hsys.currentTime)
	nucleus = pm.mel.getActiveNucleusNode(False, True)
	pm.mel.addActiveToNSystem(hsys, nucleus)
	pm.connectAttr(nucleus + '.startFrame', hsys.startFrame)

	# select the hairSystem we just created and well named,
	# and maya won't create one when making curves dynamic
	keepSele.append(hsys)
	# re-select curves, mesh and hairSystem
	pm.select(keepSele, r= 1)
	# trun on 'Collide With Mesh'
	pm.optionVar(intValue= ['makeCurvesDynamicCollideWithMesh', int(collide)])
	# MakeCurvesDynamic callback
	pm.mel.eval('makeCurvesDynamic 2 { "1", "1", "1", "1", "0"}')

	return meshPatch, hsys


def attachSlot(palName, descName, fxmName, descHairSysName):
	"""doc"""
	if not xg.fxModuleType(palName, descName, fxmName) == 'AnimWiresFXModule':
		return

	refwFrame = xg.getAttr('refWiresFrame', palName, descName, fxmName)
	if xg.getAttr('liveMode', palName, descName, fxmName) == 'false':
		wiresfile = xg.getAttr('wiresFile', palName, descName, fxmName)
		pm.mel.xgmFindAttachment(d= descName, f= wiresfile, fm= int(refwFrame), m= fxmName)
	else:
		curves = getHairCurves(descHairSysName)
		if curves:
			# attach wires to curves
			pm.select(curves, r= 1)
			pm.mel.xgmFindAttachment(d= descName, fm= int(refwFrame), m= fxmName)
			print 'The following curves were attached: ',[c.name() for c in curves]
		else:
			print 'No curves selected. Nothing to attach.'


