# -*- coding:utf-8 -*-
'''
Created on 2017.05.24

@author: davidpower
'''
import os
import json
from functools import partial

import pymel.core as pm

import mQtGui; reload(mQtGui)
import mQtGui.muiSwitchBox as mqsb; reload(mqsb)
import mQtGui.mGetQt as mqt; reload(mqt)

import xgenHub; reload(xgenHub)

import mMaya as mMaya; reload(mMaya)
import mMaya.mTexture as mTex; reload(mTex)

import ui;reload(ui)
import ui.panelMOD as panelMOD; reload(panelMOD)
import ui.panelSIM as panelSIM; reload(panelSIM)
import ui.panelVRS as panelVRS; reload(panelVRS)
import ui.panelREN as panelREN; reload(panelREN)


__version__ = xgenHub.__version__
__uititle__ = 'XGen Hub - v%s' % __version__


class MsXGenHubUI(xgenHub.MsXGenHub):
	"""doc"""
	def __init__(self):
		"""doc"""
		xgenHub.MsXGenHub.__init__(self)
		# user settings
		self.settings = '/'.join([os.environ.get('MAYA_APP_DIR'), 'xgenHub_lastStatus.json'])
		# main window
		self.uiName = 'ms_xgenHub_mainUI'
		self.uiWidth = 261
		self.uiHeight = 524
		# UI MODE
		self.MODE = self.loadLastStatus()
		self.MODELIST = ['MOD', 'SIM', 'VRS', 'REN']
		self.MODEDICT = {'MOD': False, 'SIM': False, 'VRS': False, 'REN': False}
		# snapshot things
		self.snapSize = [252, 140]
		self.snapNull = os.path.dirname(__file__) + '/None.png'
		self.snapExtn = [80, 80, 80, 255]
		self.snapShow = [.22, .46, .34]
		self.snapTake = [.48, .25, .28]
		self.snapRest = [.36, .36, .36]
		self.snapBtnn = 'xgenHub_snapShotBtn_UIprefix'
		# ui placeholder, will be fit in later
		self.txt_ban1 = 'banner text main'
		self.txt_ban2 = 'banner text sub'
		self.btn_prev = 'previous mode button'
		self.btn_next = 'next mode button'
		self.col_main = 'main columnLayout'
		self.col_acts = 'action switch columnLayout'
		self.col_acth = 'hold action switch columnLayout'
		self.qsb_mode = 'action switch'
		self.col_oper = 'operation panel columnLayout'
		self.txf_repo = 'repo path textfield'
		self.btn_link = 'repo link button'
		self.img_snap = 'snapshot image'
		self.proc_btn = 'final execute button'


	def loadLastStatus(self, *args):
		"""doc"""
		if os.path.isfile(self.settings):
			with open(self.settings) as jsonSet:
				return json.load(jsonSet)['MODE']
		else:
			return 'SIM'


	def saveLastStatus(self, *args):
		"""doc"""
		with open(self.settings, 'w') as jsonSet:
			json.dump({'MODE': self.MODE}, jsonSet, indent=4)


	def linkRepoDir(self):
		"""doc"""
		result = pm.fileDialog2(cap= 'Select Server Project Folder',
			fm= 3, okc= 'Select', dir= pm.workspace(q= 1, rd= 1))
		if result:
			self.initVersionRepo(result[0])
			pm.textField(self.txf_repo, e= 1, text= self.projPath)
			# init option menus
			self.initPanel()


	def actionSwitch(self, onLabel, offLabel, onColor, offColor, default, btnLike= False):
		"""doc"""
		if pm.columnLayout(self.col_acth, q= 1, ex= 1):
			pm.deleteUI(self.col_acth)

		self.col_acth = pm.columnLayout(p= self.col_acts)
		pm.text(l= ' - Action Mode', h= 20)
		cmA= pm.columnLayout()
		self.qsb_mode = mqsb.SwitchBox(onl= onLabel, ofl= offLabel, btn= btnLike,
			w= self.uiWidth - 6, h= 35, onbg= onColor, ofbg= offColor, v= default, p= cmA)
		pm.setParent('..')


	def snapshot_take(self, index, *args):
		"""
		Take snapshots before export.
		"""
		oriPath = pm.image(self.img_snap, q= 1, i= 1)
		tmpPath = self.snapshotTmp % (index+1)
		if not os.path.isfile(tmpPath) or oriPath == tmpPath:
			if not os.path.exists(os.path.dirname(tmpPath)):
				os.mkdir(os.path.dirname(tmpPath))
			pm.refresh(cv= True, fe= self.snapshotExt, fn= tmpPath)
			snapImg = mTex.MQImage(tmpPath)
			snapImg = mTex.resizeImage(snapImg, self.snapSize, True)
			snapImg = mTex.extendImage(snapImg, self.snapSize, self.snapExtn)
			snapImg = mTex.paintTextWatermark(snapImg, str(index+1), [20, 40], [10, 10, 10, 255])
			snapImg.save(tmpPath)
			pm.button(self.snapBtnn + str(index+1), e= 1, bgc= self.snapTake)
		else:
			pm.button(self.snapBtnn + str(index+1), e= 1, bgc= self.snapShow)
		pm.image(self.img_snap, e= 1, i= tmpPath)
		for i in range(5):
			if not i == index:
				pm.button(self.snapBtnn + str(i+1), e= 1, bgc= self.snapRest)


	def snapshot_clear(self):
		"""doc"""
		for i in range(5):
			tmpPath = self.snapshotTmp % (i+1)
			if os.path.isfile(tmpPath):
				os.remove(tmpPath)


	def initAction(self):
		"""doc"""
		if self.MODE == 'MOD':
			self.makePanel = self.MODmakePanel
			self.initPanel = self.MODinitPanel
		if self.MODE == 'SIM':
			self.makePanel = self.SIMmakePanel
			self.initPanel = self.SIMinitPanel
		if self.MODE == 'VRS':
			self.makePanel = self.VRSmakePanel
			self.initPanel = self.VRSinitPanel
		if self.MODE == 'REN':
			self.makePanel = self.RENmakePanel
			self.initPanel = self.RENinitPanel
			
		self.makePanel(self.qsb_mode.isChecked())


	def initMode(self):
		"""doc"""
		pm.text(self.txt_ban2, e= 1, l= self.MODE)
		if self.MODE == 'MOD':
			self.actionSwitch('CHECK  IN', 'CHECK  OUT',
							[106, 128, 31], [75, 115, 59], self.MODEDICT[self.MODE])
		if self.MODE == 'SIM':
			self.actionSwitch('EXPORT', 'IMPORT',
							[121, 82, 48], [124, 70, 59], self.MODEDICT[self.MODE])
		if self.MODE == 'VRS':
			self.actionSwitch('EXPORT', 'IMPORT',
							[35, 90, 121], [50, 70, 124], self.MODEDICT[self.MODE])
		if self.MODE == 'REN':
			self.actionSwitch('', 'GRAB  VRAY  SCRIPT',
							[190, 70, 80], [190, 70, 80], self.MODEDICT[self.MODE], True)
			self.qsb_mode.setEnabled(False)
		self.initAction()
		self.qsb_mode.toggleCmd = partial(self.initPanel)


	def switchMode(self, nextMode, *args):
		"""doc"""
		current = self.MODELIST.index(self.MODE)
		if nextMode:
			self.MODE = self.MODELIST[(current + 1) % len(self.MODELIST)]
		else:
			self.MODE = self.MODELIST[(current - 1) % len(self.MODELIST)]
		self.initMode()
		self.initPanel()


	def showUI(self):
		"""doc"""
		
		if pm.window(self.uiName, q= 1, ex= 1):
			pm.deleteUI(self.uiName)

		# make window
		pm.window(self.uiName, t= __uititle__, s= 0, mxb= 0, mnb= 0, cc= self.saveLastStatus)
		# main column
		self.col_main = pm.columnLayout(adj= 1)

		# top banner
		# main
		pm.columnLayout(adj= 1, bgc= [.22,.22,.22])
		pm.text(l= '', h= 3)
		self.txt_ban1 = pm.text(l= 'XGen Hub')
		QBannerTxt1 = mqt.convert(self.txt_ban1)
		QBannerTxt1.setStyleSheet('QObject {font: bold 12px; color: #121212;}')
		pm.text(l= '', h= 3)
		pm.setParent('..')
		# sub
		pm.rowLayout(nc= 5, adj= 3)
		pm.text(l= '', w= 8)
		self.btn_prev = pm.iconTextButton(i= 'SP_FileDialogBack_Disabled.png',
			c= partial(self.switchMode, False))		
		pm.columnLayout(adj= 1, h= 33)
		self.txt_ban2 = pm.text(l= self.MODE)
		QBannerTxt2 = mqt.convert(self.txt_ban2)
		QBannerTxt2.setStyleSheet('QObject {font: bold 22px; color: #666666;}')
		pm.setParent('..')
		self.btn_next = pm.iconTextButton(i= 'SP_FileDialogForward_Disabled.png',
			c= partial(self.switchMode, True))
		pm.text(l= '', w= 8)
		pm.setParent('..')
		
		# ----------
		pm.text(l= '', h= 4);pm.separator();pm.text(l= '', h= 2)
		
		# XGenHub Repository Root
		pm.columnLayout(adj= 1, cal= 'left')
		pm.text(l= '  - XGenHub Repository Root', h= 22)
		pm.rowLayout(nc= 2, adj= 1)
		self.txf_repo = pm.textField(text= self.projPath, ed= False)
		self.btn_link = pm.iconTextButton(i= 'syncOn.png', w= 20, h= 20, c= self.linkRepoDir)
		pm.setParent('..')

		# Action Mode
		self.col_acts = pm.columnLayout(w= 257, h= 57)
		pm.setParent('..')
		
		# ----------
		pm.text(l= '', h= 6);pm.separator();pm.text(l= '', h= 4)

		# operation panel
		self.col_oper = pm.columnLayout(w= 257, h= 92)
		pm.setParent('..')

		# snapshot panel
		pm.columnLayout(adj= 1, cal= 'center')
		pm.text(l= '  [ Snapshots ]  ', h= 20)
		pm.columnLayout(adj= 1, h= 142, cal= 'center')
		self.img_snap = pm.image(i= self.snapNull)
		pm.setParent('..')
		pm.text(l= '', h= 2)
		pm.rowLayout(nc= 5)
		for i in range(5):
			pm.button(self.snapBtnn + str(i+1), l= str(i+1), w= 49)
		pm.setParent('..')
		pm.setParent('..')
		pm.setParent('..')

		# ----------
		pm.text(l= '', h= 4);pm.separator();pm.text(l= '', h= 2)

		# execute button
		pm.columnLayout(adj= 1)
		self.proc_btn = pm.button(l= 'P R O C E E D', h= 45, bgc= [0.25, 0.46, 0.49])
		pm.setParent('..')

		# main column END
		pm.setParent('..')

		self.initMode()

		pm.window(self.uiName, e= 1, w= self.uiWidth, h= self.uiHeight)
		pm.showWindow(self.uiName)


MsXGenHubUI.MODmakePanel = panelMOD.makePanel
MsXGenHubUI.MODinitPanel = panelMOD.initPanel

MsXGenHubUI.SIMmakePanel = panelSIM.makePanel
MsXGenHubUI.SIMinitPanel = panelSIM.initPanel

MsXGenHubUI.VRSmakePanel = panelVRS.makePanel
MsXGenHubUI.VRSinitPanel = panelVRS.initPanel

MsXGenHubUI.RENmakePanel = panelREN.makePanel
MsXGenHubUI.RENinitPanel = panelREN.initPanel

if __name__ == '__main__':
	pass
