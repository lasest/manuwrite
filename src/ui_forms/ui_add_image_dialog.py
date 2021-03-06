# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/add_image_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddImageDialog(object):
    def setupUi(self, AddImageDialog):
        AddImageDialog.setObjectName("AddImageDialog")
        AddImageDialog.setWindowModality(QtCore.Qt.WindowModal)
        AddImageDialog.resize(539, 275)
        AddImageDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddImageDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.InfoLabel = QtWidgets.QLabel(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.InfoLabel.sizePolicy().hasHeightForWidth())
        self.InfoLabel.setSizePolicy(sizePolicy)
        self.InfoLabel.setObjectName("InfoLabel")
        self.verticalLayout.addWidget(self.InfoLabel)
        self.AutogenIdentifierCheckbox = QtWidgets.QCheckBox(AddImageDialog)
        self.AutogenIdentifierCheckbox.setChecked(True)
        self.AutogenIdentifierCheckbox.setObjectName("AutogenIdentifierCheckbox")
        self.verticalLayout.addWidget(self.AutogenIdentifierCheckbox)
        self.AutonumberCheckbox = QtWidgets.QCheckBox(AddImageDialog)
        self.AutonumberCheckbox.setChecked(True)
        self.AutonumberCheckbox.setObjectName("AutonumberCheckbox")
        self.verticalLayout.addWidget(self.AutonumberCheckbox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LabelLayout = QtWidgets.QVBoxLayout()
        self.LabelLayout.setSpacing(7)
        self.LabelLayout.setObjectName("LabelLayout")
        self.IdentifierLabel = QtWidgets.QLabel(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IdentifierLabel.sizePolicy().hasHeightForWidth())
        self.IdentifierLabel.setSizePolicy(sizePolicy)
        self.IdentifierLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.IdentifierLabel.setObjectName("IdentifierLabel")
        self.LabelLayout.addWidget(self.IdentifierLabel)
        self.ImageTextLabel = QtWidgets.QLabel(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageTextLabel.sizePolicy().hasHeightForWidth())
        self.ImageTextLabel.setSizePolicy(sizePolicy)
        self.ImageTextLabel.setObjectName("ImageTextLabel")
        self.LabelLayout.addWidget(self.ImageTextLabel)
        self.ImagePathLabel = QtWidgets.QLabel(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImagePathLabel.sizePolicy().hasHeightForWidth())
        self.ImagePathLabel.setSizePolicy(sizePolicy)
        self.ImagePathLabel.setObjectName("ImagePathLabel")
        self.LabelLayout.addWidget(self.ImagePathLabel)
        self.horizontalLayout.addLayout(self.LabelLayout)
        self.InputLayout = QtWidgets.QVBoxLayout()
        self.InputLayout.setSpacing(7)
        self.InputLayout.setObjectName("InputLayout")
        self.IdentifierLineEdit = QtWidgets.QLineEdit(AddImageDialog)
        self.IdentifierLineEdit.setObjectName("IdentifierLineEdit")
        self.InputLayout.addWidget(self.IdentifierLineEdit)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ImageTextLineEdit = QtWidgets.QLineEdit(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageTextLineEdit.sizePolicy().hasHeightForWidth())
        self.ImageTextLineEdit.setSizePolicy(sizePolicy)
        self.ImageTextLineEdit.setMinimumSize(QtCore.QSize(350, 0))
        self.ImageTextLineEdit.setObjectName("ImageTextLineEdit")
        self.horizontalLayout_3.addWidget(self.ImageTextLineEdit)
        self.InputLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ImagePathLineEdit = QtWidgets.QLineEdit(AddImageDialog)
        self.ImagePathLineEdit.setMinimumSize(QtCore.QSize(350, 0))
        self.ImagePathLineEdit.setObjectName("ImagePathLineEdit")
        self.horizontalLayout_2.addWidget(self.ImagePathLineEdit)
        self.OpenFileButton = QtWidgets.QToolButton(AddImageDialog)
        self.OpenFileButton.setObjectName("OpenFileButton")
        self.horizontalLayout_2.addWidget(self.OpenFileButton)
        self.InputLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.InputLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.WidthLabel = QtWidgets.QLabel(AddImageDialog)
        self.WidthLabel.setObjectName("WidthLabel")
        self.horizontalLayout_4.addWidget(self.WidthLabel)
        self.WidthLineEdit = QtWidgets.QLineEdit(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WidthLineEdit.sizePolicy().hasHeightForWidth())
        self.WidthLineEdit.setSizePolicy(sizePolicy)
        self.WidthLineEdit.setObjectName("WidthLineEdit")
        self.horizontalLayout_4.addWidget(self.WidthLineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.HeightLabel = QtWidgets.QLabel(AddImageDialog)
        self.HeightLabel.setObjectName("HeightLabel")
        self.horizontalLayout_4.addWidget(self.HeightLabel)
        self.HeightLineEdit = QtWidgets.QLineEdit(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HeightLineEdit.sizePolicy().hasHeightForWidth())
        self.HeightLineEdit.setSizePolicy(sizePolicy)
        self.HeightLineEdit.setObjectName("HeightLineEdit")
        self.horizontalLayout_4.addWidget(self.HeightLineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddImageDialog)
        self.buttonBox.accepted.connect(AddImageDialog.accept)
        self.buttonBox.rejected.connect(AddImageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddImageDialog)

    def retranslateUi(self, AddImageDialog):
        _translate = QtCore.QCoreApplication.translate
        AddImageDialog.setWindowTitle(_translate("AddImageDialog", "Add image - ManuWrite"))
        self.InfoLabel.setText(_translate("AddImageDialog", "Enter image information:"))
        self.AutogenIdentifierCheckbox.setText(_translate("AddImageDialog", "Generate identifier automatically"))
        self.AutonumberCheckbox.setText(_translate("AddImageDialog", "Add figure number automatically"))
        self.IdentifierLabel.setText(_translate("AddImageDialog", "Identifier"))
        self.ImageTextLabel.setText(_translate("AddImageDialog", "Image text:"))
        self.ImagePathLabel.setText(_translate("AddImageDialog", "Path to image:"))
        self.OpenFileButton.setText(_translate("AddImageDialog", "..."))
        self.WidthLabel.setText(_translate("AddImageDialog", "Width:"))
        self.HeightLabel.setText(_translate("AddImageDialog", "Height:"))
