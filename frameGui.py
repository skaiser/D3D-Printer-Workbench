# -*- coding: utf-8 -*-
# Author: Ruslan Krenzler.
# Date: 11 February 2018
# Create a pipe frame box.

import math
import os.path

from PySide import QtCore, QtGui
import FreeCAD

import D3DBase
from frame import *


class MainDialog(QtGui.QDialog):
	QSETTINGS_APPLICATION = "OSE D3D-Printer-Workbench"
	QSETTINGS_NAME = "frame user input"
	def __init__(self, document, pipeTable, cornerTable):
		super(MainDialog, self).__init__()
		self.document = document
		self.pipeTable = pipeTable
		self.cornerTable = cornerTable
		self.initUi()

	def initUi(self): 
		Dialog = self # Added 
		self.result = -1 
		self.setupUi(self)
		# Restore previous user input. Ignore exceptions to prevent this part
		# part of the code to prevent GUI from starting, once settings are broken.
		try:
			self.restoreInput()
		except Exception as e:
			print ("Could not restore old user input!")
			print(e)
		self.show()

# The following lines are from QtDesigner .ui-file processed by pyside-uic
# pyside-uic --indent=0 create-pipe.ui -o tmp.py
#
# The file paths needs to be adjusted manually. For example
# self.label.setPixmap(QtGui.QPixmap( GetMacroPath()+"/pipe-frame-box-dimensions.png"))
# access datata in some special FreeCAD directory.
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(614, 566)
		self.verticalLayout = QtGui.QVBoxLayout(Dialog)
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalWidget = QtGui.QWidget(Dialog)
		self.horizontalWidget.setMinimumSize(QtCore.QSize(0, 134))
		self.horizontalWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.horizontalWidget.setObjectName("horizontalWidget")
		self.checkBoxCreateSolid = QtGui.QCheckBox(self.horizontalWidget)
		self.checkBoxCreateSolid.setGeometry(QtCore.QRect(0, 0, 121, 26))
		self.checkBoxCreateSolid.setChecked(True)
		self.checkBoxCreateSolid.setObjectName("checkBoxCreateSolid")
		self.label_3 = QtGui.QLabel(self.horizontalWidget)
		self.label_3.setGeometry(QtCore.QRect(0, 30, 21, 25))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
		self.label_3.setSizePolicy(sizePolicy)
		self.label_3.setMaximumSize(QtCore.QSize(200, 16777215))
		self.label_3.setObjectName("label_3")
		self.lineEditLX = QtGui.QLineEdit(self.horizontalWidget)
		self.lineEditLX.setGeometry(QtCore.QRect(20, 30, 71, 27))
		self.lineEditLX.setObjectName("lineEditLX")
		self.label_5 = QtGui.QLabel(self.horizontalWidget)
		self.label_5.setGeometry(QtCore.QRect(110, 30, 21, 25))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
		self.label_5.setSizePolicy(sizePolicy)
		self.label_5.setMaximumSize(QtCore.QSize(200, 16777215))
		self.label_5.setObjectName("label_5")
		self.lineEditLY = QtGui.QLineEdit(self.horizontalWidget)
		self.lineEditLY.setGeometry(QtCore.QRect(130, 30, 71, 27))
		self.lineEditLY.setObjectName("lineEditLY")
		self.label_6 = QtGui.QLabel(self.horizontalWidget)
		self.label_6.setGeometry(QtCore.QRect(220, 30, 21, 25))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
		self.label_6.setSizePolicy(sizePolicy)
		self.label_6.setMaximumSize(QtCore.QSize(200, 16777215))
		self.label_6.setObjectName("label_6")
		self.lineEditLZ = QtGui.QLineEdit(self.horizontalWidget)
		self.lineEditLZ.setGeometry(QtCore.QRect(240, 30, 71, 27))
		self.lineEditLZ.setObjectName("lineEditLZ")
		self.label_2 = QtGui.QLabel(self.horizontalWidget)
		self.label_2.setGeometry(QtCore.QRect(0, 70, 91, 17))
		self.label_2.setObjectName("label_2")
		self.lineEditPipeName = QtGui.QLineEdit(self.horizontalWidget)
		self.lineEditPipeName.setGeometry(QtCore.QRect(80, 70, 171, 27))
		self.lineEditPipeName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
		self.lineEditPipeName.setObjectName("lineEditPipeName")
		self.pushButtonSelectPipe = QtGui.QPushButton(self.horizontalWidget)
		self.pushButtonSelectPipe.setEnabled(False)
		self.pushButtonSelectPipe.setGeometry(QtCore.QRect(260, 70, 121, 27))
		self.pushButtonSelectPipe.setObjectName("pushButtonSelectPipe")
		self.pushButtonSelectCorner = QtGui.QPushButton(self.horizontalWidget)
		self.pushButtonSelectCorner.setEnabled(False)
		self.pushButtonSelectCorner.setGeometry(QtCore.QRect(260, 100, 121, 27))
		self.pushButtonSelectCorner.setObjectName("pushButtonSelectCorner")
		self.lineEditCornerName = QtGui.QLineEdit(self.horizontalWidget)
		self.lineEditCornerName.setGeometry(QtCore.QRect(80, 100, 171, 27))
		self.lineEditCornerName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
		self.lineEditCornerName.setObjectName("lineEditCornerName")
		self.label_7 = QtGui.QLabel(self.horizontalWidget)
		self.label_7.setGeometry(QtCore.QRect(0, 100, 91, 17))
		self.label_7.setObjectName("label_7")
		self.verticalLayout.addWidget(self.horizontalWidget)
		self.label = QtGui.QLabel(Dialog)
		self.label.setText("")
		self.label.setPixmap(QtGui.QPixmap(os.path.join(D3DBase.IMAGE_PATH, "/pipe-frame-box-dimensions.png")))
		print("")
		print(os.path.join(D3DBase.IMAGE_PATH, "/pipe-frame-box-dimensions.png"))
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName("label")
		self.verticalLayout.addWidget(self.label)
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.verticalLayout.addWidget(self.buttonBox)

		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Create frame box", None, QtGui.QApplication.UnicodeUTF8))
		self.checkBoxCreateSolid.setText(QtGui.QApplication.translate("Dialog", "Create Solid", None, QtGui.QApplication.UnicodeUTF8))
		self.label_3.setText(QtGui.QApplication.translate("Dialog", "LX:", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEditLX.setText(QtGui.QApplication.translate("Dialog", "12 in", None, QtGui.QApplication.UnicodeUTF8))
		self.label_5.setText(QtGui.QApplication.translate("Dialog", "LY:", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEditLY.setText(QtGui.QApplication.translate("Dialog", "8 in", None, QtGui.QApplication.UnicodeUTF8))
		self.label_6.setText(QtGui.QApplication.translate("Dialog", "LZ:", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEditLZ.setText(QtGui.QApplication.translate("Dialog", "4 in", None, QtGui.QApplication.UnicodeUTF8))
		self.label_2.setText(QtGui.QApplication.translate("Dialog", "Pipe name:", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEditPipeName.setText(QtGui.QApplication.translate("Dialog", "NPS 1 in PVC SCH 40", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButtonSelectPipe.setText(QtGui.QApplication.translate("Dialog", "Select Pipe", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButtonSelectCorner.setText(QtGui.QApplication.translate("Dialog", "Select Corner", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEditCornerName.setText(QtGui.QApplication.translate("Dialog", "F0013WE", None, QtGui.QApplication.UnicodeUTF8))
		self.label_7.setText(QtGui.QApplication.translate("Dialog", "Pipe name:", None, QtGui.QApplication.UnicodeUTF8))

	def accept(self):
		"""User clicked OK"""
		# If there is no active document, show a warning message and exit dialog.
		if self.document is None:
			text = "I have not found any active document were I can create a corner fitting.\n"\
				"Use menu File->New to create a new document first, "\
				"then try to create the corner fitting again."
			msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Creating of the corner fitting failed.", text)
			msgBox.exec_()
			super(MainDialog, self).accept()
			return

		# Update active document.  If there is none, show a warning message and do nothing.
		# Get dimensions from the table
		box = BoxFromTable(self.document, self.pipeTable, self.cornerTable)
		box.LX = tu(self.lineEditLX.text())
		if box.LX == "":
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Set LX length.")
			msgBox.exec_()
			return
		box.LY = tu(self.lineEditLY.text())
		if box.LY == "":
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Set LY length.")
			msgBox.exec_()
			return
		box.LZ = tu(self.lineEditLZ.text())
		if box.LZ == "":
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Set LZ length.")
			msgBox.exec_()
			return
	
		pipeName = self.lineEditPipeName.text()
		if pipeName == "":
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Enter pipe name.")
			msgBox.exec_()
			return
		cornerName = self.lineEditCornerName.text()
		if cornerName == "":
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Enter corner name.")
			msgBox.exec_()
			return

		createSolid = self.checkBoxCreateSolid.isChecked()
		box.create(pipeName, cornerName, createSolid)
		self.document.recompute()
		# Save user input for the next dialog call.
		self.saveInput()
		# Call parent class.
		super(MainDialog, self).accept()


	def saveInput(self):
		"""Store user input for the next run."""
		settings = QtCore.QSettings(MainDialog.QSETTINGS_APPLICATION, MainDialog.QSETTINGS_NAME)
		check = self.checkBoxCreateSolid.checkState()
		settings.setValue("checkBoxCreateSolid", int(check))
		settings.setValue("lineEditLX", self.lineEditLX.text())
		settings.setValue("lineEditLY", self.lineEditLY.text())
		settings.setValue("lineEditLZ", self.lineEditLZ.text())
		settings.setValue("lineEditPipeName", self.lineEditPipeName.text())
		settings.setValue("lineEditCornerName", self.lineEditCornerName.text())
		settings.sync()

	def restoreInput(self):
		settings = QtCore.QSettings(MainDialog.QSETTINGS_APPLICATION, MainDialog.QSETTINGS_NAME)
		checkState = QtCore.Qt.CheckState(int(settings.value("checkBoxCreateSolid")))
		self.checkBoxCreateSolid.setCheckState(checkState)
		text = settings.value("lineEditLX")
		if text is not None:
			self.lineEditLX.setText(text)
		text = settings.value("lineEditLY")
		if text is not None:
			self.lineEditLY.setText(text)
		text = settings.value("lineEditLZ")
		if text is not None:
			self.lineEditLZ.setText(text)
		text = settings.value("lineEditPipeName")
		if text is not None:
			self.lineEditPipeName.setText(text)
		text = settings.value("lineEditCornerName")
		if text is not None:
			self.lineEditCornerName.setText(text)





