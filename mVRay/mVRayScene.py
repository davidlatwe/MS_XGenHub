# -*- coding:utf-8 -*-
'''
Created on 2017.05.24

@author: davidpower
'''
# This module only works under vray standlone

"""
To replace proxy objects in the scene file with the principal objects
in all the vrscene files by the naming prefix.

In order to replace those objects, and don't mixed them up after loaded to vray,
we naming them with different prefix to identify.

ex:
In the scene file:			proxyBox_YellowBox
							proxyBox_RedBox

In the vrscene file:	principalBox_YellowBox
						principalBox_RedBox

"""
from vray.utils import *



def saveLightLinker(remove= True):
	"""
	preserve light link group and delete it, before any other process.
	"""
	litLinkSet = findByType('SettingsLightLinker')

	linkGrp = [
		'ignored_lights',
		'ignored_shadow_lights',
		'include_exclude_light_flags',
		'include_exclude_shadow_flags'
		]
	ignorLitList = litLinkSet[0].get(linkGrp[0]) if litLinkSet else []
	ignorSdwList = litLinkSet[0].get(linkGrp[1]) if litLinkSet else []
	ignorLitFlag = litLinkSet[0].get(linkGrp[2]) if litLinkSet else []
	ignorSdwFlag = litLinkSet[0].get(linkGrp[3]) if litLinkSet else []

	if remove and litLinkSet:
		delete(litLinkSet[0])
	
	return {'ignored_lights' : ignorLitList,
			'ignored_shadow_lights' : ignorSdwList,
			'include_exclude_light_flags' : ignorLitFlag,
			'include_exclude_shadow_flags' : ignorSdwFlag}


def litLinkingAdj(litLinkDict, proxyPrefix, principalPrefix, principalList):
	"""doc"""
	def replaceObjectsInLightLink(linkType):
		"""
		Replace proxy in lightLinkGroup to principal object which we want to render out,
		all the principal objects in the principalList should have uniqname,
		means one principal object name should not be other principal object name's prefix.
		like, 'myBox' and 'myBox_A',
		in this case, when we are looking for 'myBox', 'myBox_A' will be processed as well,
		which might not the result we want.
		"""
		for i, linkGrp in enumerate(litLinkDict[linkType]):
			new_linkGrp = []
			for j, vrayObj in enumerate(linkGrp):
				if j == 0:
					# first one in list is the light object name
					new_linkGrp.append(vrayObj)
					continue
				if vrayObj.name().startswith(proxyPrefix):
					principalName = ''
					for pn in principalList:
						if pn in vrayObj.name():
							principalName = pn;break;
					for m in findByName(principalPrefix + principalName + '*'):
						if m.type() == 'Node':
							# principal object Node found
							new_linkGrp.append(m)
				else:
					new_linkGrp.append(vrayObj)
			litLinkDict[linkType][i] = new_linkGrp

		return litLinkDict

	# create new lightLinker
	create('SettingsLightLinker', 'settingsLightLinker')
	litLinkSet = findByType('SettingsLightLinker')[0]

	if litLinkDict['ignored_lights']:
		litLinkDict = replaceObjectsInLightLink('ignored_lights')
	if litLinkDict['ignored_shadow_lights']:
		litLinkDict = replaceObjectsInLightLink('ignored_shadow_lights')
	
	litLinkSet.set('ignored_lights', litLinkDict['ignored_lights'])
	litLinkSet.set('ignored_shadow_lights', litLinkDict['ignored_shadow_lights'])


def replaceMaterial(vrayNode, replaceMtl):
	"""
	keep node but replace material
	"""
	originMtl = vrayNode.get('material')
	if originMtl and (originMtl.type() == 'MtlRenderStats' or originMtl.type() == 'MtlWrapper'):
		if originMtl.type() == 'MtlWrapper':
			originMtl.set('base_material', replaceMtl)
		else:
			originMtl_base = originMtl.get('base_mtl')
			if originMtl_base.type() == 'MtlWrapper':
				originMtl_base.set('base_material', replaceMtl)
			else:
				originMtl.set('base_mtl', replaceMtl)
	else:
		vrayNode.set('material', replaceMtl)


def replaceNodeParamValue(originNode, replaceNodeName):
	"""
	get proxy node render attribute values and set to replacement node
	"""
	# modify principal Node
	for replaceNode in findByName(replaceNodeName + '*'):
		if replaceNode.type() == 'Node':
			# proxy ObjectID
			if originNode.has('objectID'):
				replaceNode.set('objectID', originNode.get('objectID'))
			# proxy primary vis
			if originNode.has('primary_visibility'):
				replaceNode.set('primary_visibility', originNode.get('primary_visibility'))
			# proxy visible
			if originNode.has('visible'):
				replaceNode.set('visible', originNode.get('visible'))
			# proxy material
			if originNode.has('material'):
				replaceNode.set('material', originNode.get('material'))


def kickProxyOutWith(yourDaddy):
	"""
	@yourDaddy  this is a args list, for shorter line purpose

	@vrsceneList		vrscene file path list
	@principalList		principal object name list
	@proxyPrefix		proxy object name prefix in side the working scene
	@principalPrefix	principal object in side vrscene file's name prefix
	"""
	vrsceneList, principalList, proxyPrefix, principalPrefix = yourDaddy

	# save light linking
	litLink_maya = saveLightLinker()
	
	# add all vrscene
	DaddyArrived = False
	for idx, vrsFile in enumerate(vrsceneList):
		# check if proxy exists before we load principals
		if findByName(proxyPrefix + principalList[idx] + '*'):
			DaddyArrived = True
			addSceneContent(vrsFile, prefix= principalPrefix + principalList[idx])

	if DaddyArrived:
		# modify object property(mtlwrapper)
		for principalName in principalList:
			for proxyNode in findByName(proxyPrefix + principalName + '*'):
				if proxyNode.type() == 'Node':
					replaceNodeParamValue(proxyNode, principalPrefix + principalName)
					# jump to find next principal
					break

		# remove placeholder
		for proxyNode in findByName(proxyPrefix + '*'):
			delete(proxyNode)

		# adjust light linking
		litLinkingAdj(litLink_maya, proxyPrefix, principalPrefix, principalList)

		print 'Daddy\'s Home, honey.'
	else:
		print 'Daddy didn\'t come.'
