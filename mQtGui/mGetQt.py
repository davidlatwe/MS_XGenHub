from maya.OpenMayaUI import MQtUtil
from shiboken import wrapInstance
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore


def convert(mguiName):
	"""
	From the name of a Maya UI element of any type to pointer,
	and wrap the pointer into a python QObject
	:param mguiName: Maya UI Name
	:type mguiName: string
	:return: QWidget or subclass instance
	:rtype: QtGui.QWidget

	Thanks to Nathan Horne
	"""
	# Get pointer
	ptr = MQtUtil.findControl(mguiName)
	if ptr is None:
		ptr = MQtUtil.findLayout(mguiName)
	if ptr is None:
		ptr = MQtUtil.findMenuItem(mguiName)
	if ptr is None:
		return None
	# Find corresponding class
	qObj = wrapInstance(long(ptr), QtCore.QObject)
	metaObj = qObj.metaObject()
	cls = metaObj.className()
	superCls = metaObj.superClass().className()
	if hasattr(QtGui, cls):
		base = getattr(QtGui, cls)
	elif hasattr(QtGui, superCls):
		base = getattr(QtGui, superCls)
	else:
		base = QtGui.QWidget

	return wrapInstance(long(ptr), base)
