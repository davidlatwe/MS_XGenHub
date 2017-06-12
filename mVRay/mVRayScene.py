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
	for idx, vrsFile in enumerate(vrsceneList):
		addSceneContent(vrsFile, prefix= principalPrefix + principalList[idx])

	# modify object property(mtlwrapper)
	for principalName in principalList:
		for vrayPlugin in findByName(proxyPrefix + principalName + '*'):
			if vrayPlugin.type() == 'Node':
				# proxy ObjectID
				objId = ''
				if vrayPlugin.has('objectID'):
					objId = vrayPlugin.get('objectID')
				# proxy primary vis
				primVis = ''
				if vrayPlugin.has('primary_visibility'):
					primVis = vrayPlugin.get('primary_visibility')
				# proxy MtlWrapper
				wrapmtl = ''
				mtl = vrayPlugin.get('material')
				if mtl.type() == 'MtlWrapper':
					wrapmtl = mtl
				# modify principal Node
				for m in findByName(principalPrefix + principalName + '*'):
					if m.type() == 'Node':
						if objId:
							m.set('objectID', objId)
						if primVis:
							m.set('primary_visibility', primVis)
						if wrapmtl:
							m.set('material', wrapmtl)
				# jump to find next principal
				break

	# remove placeholder
	for vrayPlugin in findByName(proxyPrefix + '*'):
		delete(vrayPlugin)

	# adjust light linking
	litLinkingAdj(litLink_maya, proxyPrefix, principalPrefix, principalList)

	print 'Daddy\'s Home, honey.'
