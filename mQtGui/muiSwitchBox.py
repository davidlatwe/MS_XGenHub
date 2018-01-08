from maya.OpenMayaUI import MQtUtil
from ..vendor.Qt import QtWidgets, QtCore, QtGui
import mGetQt as mqt; reload(mqt)

class SwitchBox(QtWidgets.QCheckBox):

	def __init__(self, *args, **kwargs):
		"""
		constructor
		"""
		QtWidgets.QCheckBox.__init__(self)
		''' DEFAULT '''
		# default size vars
		self.baseW = 100
		self.baseH = 22
		self.baseG = 2
		''' ARGS: SIZE '''
		# setting some size aspects
		self.w = kwargs['w'] if 'w' in kwargs else self.baseW
		self.h = kwargs['h'] if 'h' in kwargs else self.baseH
		''' ARGS: COLOR '''
		# switch color
		self.btnBG = kwargs['btnbg'] if 'btnbg' in kwargs else [150, 150, 150]
		self.onBG = kwargs['onbg'] if 'onbg' in kwargs else [55, 116, 116]
		self.offBG = kwargs['ofbg'] if 'ofbg' in kwargs else [148, 97, 79]
		''' ARGS: STATE '''
		# switch state text
		self.onLabel = kwargs['onl'] if 'onl' in kwargs else ''
		self.offLabel = kwargs['ofl'] if 'ofl' in kwargs else ''
		self.default = kwargs['v'] if 'v' in kwargs else False
		''' ARGS: BUTTON '''
		# turn to button like (no switch handle)
		self.likeBtn = kwargs['btn'] if 'btn' in kwargs else False
		''' ARGS: CMD '''
		# maya command to exec when state changed
		self.onCmd = kwargs['onc'] if 'onc' in kwargs else ''
		self.offCmd = kwargs['ofc'] if 'ofc' in kwargs else ''
		self.toggleCmd = kwargs['cc'] if 'cc' in kwargs else ''
		''' ARGS: PARENT '''
		# maya gui parent layout
		self.p = kwargs['p'] if 'p' in kwargs else ''
		self.fit = kwargs['fit'] if 'fit' in kwargs else True
		''' SET '''
		# setting w/h
		self.setMinimumWidth(self.w)
		self.setMaximumWidth(self.w)
		self.setMinimumHeight(self.h)
		self.setMaximumHeight(self.h)
		# set parent
		qtp = mqt.convert(self.p)
		self.setParent(qtp)
		if self.fit:
			qtp.setMinimumWidth(self.w)
			qtp.setMaximumWidth(self.w)
			qtp.setMinimumHeight(self.h)
			qtp.setMaximumHeight(self.h)
		if self.default:
			self.setChecked(True)


	def execCmd(self, cmd):
		"""
		exec <string> or <partial func>
		"""
		if str(type(cmd)) == "<type 'functools.partial'>":
			cmd()
		if str(type(cmd)) == "<type 'str'>":
			exec(cmd)


	def mousePressEvent(self, *args, **kwargs):
		"""
		override default and exec cmd
		"""
		# tick on and off set here
		if self.isChecked():
			''' RUN OFF CMD '''
			self.setChecked(False)
			if self.offCmd:
				self.execCmd(self.offCmd)
		else:
			''' RUN ON CMD '''
			self.setChecked(True)
			if self.onCmd:
				self.execCmd(self.onCmd)
		''' RUN TOGGLE CMD '''
		if self.toggleCmd:
			self.execCmd(self.toggleCmd)

		return QtWidgets.QCheckBox.mousePressEvent(self, *args, **kwargs)


	def paintEvent(self,event):
		"""
		override default style
		"""
		painter = QtGui.QPainter()
		painter.begin(self)
		# smooth curves
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		# keep default pen
		pen = painter.pen()
		# set to NoPen for no stroke(outline)
		painter.setPen(QtCore.Qt.NoPen)
		'''# set font
		font  = QtGui.QFont()
		font.setFamily("Courier New")
		font.setPixelSize(10)
		painter.setFont(font)'''
		# define some format rule
		btnW = self.w/2
		btnH = self.h
		btnG = self.baseG # int((self.h/self.baseH)*self.baseG)
		roun = 2
		if self.isEnabled():
			onBG = self.onBG
			offBG = self.offBG
			btnBG = self.btnBG
		else:
			onBG = [v * 0.7 for v in self.onBG]
			offBG = [v * 0.7 for v in self.offBG]
			btnBG = [v * 0.7 for v in self.btnBG]
		btnBG = QtGui.QColor(btnBG[0], btnBG[1], btnBG[2], 160)
		onBG = QtGui.QColor(onBG[0], onBG[1], onBG[2])
		offBG = QtGui.QColor(offBG[0], offBG[1], offBG[2])
		# change the look for on/off
		if self.isChecked():
			''' ON '''
			# background
			brush = QtGui.QBrush(onBG, style= QtCore.Qt.SolidPattern)
			painter.setBrush(brush)
			painter.drawRoundedRect(0, 0, self.width(), self.height(), roun, roun)
			# switch
			if not self.likeBtn:
				brush = QtGui.QBrush(btnBG, style= QtCore.Qt.SolidPattern)
				painter.setBrush(brush)
				painter.drawRoundedRect(btnW, btnG, btnW-btnG, btnH-(btnG*2), roun, roun)
			# label
			painter.setPen(pen)
			if not self.likeBtn:
				painter.drawText(btnG, btnG, btnW-btnG, btnH-(btnG*2), \
					QtCore.Qt.AlignCenter, self.onLabel)
			else:
				painter.drawText(btnG, btnG, self.w-btnG, btnH-(btnG*2), \
					QtCore.Qt.AlignCenter, self.onLabel)

		else:
			''' OFF '''
			# background
			brush = QtGui.QBrush(offBG, style= QtCore.Qt.SolidPattern)
			painter.setBrush(brush)
			painter.drawRoundedRect(0, 0, self.width(), self.height(), roun, roun)
			# switch
			if not self.likeBtn:
				brush = QtGui.QBrush(btnBG, style= QtCore.Qt.SolidPattern)
				painter.setBrush(brush)
				painter.drawRoundedRect(btnG, btnG, btnW-btnG, btnH-(btnG*2), roun, roun)
			# label
			painter.setPen(pen)
			if not self.likeBtn:
				painter.drawText(btnW, btnG, btnW-btnG, btnH-(btnG*2), \
					QtCore.Qt.AlignCenter, self.offLabel)
			else:
				painter.drawText(btnG, btnG, self.w-btnG, btnH-(btnG*2), \
					QtCore.Qt.AlignCenter, self.offLabel)

		painter.end()