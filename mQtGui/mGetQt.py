from maya.OpenMayaUI import MQtUtil
from ..vendor.Qt import QtCompat
from ..vendor.Qt import QtWidgets, QtCore


def convert(mguiName):
	"""
	From the name of a Maya UI element of any type to pointer,
	and wrap the pointer into a python QObject
	:param mguiName: Maya UI Name
	:type mguiName: string
	:return: QWidget or subclass instance
	:rtype: QtWidgets.QWidget

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
	qObj = QtCompat.wrapInstance(long(ptr), QtCore.QObject)
	metaObj = qObj.metaObject()
	cls = metaObj.className()
	superCls = metaObj.superClass().className()
	if hasattr(QtWidgets, cls):
		base = getattr(QtWidgets, cls)
	elif hasattr(QtWidgets, superCls):
		base = getattr(QtWidgets, superCls)
	else:
		base = QtWidgets.QWidget

	return QtCompat.wrapInstance(long(ptr), base)
