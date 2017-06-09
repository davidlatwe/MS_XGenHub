# -*- coding:utf-8 -*-
'''
Created on 2017.05.24

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
	col_opeh = cls.uiName + 'col_opeh'
	exp_opMenu = cls.uiName + 'exp_opMenu'
	ver_opMenu = cls.uiName + 'ver_opMenu'
	pal_opMenu = cls.uiName + 'pal_opMenu'
	des_opMenu = cls.uiName + 'des_opMenu'

	if pm.columnLayout(col_opeh, q= 1, ex= 1):
		pm.deleteUI(col_opeh)

	pm.columnLayout(col_opeh, p= cls.col_oper)

	# *********************************************
	# ROW ONE - chd num 2
	row1 = pm.rowLayout(nc= 2, adj= 1)
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
		pm.columnLayout(cal= 'left')
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

	# *********************************************
	# ROW TWO A - chd num 2
	descRow = pm.rowLayout(nc= 2, adj= 1, en= False)
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
	#pm.setParent('..')

	# *********************************************
	# ROW TWO B - chd num 2
	toolRow = pm.rowLayout(nc= 2, adj= 1, en= False)
	if toolRow:
		# CHD 0
		pm.columnLayout(cal= 'left')
		pm.text(l= '  * AnimWire Ready', h= 20)
		linkHairSysBtn = pm.button(l= 'Link Hair System', h= 19, w= 140)
		pm.setParent('..')
		# CHD 1
		pm.columnLayout(w= 104, cal= 'left')
		pm.text(l= '  * Anim Branch', h= 20)
		brn_optMenu = pm.optionMenu(w= 102)
		pm.setParent('..')
	pm.setParent('..')
	#pm.setParent('..')
	print 'AAA__ ' + cls.col_oper
	print 'PPP__ ' + col_opeh
	print 'RRR__ ' + pm.rowLayout(toolRow, q= 1, p= 1)

	pm.setParent('..')

	# COMMAND SET
	
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
		if cls.linked and os.listdir(cls.vsRepo):
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

	def snapshot_show(index, *args):
		"""doc"""
		imgPath = cls.snapNull
		if cls.linked and os.listdir(cls.vsRepo):
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
		print 'shitshit'
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

	def snapshot_take(index, *args):
		"""
		Take snapshots before export.
		"""
		oriPath = pm.image(cls.img_snap, q= 1, i= 1)
		tmpPath = cls.snapshotTmp % (index+1)
		if not os.path.isfile(tmpPath) or oriPath == tmpPath:
			if not os.path.exists(os.path.dirname(tmpPath)):
				os.mkdir(os.path.dirname(tmpPath))
			pm.refresh(cv= True, fe= cls.snapshotExt, fn= tmpPath)
			snapImg = mTex.MQImage(tmpPath)
			snapImg = mTex.resizeImage(snapImg, cls.snapSize, True)
			snapImg = mTex.extendImage(snapImg, cls.snapSize, cls.snapExtn)
			snapImg = mTex.paintTextWatermark(snapImg, str(index+1), [20, 40], [10, 10, 10, 255])
			snapImg.save(tmpPath)
			pm.button(cls.snapBtnn + str(index+1), e= 1, bgc= cls.snapTake)
		else:
			pm.button(cls.snapBtnn + str(index+1), e= 1, bgc= cls.snapShow)
		pm.image(cls.img_snap, e= 1, i= tmpPath)
		for i in range(5):
			if not i == index:
				pm.button(cls.snapBtnn + str(i+1), e= 1, bgc= cls.snapRest)

	#
	if switch:
		pm.rowLayout(descRow, e= 1, en= False, vis= False)
		pm.rowLayout(toolRow, e= 1, en= False, vis= True)

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

		pm.optionMenu(exp_opMenu, e= 1, cc= animToolEnable)
		pm.optionMenu(brn_optMenu, e= 1, cc= addAnimBranch)

		for i in range(5):
			pm.button(cls.snapBtnn + str(i+1), e= 1, en= 1, c= partial(snapshot_take, i),
				bgc= cls.snapRest)
	else:
		pm.rowLayout(descRow, e= 1, en= True, vis= True)
		pm.rowLayout(toolRow, e= 1, en= False, vis= False)

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


def initPanel(cls):
	"""doc"""
	exp_opMenu = cls.uiName + 'exp_opMenu'
	ver_opMenu = cls.uiName + 'ver_opMenu'
	pal_opMenu = cls.uiName + 'pal_opMenu'
	des_opMenu = cls.uiName + 'des_opMenu'

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