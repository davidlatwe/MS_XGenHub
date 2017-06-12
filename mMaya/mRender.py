# -*- coding:utf-8 -*-
'''
Created on 2017.02.21

@author: davidpower
'''
import pymel.core as pm


def getVRaySettingsNode():
	"""
	Create vraySettings node without UI
	credit gose to Stas Poritskiy
	http://stascrash.com
	http://forums.cgsociety.org/showthread.php?t=1266983
	"""
	# check vray plugin loaded
	if not pm.pluginInfo('vrayformaya', q= 1, l= 1):
		pm.loadPlugin('vrayformaya')

	# Get Render-Node
	vraySetNode = pm.ls(type= 'VRaySettingsNode')

	if not vraySetNode:
		# Try and register vray
		try:
			pm.renderer('vray')
		except RuntimeError:
			print "Vray already Registered"
		# Collect all vray-Attributes
		globalsTabLabels = pm.renderer('vray', query= True, globalsTabLabels= True)
		globalsTabCreateProcNames = pm.renderer('vray', query= True, globalsTabCreateProcNames= True)
		globalsTabUpdateProcNames = pm.renderer('vray', query= True, globalsTabUpdateProcNames= True)
		# Construct Vray-Renderer
		for tab_id in range(len(globalsTabLabels)):
			pm.renderer('vray', edit=True, addGlobalsTab=[
				str(globalsTabLabels[tab_id]),
				str(globalsTabCreateProcNames[tab_id]),
				str(globalsTabUpdateProcNames[tab_id])
				])
		# Create DAG for VRAYSETTINGS
		pm.shadingNode('VRaySettingsNode', asUtility= True, name= 'vraySettings')

	return pm.PyNode('vraySettings')