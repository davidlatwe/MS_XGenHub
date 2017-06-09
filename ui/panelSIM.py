# -*- coding:utf-8 -*-
'''
Created on 2017.06.09

@author: davidpower
'''
import os
from functools import partial
import pymel.core as pm

from .. import mMaya as mMaya; reload(mMaya)
from ..mMaya import mTexture as mTex; reload(mTex)



def makePanel(cls, switch):
	"""
	@switch:
		True  -> check in
		False -> check out
	"""
	global col_ope1
	global col_ope2
	global pal_opMenu
	global brn_opMenu

	col_ope1 = cls.uiName + 'col_ope1'
	col_ope2 = cls.uiName + 'col_ope2'

	pal_opMenu = cls.uiName + 'pal_opMenu'
	brn_opMenu = cls.uiName + 'brn_opMenu'

	if pm.columnLayout(col_ope1, q= 1, ex= 1):
		pm.deleteUI(col_ope1)
	if pm.columnLayout(col_ope2, q= 1, ex= 1):
		pm.deleteUI(col_ope2)

	pm.columnLayout(col_ope1, p= cls.col_oper)

	# *********************************************
	# ROW ONE - chd num 1
	row1 = pm.rowLayout(nc= 1)
	if row1:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  + Collection', h= 20)
		pal_opMenu = pm.optionMenu(w= 200)
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
	pm.setParent('..')
	
	pm.setParent('..')


	pm.columnLayout(col_ope2, p= cls.col_oper)

	# *********************************************
	# ROW TWO A - chd num 1
	shotRow = pm.rowLayout(nc= 1, vis= switch)
	if shotRow:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  * Shot Name', h= 20)
		txt_shot = pm.textField(w= 200)
		pm.setParent('..')
	pm.setParent('..')

	# *********************************************
	# ROW TWO B - chd num 1
	animRow = pm.rowLayout(nc= 1, vis= not switch)
	if animRow:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  * Anim Branch', h= 20)
		brn_opMenu = pm.optionMenu(w= 200)
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

	def snapshot_show(index, *args):
		"""doc"""
		imgPath = cls.snapNull
		if cls.linked and os.listdir(cls.vsRepo) and pal_opMenu.getItemListLong():
			palName = pal_opMenu.getValue()
			version = ''
			if pm.optionMenu(brn_opMenu, q= 1, ill= 1):
				version = cls.dirAnim + pm.optionMenu(brn_opMenu, q= 1, v= 1)
			if palName and version:
				imgPath = cls.snapshotImgPath(palName, version, str(index+1))
				imgPath = imgPath if os.path.isfile(imgPath) else cls.snapNull
		pm.image(cls.img_snap, e= 1, i= imgPath)
		pm.button(cls.snapBtnn + str(index+1), e= 1, bgc= cls.snapShow)
		for i in range(5):
			if not i == index:
				pm.button(cls.snapBtnn + str(i+1), e= 1, bgc= cls.snapRest)

	def process(mqsb, *args):
		"""doc"""
		if mqsb.isChecked():
			# export
			if not pal_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : There are no collections in current scene.')
				return None
			if not pm.textField(txt_shot, q= 1, text= 1):
				pm.warning('[XGen Hub] : No shotName given.')
				return None
			palName = str(pal_opMenu.getValue())
			shotName = str(pm.textField(txt_shot, q= 1, text= 1))

			cls.exportAnimPackage(palName, shotName)
		else:
			# import
			if not pal_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : There are no collections in repo.')
				return None
			if not brn_opMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : This collection has no animBranch in repo yet.')
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

			palName = str(pal_opMenu.getValue())
			version = cls.dirAnim + str(brn_opMenu.getValue())
			cls.importPalette(palName, version, False, True, True)


	# MODIFY
	if switch:
		for i in range(5):
			pm.button(cls.snapBtnn + str(i+1), e= 1, en= 1, c= partial(cls.snapshot_take, i),
				bgc= cls.snapRest)

		pm.optionMenu(pal_opMenu, e= 1, cc= '')
	else:
		for i in range(5):
			pm.button(cls.snapBtnn + str(i+1), e= 1, c= partial(snapshot_show, i))

		def animBranchAndSnapshot(*args):
			"""doc"""
			animBranchList();snapshot_show(0)
		pm.optionMenu(pal_opMenu, e= 1, cc= animBranchAndSnapshot)

		pm.optionMenu(brn_opMenu, e= 1, cc= partial(snapshot_show, 0))

		# load
		animBranchAndSnapshot()

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