# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/add_footnote_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddFootnoteDialog(object):
    def setupUi(self, AddFootnoteDialog):
        AddFootnoteDialog.setObjectName("AddFootnoteDialog")
        AddFootnoteDialog.resize(400, 300)
        AddFootnoteDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddFootnoteDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AutogenIdentifierCheckbox = QtWidgets.QCheckBox(AddFootnoteDialog)
        self.AutogenIdentifierCheckbox.setChecked(True)
        self.AutogenIdentifierCheckbox.setObjectName("AutogenIdentifierCheckbox")
        self.verticalLayout.addWidget(self.AutogenIdentifierCheckbox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.IdentifierLabel = QtWidgets.QLabel(AddFootnoteDialog)
        self.IdentifierLabel.setObjectName("IdentifierLabel")
        self.horizontalLayout.addWidget(self.IdentifierLabel)
        self.IdentifierLineEdit = QtWidgets.QLineEdit(AddFootnoteDialog)
        self.IdentifierLineEdit.setObjectName("IdentifierLineEdit")
        self.horizontalLayout.addWidget(self.IdentifierLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.TextLabel = QtWidgets.QLabel(AddFootnoteDialog)
        self.TextLabel.setObjectName("TextLabel")
        self.verticalLayout.addWidget(self.TextLabel)
        self.TextPlainTextEdit = QtWidgets.QPlainTextEdit(AddFootnoteDialog)
        self.TextPlainTextEdit.setObjectName("TextPlainTextEdit")
        self.verticalLayout.addWidget(self.TextPlainTextEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddFootnoteDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddFootnoteDialog)
        self.buttonBox.accepted.connect(AddFootnoteDialog.accept)
        self.buttonBox.rejected.connect(AddFootnoteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddFootnoteDialog)

    def retranslateUi(self, AddFootnoteDialog):
        _translate = QtCore.QCoreApplication.translate
        AddFootnoteDialog.setWindowTitle(_translate("AddFootnoteDialog", "Add footnote"))
        self.AutogenIdentifierCheckbox.setText(_translate("AddFootnoteDialog", "Generate identifier automatically"))
        self.IdentifierLabel.setText(_translate("AddFootnoteDialog", "Identifier"))
        self.TextLabel.setText(_translate("AddFootnoteDialog", "Footnote text"))