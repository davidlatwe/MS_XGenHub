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

import ui;reload(ui)
import ui.panelMOD as panelMOD; reload(panelMOD)


__version__ = xgenHub.__version__
__uititle__ = 'XGen Hub - v%s' % __version__


class MsXGenHubUI(xgenHub.MsXGenHub):
	"""doc"""
	def __init__(self):
		"""doc"""
		xgenHub.MsXGenHub.__init__(self)
		# main window
		self.uiName = 'ms_xgenHub_mainUI'
		self.uiWidth = 261
		self.uiHeight = 504
		# UI MODE
		self.MODE = 'MOD'
		self.DEFAULT = {'MOD': True}
		# snapshot things
		self.snapSize = [252, 140]
		self.snapNull = os.path.dirname(__file__) + '/None.png'
		self.snapExtn = [80, 80, 80, 255]
		self.snapShow = [.22, .46, .34]
		self.snapTake = [.48, .25, .28]
		self.snapRest = [.36, .36, .36]
		self.snapBtnn = 'xgenHub_snapShotBtn_UIprefix'
		# ui placeholder, will be fit in later
		self.col_main = 'main columnLayout'
		self.col_acts = 'action switch columnLayout'
		self.col_acth = 'hold action switch columnLayout'
		self.qsb_mode = 'action switch'
		self.col_oper = 'operation panel columnLayout'
		self.txf_repo = 'repo path textfield'
		self.btn_link = 'repo link button'
		self.img_snap = 'snapshot image'
		self.proc_btn = 'final execute button'


	def linkRepoDir(self):
		"""doc"""
		result = pm.fileDialog2(cap= 'Select Server Project Folder',
			fm= 3, okc= 'Select', dir= pm.workspace(q= 1, rd= 1))
		if result:
			self.initVersionRepo(result[0])
			pm.textField(self.txf_repo, e= 1, text= self.projPath)
			# init option menus
			self.initPanel()


	def actionSwitch(self, onLabel, offLabel, onColor, offColor, default):
		"""doc"""
		if pm.columnLayout(self.col_acth, q= 1, ex= 1):
			pm.deleteUI(self.col_acth)

		self.col_acth = pm.columnLayout(p= self.col_acts)
		pm.text(l= ' - Action Mode', h= 20)
		cmA= pm.columnLayout()
		self.qsb_mode = mqsb.SwitchBox(onl= onLabel, ofl= offLabel,
			w= self.uiWidth - 6, h= 35, onbg= onColor, ofbg= offColor, v= default, p= cmA)
		pm.setParent('..')


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
			
		self.makePanel(self.qsb_mode.isChecked())


	def initMode(self):
		"""doc"""
		if self.MODE == 'MOD':
			self.actionSwitch('CHECK  IN', 'CHECK  OUT',
							[126, 121, 31], [60, 124, 69], self.DEFAULT[self.MODE])
		self.initAction()
		self.qsb_mode.toggleCmd = partial(self.initPanel)


	def showUI(self):
		"""doc"""
		
		if pm.window(self.uiName, q= 1, ex= 1):
			pm.deleteUI(self.uiName)

		# make window
		pm.window(self.uiName, t= __uititle__, s= 0, mxb= 0, mnb= 0)
		# main column
		self.col_main = pm.columnLayout(adj= 1)

		# top banner
		pm.columnLayout(adj= 1, h= 40)
		bannerTxt = pm.text(l= 'XGen Hub')
		QBannerTxt = mqt.convert(bannerTxt)
		QBannerTxt.setStyleSheet('QObject {font: bold 26px; color: #222222;}')
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
		self.img_snap = pm.image(i= snapshot_empty)
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


if __name__ == '__main__':
	pass