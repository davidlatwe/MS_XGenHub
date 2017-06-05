# -*- coding:utf-8 -*-
'''
Created on 2017.05.24

@author: davidpower
'''
import os
from functools import partial

import pymel.core as pm

import mQtGui; reload(mQtGui)
import mQtGui.muiSwitchBox as mqsb; reload(mqsb)
import mQtGui.mGetQt as mqt; reload(mqt)
import mMaya; reload(mMaya)
import mMaya.mTexture as mTex; reload(mTex)
import xgenHub; reload(xgenHub)


windowTitle = 'XGen Hub - v1.0 Alpha'
windowName = 'ms_xgenHub_mainUI'
column_main = windowName + '_main_column'
column_linkArea = windowName + '_linkArea_column'

windowWidth = 260
windowHeight = 300
snapshotSize = [252, 140]
snapshot_empty = os.path.dirname(__file__) + '/None.png'
snapshot_extnQ = [80, 80, 80, 255]
snapshot_showC = [.22, .46, .34]
snapshot_takeC = [.48, .25, .28]
snapshot_restC = [.36, .36, .36]


def ui_main():
	"""
	"""	
	if pm.window(windowName, q= 1, ex= 1):
		pm.deleteUI(windowName)
	
	msXGenHub = xgenHub.MsXGenHub()

	pm.window(windowName, t= windowTitle, s= 0, mxb= 0, mnb= 0)
	pm.columnLayout(column_main, adj= 1)

	bannerArea = pm.columnLayout(adj= 1, h= 40)
	bannerTxt = pm.text(l= 'XGen Hub')
	QBannerTxt = mqt.convert(bannerTxt)
	QBannerTxt.setStyleSheet('QObject {font: bold 26px; color: #222222;}')
	pm.setParent('..')
	pm.text(l= '', h= 4)
	pm.separator()
	pm.text(l= '', h= 2)
	pm.setParent('..')

	pm.columnLayout(column_linkArea, adj= 1, cal= 'left')
	pm.text(l= '  - XGenHub Repository Root', h= 22)
	pm.rowLayout(nc= 2, adj= 1)
	repoPath_textF = pm.textField(text= msXGenHub.projPath, ed= False)
	repoLink_icBtn = pm.iconTextButton(i= 'syncOn.png', w= 20, h= 20)
	pm.setParent('..')

	pm.columnLayout()
	pm.text(l= ' - Action Mode', h= 20)
	cmA= pm.columnLayout()
	mode_mqsb = mqsb.SwitchBox(onl= 'CHECK  IN', ofl= 'CHECK  OUT',
		w= windowWidth - 6, h= 35, onbg= [126, 121, 31], ofbg= [60, 124, 69], v= True, p= cmA)
	pm.setParent('..')
	pm.setParent('..')

	pm.text(l= '', h= 6)
	pm.separator()
	pm.text(l= '', h= 4)

	pm.rowLayout(nc= 2, adj= 1)
	
	pm.columnLayout(cal= 'left')
	pm.text(l= '  + Collection', h= 20)
	pal_optMenu = pm.optionMenu(w= 140)
	pm.setParent('..')

	holder_col = pm.columnLayout(w= 104, cal= 'left')
	pm.setParent('..')

	pm.setParent('..')

	descOptionZone = pm.rowLayout(nc= 2, adj= 1, en= False)

	pm.columnLayout(cal= 'left')
	pm.text(l= '  * Description', h= 20)
	des_optMenu = pm.optionMenu(w= 140)
	pm.setParent('..')

	pm.columnLayout(w= 104, cal= 'left')
	pm.text(l= '  * Content', h= 20)
	cnt_optMenu = pm.optionMenu(w= 102)
	pm.menuItem('description')
	pm.menuItem('groom only')
	pm.menuItem('guides only')
	pm.setParent('..')

	pm.setParent('..')

	pm.columnLayout(adj= 1, cal= 'center')
	pm.text(l= '  [ Snapshots ]  ', h= 20)
	pm.columnLayout(adj= 1, h= 142, cal= 'center')
	snapShot_pic = pm.image(i= snapshot_empty)
	pm.setParent('..')
	pm.text(l= '', h= 2)
	pm.rowLayout(nc= 5)
	for i in range(5):
		pm.button('xgenHub_snapShotBtn' + str(i+1), l= str(i+1), w= 49)
	pm.setParent('..')
	pm.setParent('..')

	pm.text(l= '', h= 4)
	pm.separator()
	pm.text(l= '', h= 2)

	pm.columnLayout(adj= 1)
	proc_btn = pm.button(l= 'P R O C E E D', h= 45, bgc= [0.25, 0.46, 0.49])
	pm.setParent('..')

	# COMMANDS AND FUNCTIONS

	ver_opMenu = windowName + 'ver_opMenu'
	exp_opMenu = windowName + 'exp_opMenu'
	ver_column = windowName + '_ver_column'
	exp_column = windowName + '_exp_column'
	def clearBoth():
		"""doc"""
		def snapshot_clear():
			"""doc"""
			for i in range(5):
				tmpPath = msXGenHub.snapshotTmp % (i+1)
				if os.path.isfile(tmpPath):
					os.remove(tmpPath)
		
		if pm.columnLayout(ver_column, q= 1, ex= 1):
			pm.deleteUI(ver_column)
		if pm.columnLayout(exp_column, q= 1, ex= 1):
			pm.deleteUI(exp_column)
		
		if pal_optMenu.getItemListLong():
			pal_optMenu.clear()
		if des_optMenu.getItemListLong():
			des_optMenu.clear()
		pm.menuItem('All descriptions', p= des_optMenu)
		
		pm.image(snapShot_pic, e= 1, i= snapshot_empty)
		snapshot_clear()

	def init_checkIn():
		"""doc"""
		pm.columnLayout(exp_column, cal= 'left', p= holder_col)
		pm.text(l= '  + Version', h= 20)
		pm.optionMenu(exp_opMenu, w= 100)
		pm.menuItem('BUMP')
		pm.menuItem('SAVE')
		pm.menuItem('BAKE')
		pm.setParent('..')
		pm.rowLayout(descOptionZone, e= 1, en= False)

		for pal in pm.ls(type= 'xgmPalette'):
			pm.menuItem(pal.name(), p= pal_optMenu)

		def snapshot_take(index, *args):
			"""
			Take snapshots before export.
			"""
			oriPath = pm.image(snapShot_pic, q= 1, i= 1)
			tmpPath = msXGenHub.snapshotTmp % (index+1)
			if not os.path.isfile(tmpPath) or oriPath == tmpPath:
				if not os.path.exists(os.path.dirname(tmpPath)):
					os.mkdir(os.path.dirname(tmpPath))
				pm.refresh(cv= True, fe= msXGenHub.snapshotExt, fn= tmpPath)
				snapImg = mTex.MQImage(tmpPath)
				snapImg = mTex.resizeImage(snapImg, snapshotSize, True)
				snapImg = mTex.extendImage(snapImg, snapshotSize, snapshot_extnQ)
				snapImg = mTex.paintTextWatermark(snapImg, str(index+1), [20, 40], [10, 10, 10, 255])
				snapImg.save(tmpPath)
				pm.button('xgenHub_snapShotBtn' + str(index+1), e= 1, bgc= snapshot_takeC)
			else:
				pm.button('xgenHub_snapShotBtn' + str(index+1), e= 1, bgc= snapshot_showC)
			pm.image(snapShot_pic, e= 1, i= tmpPath)
			for i in range(5):
				if not i == index:
					pm.button('xgenHub_snapShotBtn' + str(i+1), e= 1, bgc= snapshot_restC)

		for i in range(5):
			pm.button('xgenHub_snapShotBtn' + str(i+1), e= 1, en= 1, c= partial(snapshot_take, i),
				bgc= snapshot_restC)

	def init_checkOut():
		"""doc"""
		pm.columnLayout(ver_column, cal= 'left', p= holder_col)
		pm.text(l= '  = Version', h= 20)
		pm.optionMenu(ver_opMenu, w= 100)
		pm.setParent('..')
		pm.rowLayout(descOptionZone, e= 1, en= True)

		if msXGenHub.linked:
			palList = os.listdir(msXGenHub.vsRepo)
			for pal in palList:
				if os.path.isdir(os.path.join(msXGenHub.vsRepo, pal)):
					pm.menuItem(pal, p= pal_optMenu)
				
		def versionList():
			"""doc"""
			for item in pm.optionMenu(ver_opMenu, q= 1, ill= 1):
				pm.deleteUI(item)
			if msXGenHub.linked and os.listdir(msXGenHub.vsRepo):
				palPath = os.path.join(msXGenHub.vsRepo, pal_optMenu.getValue())
				verList = os.listdir(palPath)
				verList.reverse()
				for ver in verList:
					pm.menuItem(ver, p= ver_opMenu)

		def descriptionList():
			"""doc"""
			if des_optMenu.getItemListLong():
				des_optMenu.clear()
			pm.menuItem('All descriptions', p= des_optMenu)
			if msXGenHub.linked and os.listdir(msXGenHub.vsRepo):
				palName = pal_optMenu.getValue()
				version = pm.optionMenu(ver_opMenu, q= 1, v= 1)
				palVerPath = os.path.join(msXGenHub.vsRepo, palName, version)
				if msXGenHub.linked and os.path.isdir(palVerPath):
					for desc in os.listdir(palVerPath):
						if os.path.isdir(os.path.join(palVerPath, desc)) and not desc == '_snapshot_':
							pm.menuItem(desc, p= des_optMenu)
			else:
				pm.rowLayout(descOptionZone, e= 1, en= False)
				for i in range(5):
					pm.button('xgenHub_snapShotBtn' + str(i+1), e= 1, en= 0)

		def snapshot_show(index, *args):
			"""doc"""
			imgPath = snapshot_empty
			if msXGenHub.linked and os.listdir(msXGenHub.vsRepo):
				palName = pal_optMenu.getValue()
				version = pm.optionMenu(ver_opMenu, q= 1, v= 1)
				if palName and version:
					imgPath = msXGenHub.snapshotImgPath(palName, version, str(index+1))
					imgPath = imgPath if os.path.isfile(imgPath) else snapshot_empty
			pm.image(snapShot_pic, e= 1, i= imgPath)
			pm.button('xgenHub_snapShotBtn' + str(index+1), e= 1, bgc= snapshot_showC)
			for i in range(5):
				if not i == index:
					pm.button('xgenHub_snapShotBtn' + str(i+1), e= 1, bgc= snapshot_restC)
		
		for i in range(5):
			pm.button('xgenHub_snapShotBtn' + str(i+1), e= 1, c= partial(snapshot_show, i))
		
		def descAndVerAndSnapshot(*args):
			"""doc"""
			versionList()
			descriptionList()
			snapshot_show(0)
		pm.optionMenu(pal_optMenu, e= 1, cc= descAndVerAndSnapshot)

		def descAndSnapshot(*args):
			"""doc"""
			descriptionList()
			snapshot_show(0)
		pm.optionMenu(ver_opMenu, e= 1, cc= descAndSnapshot)

		# load version
		versionList()
		# load description
		descriptionList()
		# load snapshot
		snapshot_show(0)

	def actModeShift(mqsb):
		"""doc"""
		clearBoth()
		if mqsb.isChecked():
			init_checkIn()
		else:
			init_checkOut()
	mode_mqsb.toggleCmd = partial(actModeShift, mode_mqsb)

	def linkRepoDir(*args):
		"""doc"""
		result = pm.fileDialog2(cap= 'Select Server Project Folder', fm= 3, okc= 'Select', dir= pm.workspace(q= 1, rd= 1))
		if result:
			msXGenHub.initVersionRepo(result[0])
			pm.textField(repoPath_textF, e= 1, text= msXGenHub.projPath)
			# init option menus
			actModeShift(mode_mqsb)
	repoLink_icBtn.setCommand(partial(linkRepoDir))

	def process(mqsb, *args):
		"""doc"""
		if mqsb.isChecked():
			# export
			if not pal_optMenu.getNumberOfItems():
				pm.warning('[XGen Hub] : There are no collections in current scene.')
				return None
			palName = str(pal_optMenu.getValue())
			expMode = pm.optionMenu(exp_opMenu, q= 1, v= 1)
			newWork = True
			version = '000'
			bake = False
			palPath = os.path.join(msXGenHub.vsRepo, palName)
			if os.path.exists(palPath):
				verList = os.listdir(palPath)
				if verList:
					version = verList[-1][1:]
					newWork = False
			# check if get baked version, and we are not going to bake now
			if not version.isdigit() and not expMode == 'BAKE':
				# jump back to previous version
				version = verList[-2][1:]
				if not version.isdigit():
					# one palette should have one baked version only
					pm.error('[XGen Hub] : Version Repo Error.')
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
				version = 'vBaked'
			msXGenHub.exportFullPackage(palName, version, bake)
		else:
			# import
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
			palName = str(pal_optMenu.getValue())
			descName = str(des_optMenu.getValue())
			version = str(pm.optionMenu(ver_opMenu, q= 1, v= 1))
			bake = True if version == 'vBaked' else False
			if descName == 'All descriptions':
				if impType == 'description':
					msXGenHub.importPalette(palName, version, not bake)
				if impType == 'groom only':
					msXGenHub.importGrooming(palName, version= version)
				if impType == 'guides only':
					msXGenHub.importGuides(palName, version= version)
			else:
				if impType == 'description':
					msXGenHub.importDescription(palName, descName, version, not bake)
				if impType == 'groom only':
					msXGenHub.importGrooming(palName, descName, version)
				if impType == 'guides only':
					msXGenHub.importGuides(palName, descName, version)
	
	proc_btn.setCommand(partial(process, mode_mqsb))

	# SHOW WINDOW

	actModeShift(mode_mqsb)

	pm.window(windowName, e= 1, w= windowWidth, h= windowHeight)

	pm.showWindow(windowName)