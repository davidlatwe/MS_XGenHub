# -*- coding:utf-8 -*-
'''
Created on 2017.06.09

@author: davidpower
'''
import os
from functools import partial
import pymel.core as pm



def makePanel(cls, switch):
	"""
	@switch:
		True  -> check in
		False -> check out
	"""
	global col_ope1
	global col_ope2
	global exp_opMenu
	global ver_opMenu
	global pal_opMenu
	global des_opMenu

	col_ope1 = cls.uiName + 'col_ope1'
	col_ope2 = cls.uiName + 'col_ope2'
	exp_opMenu = cls.uiName + 'exp_opMenu'
	ver_opMenu = cls.uiName + 'ver_opMenu'
	pal_opMenu = cls.uiName + 'pal_opMenu'
	des_opMenu = cls.uiName + 'des_opMenu'

	if pm.columnLayout(col_ope1, q= 1, ex= 1):
		pm.deleteUI(col_ope1)
	if pm.columnLayout(col_ope2, q= 1, ex= 1):
		pm.deleteUI(col_ope2)

	pm.columnLayout(col_ope1, p= cls.col_oper)

	# *********************************************
	# ROW ONE - chd num 2
	row1 = pm.rowLayout(nc= 2)
	if row1:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  + Collection', h= 20)
		pal_opMenu = pm.optionMenu(w= 140)
		if switch:
			for pal in pm.ls(type= 'xgmPalette'):
				pm.menuItem(pal.name(), p= pal_opMenu)
		else:
			if cls.linked:
				palList = os.listdir(cls.vsRepo)
				for pal in palList:
					if os.path.isdir(os.path.join(cls.vsRepo, pal)):
						pm.menuItem(pal, p= pal_opMenu)
		pm.setParent('..')
		# CHD 1
		pm.columnLayout(w= 104, cal= 'left')
		if switch:
			pm.text(l= '  + Version', h= 20)
			pm.optionMenu(exp_opMenu, w= 100)
			pm.menuItem('BUMP')
			pm.menuItem('SAVE')
			pm.menuItem('BAKE')
			pm.menuItem('ANIM')
			pm.setParent('..')
		else:
			pm.text(l= '  = Version', h= 20)
			ver_opMenu = pm.optionMenu(w= 100)
		pm.setParent('..')
	pm.setParent('..')
	
	pm.setParent('..')


	pm.columnLayout(col_ope2, p= cls.col_oper)

	# *********************************************
	# ROW TWO A - chd num 2
	descRow = pm.rowLayout(nc= 2, adj= 1, en= not switch, vis= not switch)
	if descRow:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  * Description', h= 20)
		des_opMenu = pm.optionMenu(w= 140)
		pm.setParent('..')
		# CHD 1
		pm.columnLayout(w= 104, cal= 'left')
		pm.text(l= '  * Content', h= 20)
		cnt_optMenu = pm.optionMenu(w= 102)
		pm.menuItem('description')
		pm.menuItem('groom only')
		pm.menuItem('guides only')
		pm.setParent('..')
	pm.setParent('..')

	# *********************************************
	# ROW TWO B - chd num 2
	toolRow = pm.rowLayout(nc= 2, adj= 1, en= False, vis= switch)
	if toolRow:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  * AnimWire Ready', h= 20)
		linkHairSysBtn = pm.button(l= 'Link Hair System', h= 19, w= 140)
		pm.setParent('..')
		# CHD 1
		pm.columnLayout(w= 104, cal= 'left')
		pm.text(l= '  * ANIM Branch', h= 20)
		brn_optMenu = pm.optionMenu(w= 102)
		pm.setParent('..')
	pm.setParent('..')

	pm.setParent('..')


	# FUNCTION SET
	
	def versionList():
		if ver_opMenu.getItemListLong():
			ver_opMenu.clear()
		if cls.linked and os.listdir(cls.vsRepo) and pal_opMenu.getItemListLong():
			palPath = os.path.join(cls.vsRepo, pal_opMenu.getValue())
			verList = [d for d in os.listdir(palPath) if not d.startswith(cls.dirAnim)]
			verList.reverse()
			for ver in verList:
				pm.menuItem(ver, p= ver_opMenu)

	def descriptionList():
		"""doc"""
		if des_opMenu.getItemListLong():
			des_opMenu.clear()
		pm.menuItem('All descriptions', p= des_opMenu)
		if cls.linked and os.listdir(cls.vsRepo) and pal_opMenu.getItemListLong() and ver_opMenu.getItemListLong():
			palName = pal_opMenu.getValue()
			version = pm.optionMenu(ver_opMenu, q= 1, v= 1)
			palVerPath = os.path.join(cls.vsRepo, palName, version)
			if cls.linked and os.path.isdir(palVerPath):
				for desc in os.listdir(palVerPath):
					if os.path.isdir(os.path.join(palVerPath, desc)) and not desc == '_snapshot_':
						pm.menuItem(desc, p= des_opMenu)
		else:
			pm.rowLayout(descRow, e= 1, en= False)
			for i in range(5):
				pm.button(cls.snapBtnn + str(i+1), e= 1, en= 0)

	def animBranchList(*args):
		"""doc"""
		if brn_optMenu.getItemListLong():
			brn_optMenu.clear()
		if cls.linked and os.listdir(cls.vsRepo) and pal_opMenu.getItemListLong():
			palPath = os.path.join(cls.vsRepo, pal_opMenu.getValue())
			prefix = cls.dirAnim
			verList = []
			if os.path.exists(palPath):
				#verList = [d[len(prefix):-2] for d in os.listdir(palPath) if d.startswith(prefix)]
				verList = [d[len(prefix):] for d in os.listdir(palPath) if d.startswith(prefix)]
				verList = list(set(verList))
			for ver in verList:
				pm.menuItem(ver, p= brn_optMenu)
			if verList:
				pm.menuItem('Add New..', p= brn_optMenu)
			else:
				pm.menuItem('BASE', p= brn_optMenu)

	def snapshot_show(index, *args):
		"""doc"""
		imgPath = cls.snapNull
		if cls.linked and os.listdir(cls.vsRepo) and pal_opMenu.getItemListLong() and ver_opMenu.getItemListLong():
			palName = pal_opMenu.getValue()
			version = pm.optionMenu(ver_opMenu, q= 1, v= 1)
			if palName and version:
				imgPath = cls.snapshotImgPath(palName, version, str(index+1))
				imgPath = imgPath if os.path.isfile(imgPath) else cls.snapNull
		pm.image(cls.img_snap, e= 1, i= imgPath)
		pm.button(cls.snapBtnn + str(index+1), e= 1, bgc= cls.snapShow)
		for i in range(5):
			if not i == index:
				pm.button(cls.snapBtnn + str(i+1), e= 1, bgc= cls.snapRest)

	def animToolEnable(*args):
		"""doc"""
		mode = pm.optionMenu(exp_opMenu, q= 1, v= 1)
		if mode == 'ANIM':
			pm.rowLayout(toolRow, e= 1, en= True, vis= True)
		else:
			pm.rowLayout(toolRow, e= 1, en= False, vis= True)

	def addAnimBranch(*args):
		"""doc"""
		if not brn_optMenu.getValue() == 'Add New..':
			return
		result = pm.promptDialog(title= "New Anim Branch", message= "Enter Name:",
			button= ["OK", "Cancel"], defaultButton= "OK", cancelButton= "Cancel",
			dismissString= "Cancel")
		if result == "OK":
			branch = pm.promptDialog(query= 1, text= 1)
			pm.menuItem(branch, ia= '', p= brn_optMenu)
			brn_optMenu.setValue(branch)

	def linkHairSys(*args):
		"""doc"""
		if pal_opMenu.getItemListLong():
			palName = str(pal_opMenu.getValue())
			cls.linkHairSystem(palName)
		else:
			pm.warning('[XGen Hub] : There is no collection in the scene.')

	def process(mqsb, *args):
		"""doc"""
		if mqsb.isChecked():
			# export
			if not pal_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : There are no collections in current scene.')
				return None
			palName = str(pal_opMenu.getValue())
			expMode = pm.optionMenu(exp_opMenu, q= 1, v= 1)
			newWork = True
			noBaked = True
			version = '000'
			verList = []
			bake = False
			anim = False
			
			palPath = os.path.join(cls.vsRepo, palName)
			if os.path.exists(palPath):
				verList = [d for d in os.listdir(palPath) if not d.startswith(cls.dirAnim)]
				if verList:
					version = verList[-1][1:]
					newWork = False
					noBaked = False if cls.dirBake in verList else True
			
			# get anim version
			if expMode == 'ANIM':
				#version = '00'
				dirAnimKeep = cls.dirAnim
				cls.dirAnim += str(brn_optMenu.getValue())
				#if os.path.exists(palPath):
				#	verList = [d for d in os.listdir(palPath) if d.startswith(cls.dirAnim)]
				#	if verList:
				#		version = verList[-1][len(cls.dirAnim):]

			# check if get baked version, and we are not going to bake now
			if not version.isdigit() and not expMode in ['BAKE', 'ANIM']:
				# jump back to previous version
				version = verList[-2][1:]
				if not version.isdigit():
					# one palette should have one baked version only
					pm.error('[XGen Hub] : Version Repo Error. Export Mode: [%s]' % expMode)

			# set version
			if expMode == 'BUMP':
				version = 'v%03d' % (int(version) + 1)
			if expMode == 'SAVE':
				version = 'v%03d' % (int(version) + 1 if newWork else 0)
			if expMode == 'BAKE':
				if newWork:
					pm.warning('[XGen Hub] : Should Not Bake with no version backup.')
					return None
				bake = True
				version = cls.dirBake
			if expMode == 'ANIM':
				if newWork:
					pm.warning('[XGen Hub] : Should Not go Anim with no version backup.')
					return None
				if noBaked:
					pm.warning('[XGen Hub] : Should Not go Anim without baked version.')
					return None
				anim = True
				#version = '%s%02d' % (cls.dirAnim, int(version) + 1)
				version = '%s' % (cls.dirAnim)
				cls.dirAnim = dirAnimKeep
			cls.exportFullPackage(palName, version, bake, anim)
		else:
			# import
			if not pal_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : There are no collections in repo.')
				return None
			# simple check if geo selected
			geoSelected = False
			if pm.ls(sl= 1):
				for dag in pm.ls(sl= 1):
					if dag.type() == 'transform':
						for shp in dag.getShapes():
							if shp.type() == 'mesh':
								geoSelected = True
								break
					if geoSelected:
						break
			if not geoSelected:
				pm.warning('[XGen Hub] : Please select a geometry.')
				return None
			impType = cnt_optMenu.getValue()
			palName = str(pal_opMenu.getValue())
			descName = str(des_opMenu.getValue())
			version = str(pm.optionMenu(ver_opMenu, q= 1, v= 1))
			bake = True if version == cls.dirBake else False
			if descName == 'All descriptions':
				if impType == 'description':
					cls.importPalette(palName, version, not bake)
				if impType == 'groom only':
					cls.importGrooming(palName, version= version)
				if impType == 'guides only':
					cls.importGuides(palName, version= version)
			else:
				if impType == 'description':
					cls.importDescription(palName, descName, version, not bake)
				if impType == 'groom only':
					cls.importGrooming(palName, descName, version)
				if impType == 'guides only':
					cls.importGuides(palName, descName, version)

	# MODIFY
	if switch:
		pm.optionMenu(pal_opMenu, e= 1, cc= animBranchList)
		pm.optionMenu(exp_opMenu, e= 1, cc= animToolEnable)
		pm.optionMenu(brn_optMenu, e= 1, cc= addAnimBranch)
		linkHairSysBtn.setCommand(linkHairSys)

		for i in range(5):
			pm.button(cls.snapBtnn + str(i+1), e= 1, en= 1, c= partial(cls.snapshot_take, i),
				bgc= cls.snapRest)

		animBranchList()
	else:
		for i in range(5):
			pm.button(cls.snapBtnn + str(i+1), e= 1, c= partial(snapshot_show, i))

		def descAndVerAndSnapshot(*args):
			"""doc"""
			versionList();descriptionList();snapshot_show(0)
		pm.optionMenu(pal_opMenu, e= 1, cc= descAndVerAndSnapshot)

		def descAndSnapshot(*args):
			"""doc"""
			descriptionList();snapshot_show(0)
		pm.optionMenu(ver_opMenu, e= 1, cc= descAndSnapshot)

		# load version
		versionList()
		# load description
		descriptionList()
		# load snapshot
		snapshot_show(0)

	cls.proc_btn.setCommand(partial(process, cls.qsb_mode))


def initPanel(cls):
	"""doc"""
	global exp_opMenu
	global ver_opMenu
	global pal_opMenu
	global des_opMenu

	if pm.columnLayout(ver_opMenu, q= 1, ex= 1):
		pm.deleteUI(ver_opMenu)
	if pm.columnLayout(exp_opMenu, q= 1, ex= 1):
		pm.deleteUI(exp_opMenu)

	if pm.optionMenu(pal_opMenu, q= 1, ex= 1):
		for item in pm.optionMenu(pal_opMenu, q= 1, ill= 1):
				pm.deleteUI(item)
	if pm.optionMenu(des_opMenu, q= 1, ex= 1):
		for item in pm.optionMenu(des_opMenu, q= 1, ill= 1):
				pm.deleteUI(item)
		pm.menuItem('All descriptions', p= des_opMenu)

	pm.image(cls.img_snap, e= 1, i= cls.snapNull)
	cls.snapshot_clear()

	cls.makePanel(cls.qsb_mode.isChecked())