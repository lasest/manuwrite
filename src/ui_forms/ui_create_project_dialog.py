# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/create_project_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateProjectDialog(object):
    def setupUi(self, CreateProjectDialog):
        CreateProjectDialog.setObjectName("CreateProjectDialog")
        CreateProjectDialog.resize(539, 242)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateProjectDialog.sizePolicy().hasHeightForWidth())
        CreateProjectDialog.setSizePolicy(sizePolicy)
        CreateProjectDialog.setMinimumSize(QtCore.QSize(500, 200))
        CreateProjectDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateProjectDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LabelsLayout = QtWidgets.QVBoxLayout()
        self.LabelsLayout.setObjectName("LabelsLayout")
        self.TitleLabel = QtWidgets.QLabel(CreateProjectDialog)
        self.TitleLabel.setObjectName("TitleLabel")
        self.LabelsLayout.addWidget(self.TitleLabel)
        self.AuthorsLabel = QtWidgets.QLabel(CreateProjectDialog)
        self.AuthorsLabel.setObjectName("AuthorsLabel")
        self.LabelsLayout.addWidget(self.AuthorsLabel)
        self.ProjectTypeLabel = QtWidgets.QLabel(CreateProjectDialog)
        self.ProjectTypeLabel.setObjectName("ProjectTypeLabel")
        self.LabelsLayout.addWidget(self.ProjectTypeLabel)
        self.horizontalLayout.addLayout(self.LabelsLayout)
        self.InputsLayout = QtWidgets.QVBoxLayout()
        self.InputsLayout.setObjectName("InputsLayout")
        self.TitleLineEdit = QtWidgets.QLineEdit(CreateProjectDialog)
        self.TitleLineEdit.setObjectName("TitleLineEdit")
        self.InputsLayout.addWidget(self.TitleLineEdit)
        self.AuthoursLineEdit = QtWidgets.QLineEdit(CreateProjectDialog)
        self.AuthoursLineEdit.setObjectName("AuthoursLineEdit")
        self.InputsLayout.addWidget(self.AuthoursLineEdit)
        self.ProjectTypeComboBox = QtWidgets.QComboBox(CreateProjectDialog)
        self.ProjectTypeComboBox.setObjectName("ProjectTypeComboBox")
        self.InputsLayout.addWidget(self.ProjectTypeComboBox)
        self.horizontalLayout.addLayout(self.InputsLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(CreateProjectDialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.LocationLayout = QtWidgets.QHBoxLayout()
        self.LocationLayout.setObjectName("LocationLayout")
        self.LocationLineEdit = QtWidgets.QLineEdit(CreateProjectDialog)
        self.LocationLineEdit.setObjectName("LocationLineEdit")
        self.LocationLayout.addWidget(self.LocationLineEdit)
        self.LocationToolButton = QtWidgets.QToolButton(CreateProjectDialog)
        self.LocationToolButton.setObjectName("LocationToolButton")
        self.LocationLayout.addWidget(self.LocationToolButton)
        self.verticalLayout.addLayout(self.LocationLayout)
        self.ResultButtonsLayout = QtWidgets.QHBoxLayout()
        self.ResultButtonsLayout.setObjectName("ResultButtonsLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultButtonsLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(CreateProjectDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.ResultButtonsLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.ResultButtonsLayout)
        self.actionChooseFolder = QtWidgets.QAction(CreateProjectDialog)
        self.actionChooseFolder.setObjectName("actionChooseFolder")

        self.retranslateUi(CreateProjectDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateProjectDialog)

    def retranslateUi(self, CreateProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateProjectDialog.setWindowTitle(_translate("CreateProjectDialog", "Create project"))
        self.TitleLabel.setText(_translate("CreateProjectDialog", "Title"))
        self.AuthorsLabel.setText(_translate("CreateProjectDialog", "Authors"))
        self.ProjectTypeLabel.setText(_translate("CreateProjectDialog", "Project type"))
        self.label_4.setText(_translate("CreateProjectDialog", "Location:"))
        self.LocationToolButton.setText(_translate("CreateProjectDialog", "..."))
        self.actionChooseFolder.setText(_translate("CreateProjectDialog", "Choose folder"))