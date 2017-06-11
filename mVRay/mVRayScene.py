from vray.utils import *

def saveLightLinker(litLinkSet):
	"""doc"""
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
	
	return {'ignored_lights' : ignorLitList,
			'ignored_shadow_lights' : ignorSdwList,
			'include_exclude_light_flags' : ignorLitFlag,
			'include_exclude_shadow_flags' : ignorSdwFlag}


def mayaLinkReplace(linkType, litLink_maya):
	"""doc"""
	for i, linkGrp in enumerate(litLink_maya[linkType]):
		new_linkGrp = []
		for j, mayaObj in enumerate(linkGrp):
			if j == 0:
				#print 'LINKED_LIGHT: ' + mayaObj.name()
				new_linkGrp.append(mayaObj)
				continue
			if mayaObj.name().startswith('pCube_lightLink_'):
				target = ''
				for th in targetHair:
					if th in mayaObj.name():
						target = th;break;
				for m in findByName(target + 'vrsHair*'):
					if m.type() == 'Node':
						#print '		LINK_FOUND: ' + m.name()
						new_linkGrp.append(m)
			else:
				new_linkGrp.append(mayaObj)
		litLink_maya[linkType][i] = new_linkGrp
	return litLink_maya


def litLinkingAdj(litLink_maya, geoPlaceholder, targetHair):
	"""doc"""
	create('SettingsLightLinker', 'settingsLightLinker')
	litLinkSet = findByType('SettingsLightLinker')[0]

	if litLink_maya['ignored_lights']:
		litLink_maya = mayaLinkReplace('ignored_lights', litLink_maya)
	if litLink_maya['ignored_shadow_lights']:
		litLink_maya = mayaLinkReplace('ignored_shadow_lights', litLink_maya)
	
	litLinkSet.set('ignored_lights', litLink_maya['ignored_lights'])
	litLinkSet.set('ignored_shadow_lights', litLink_maya['ignored_shadow_lights'])


def linkHair():
	"""doc"""
	targetHair = [
		'victor',
		'acht',
		'se7en',
		'akira'
		]
	geoPlaceholder = ['pCube_lightLink_' + th for th in targetHair]

	# save light linking
	litLinkSet = findByType('SettingsLightLinker')
	litLink_maya = saveLightLinker(litLinkSet)
	# remove it
	delete(litLinkSet[0]) if litLinkSet else None
	
	# add hair vrscene
	for th in targetHair:
		repoDir = 'P:/201611_AsusBrandVideo/Maya/renderData/vrscene/all4/'
		scenefile = repoDir + th + '_all4.vrscene'
		addSceneContent(scenefile, prefix= th + 'vrsHair')
	# modify hair object property(mtlwrapper)
	for target in targetHair:
		for mayaPlugin in findByName('pCube_lightLink_' + target + '*'):
			if mayaPlugin.type() == 'Node':
				wrapmtl = mayaPlugin.get('material')
				if wrapmtl.type() == 'MtlWrapper':
					#print 'MTLWRAPPER: ' + mayaPlugin.name()
					for m in findByName(target + 'vrsHair*'):
						if m.type() == 'Node':
							#print '		WRAPPING: ' + m.name()
							#hairmtl = m.get('material')
							#wrapmtl.set('base_material', hairmtl)
							m.set('material', wrapmtl)
					break
	# remove hair placeholder
	for mayaPlugin in findByName('pCube_lightLink_*'):
		delete(mayaPlugin)
	# adjust light linking
	litLinkingAdj(litLink_maya, geoPlaceholder, targetHair)

	print 'Done'