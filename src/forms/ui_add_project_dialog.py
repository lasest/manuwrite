# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/add_project_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddProjectDialog(object):
    def setupUi(self, AddProjectDialog):
        AddProjectDialog.setObjectName("AddProjectDialog")
        AddProjectDialog.resize(539, 242)
        AddProjectDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddProjectDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LabelsLayout = QtWidgets.QVBoxLayout()
        self.LabelsLayout.setObjectName("LabelsLayout")
        self.TitleLabel = QtWidgets.QLabel(AddProjectDialog)
        self.TitleLabel.setObjectName("TitleLabel")
        self.LabelsLayout.addWidget(self.TitleLabel)
        self.AuthorsLabel = QtWidgets.QLabel(AddProjectDialog)
        self.AuthorsLabel.setObjectName("AuthorsLabel")
        self.LabelsLayout.addWidget(self.AuthorsLabel)
        self.ProjectTypeLabel = QtWidgets.QLabel(AddProjectDialog)
        self.ProjectTypeLabel.setObjectName("ProjectTypeLabel")
        self.LabelsLayout.addWidget(self.ProjectTypeLabel)
        self.horizontalLayout.addLayout(self.LabelsLayout)
        self.InputsLayout = QtWidgets.QVBoxLayout()
        self.InputsLayout.setObjectName("InputsLayout")
        self.TitleLineEdit = QtWidgets.QLineEdit(AddProjectDialog)
        self.TitleLineEdit.setObjectName("TitleLineEdit")
        self.InputsLayout.addWidget(self.TitleLineEdit)
        self.AuthoursLineEdit = QtWidgets.QLineEdit(AddProjectDialog)
        self.AuthoursLineEdit.setObjectName("AuthoursLineEdit")
        self.InputsLayout.addWidget(self.AuthoursLineEdit)
        self.ProjectTypeComboBox = QtWidgets.QComboBox(AddProjectDialog)
        self.ProjectTypeComboBox.setObjectName("ProjectTypeComboBox")
        self.InputsLayout.addWidget(self.ProjectTypeComboBox)
        self.horizontalLayout.addLayout(self.InputsLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(AddProjectDialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.LocationLayout = QtWidgets.QHBoxLayout()
        self.LocationLayout.setObjectName("LocationLayout")
        self.LocationLineEdit = QtWidgets.QLineEdit(AddProjectDialog)
        self.LocationLineEdit.setObjectName("LocationLineEdit")
        self.LocationLayout.addWidget(self.LocationLineEdit)
        self.LocationToolButton = QtWidgets.QToolButton(AddProjectDialog)
        self.LocationToolButton.setObjectName("LocationToolButton")
        self.LocationLayout.addWidget(self.LocationToolButton)
        self.verticalLayout.addLayout(self.LocationLayout)
        self.ResultButtonsLayout = QtWidgets.QHBoxLayout()
        self.ResultButtonsLayout.setObjectName("ResultButtonsLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultButtonsLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddProjectDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.ResultButtonsLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.ResultButtonsLayout)

        self.retranslateUi(AddProjectDialog)
        QtCore.QMetaObject.connectSlotsByName(AddProjectDialog)

    def retranslateUi(self, AddProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        AddProjectDialog.setWindowTitle(_translate("AddProjectDialog", "Add project"))
        self.TitleLabel.setText(_translate("AddProjectDialog", "Title"))
        self.AuthorsLabel.setText(_translate("AddProjectDialog", "Authors"))
        self.ProjectTypeLabel.setText(_translate("AddProjectDialog", "Project type"))
        self.label_4.setText(_translate("AddProjectDialog", "Location:"))
        self.LocationToolButton.setText(_translate("AddProjectDialog", "..."))