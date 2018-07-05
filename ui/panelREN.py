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
		True  -> export
		False -> import
	"""
	global col_ope1
	global col_ope2
	global pal_opMenu
	global brn_opMenu
	global sht_opMenu

	col_ope1 = cls.uiName + 'col_ope1'
	col_ope2 = cls.uiName + 'col_ope2'

	pal_opMenu = cls.uiName + 'pal_opMenu'
	brn_opMenu = cls.uiName + 'brn_opMenu'
	sht_opMenu = cls.uiName + 'sht_opMenu'

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
			pass
		else:
			if cls.linked:
				palList = os.listdir(cls.vsRepo)
				for pal in palList:
					if os.path.isdir(os.path.join(cls.vsRepo, pal)):
						pm.menuItem(pal, p= pal_opMenu)
		pm.setParent('..')
		# CHD 1
		pm.columnLayout(cal= 'left')
		if switch:
			pass
		else:
			pm.text(l= '  + ANIM Branch', h= 20)
			brn_opMenu = pm.optionMenu(w= 100)
		pm.setParent('..')
	pm.setParent('..')
	
	pm.setParent('..')


	pm.columnLayout(col_ope2, p= cls.col_oper)

	# *********************************************
	# ROW TWO A - chd num 1
	shotRow = pm.rowLayout(nc= 1, vis= switch)
	if shotRow:
		# CHD 0
		pass
	pm.setParent('..')

	# *********************************************
	# ROW TWO B - chd num 1
	animRow = pm.rowLayout(nc= 1, vis= not switch)
	if animRow:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  = Shot List', h= 20)
		sht_opMenu = pm.optionMenu(w= 140)
		pm.setParent('..')
	pm.setParent('..')

	pm.setParent('..')


	# FUNCTION SET

	def animBranchList(*args):
		"""doc"""
		if brn_opMenu.getItemListLong():
			brn_opMenu.clear()
		if cls.linked and os.listdir(cls.vsRepo) and pal_opMenu.getItemListLong():
			palPath = os.path.join(cls.vsRepo, pal_opMenu.getValue())
			prefix = cls.dirAnim
			verList = []
			if os.path.exists(palPath):
				#verList = [d[len(prefix):-2] for d in os.listdir(palPath) if d.startswith(prefix)]
				verList = [d[len(prefix):] for d in os.listdir(palPath) if d.startswith(prefix)]
				verList = list(set(verList))
			for ver in verList:
				pm.menuItem(ver, p= brn_opMenu)

	def shotNameList(*args):
		"""doc"""
		if sht_opMenu.getItemListLong():
			sht_opMenu.clear()
		if cls.linked and os.listdir(cls.vsRepo) and brn_opMenu.getItemListLong():
			if os.path.exists(cls.getVRaySceneFileRepo()):
				palName = str(pal_opMenu.getValue())
				version = cls.dirAnim + str(brn_opMenu.getValue())
				shotDir = cls.paletteDeltaDir(palName, version, '')
				if os.path.exists(shotDir):
					shotList = os.listdir(shotDir)
					for shot in shotList:
						vrsdir = os.path.dirname(cls.getVRaySceneFilePath(palName, shot))
						if any(f.endswith(".vrscene") for f in os.listdir(vrsdir)):
							pm.menuItem(shot, p= sht_opMenu)

	def snapshot_show(index, *args):
		"""doc"""
		imgPath = cls.snapNull
		if cls.linked and os.listdir(cls.vsRepo) and pal_opMenu.getItemListLong():
			palName = pal_opMenu.getValue()
			version = ''
			shotName = ''
			if pm.optionMenu(brn_opMenu, q= 1, ill= 1):
				version = cls.dirAnim + pm.optionMenu(brn_opMenu, q= 1, v= 1)
			if pm.optionMenu(sht_opMenu, q= 1, ill= 1):
				shotName = sht_opMenu.getValue()
			if palName and version and shotName:
				imgPath = cls.snapshotImgPath(palName, version, str(index+1), shotName)
				imgPath = imgPath if os.path.isfile(imgPath) else cls.snapNull
		pm.image(cls.img_snap, e= 1, i= imgPath)
		pm.button(cls.snapBtnn + str(index+1), e= 1, bgc= cls.snapShow)
		for i in range(5):
			if not i == index:
				pm.button(cls.snapBtnn + str(i+1), e= 1, bgc= cls.snapRest)

	def process(mqsb, *args):
		"""doc"""
		if mqsb.isChecked():
			pass
		else:
			# grab script
			if not pal_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : There are no collections in repo.')
				return None
			if not brn_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : This collection has no animBranch in repo yet.')
				return None
			if not sht_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : This collection has no exported shot in repo yet.')
				return None

			palName = str(pal_opMenu.getValue())
			shotName = str(sht_opMenu.getValue())
			cls.connectVRayScene(palName, shotName)


	# MODIFY
	if switch:
		pass
	else:
		for i in range(5):
			pm.button(cls.snapBtnn + str(i+1), e= 1, c= partial(snapshot_show, i))

		def animBranchAndShotListAndSnapshot(*args):
			"""doc"""
			animBranchList();shotNameList();snapshot_show(0)
		pm.optionMenu(pal_opMenu, e= 1, cc= animBranchAndShotListAndSnapshot)

		def shotListAndSnapshot(*args):
			"""doc"""
			shotNameList();snapshot_show(0)
		pm.optionMenu(brn_opMenu, e= 1, cc= shotListAndSnapshot)

		pm.optionMenu(sht_opMenu, e= 1, cc= partial(snapshot_show, 0))

		# load
		animBranchAndShotListAndSnapshot()

	cls.proc_btn.setCommand(partial(process, cls.qsb_mode))


def initPanel(cls):
	"""doc"""
	global pal_opMenu
	global brn_opMenu

	if pm.optionMenu(pal_opMenu, q= 1, ex= 1):
		for item in pm.optionMenu(pal_opMenu, q= 1, ill= 1):
				pm.deleteUI(item)
	if pm.optionMenu(brn_opMenu, q= 1, ex= 1):
		for item in pm.optionMenu(brn_opMenu, q= 1, ill= 1):
				pm.deleteUI(item)

	pm.image(cls.img_snap, e= 1, i= cls.snapNull)
	cls.snapshot_clear()

	cls.makePanel(cls.qsb_mode.isChecked())