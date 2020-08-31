# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(772, 609)
        SettingsDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MainTabWidget = QtWidgets.QTabWidget(SettingsDialog)
        self.MainTabWidget.setObjectName("MainTabWidget")
        self.GeneralTab = QtWidgets.QWidget()
        self.GeneralTab.setObjectName("GeneralTab")
        self.MainTabWidget.addTab(self.GeneralTab, "")
        self.EditorTab = QtWidgets.QWidget()
        self.EditorTab.setObjectName("EditorTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.EditorTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.FontLayout = QtWidgets.QHBoxLayout()
        self.FontLayout.setObjectName("FontLayout")
        self.FontLabel = QtWidgets.QLabel(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FontLabel.sizePolicy().hasHeightForWidth())
        self.FontLabel.setSizePolicy(sizePolicy)
        self.FontLabel.setObjectName("FontLabel")
        self.FontLayout.addWidget(self.FontLabel)
        self.FontComboBox = QtWidgets.QFontComboBox(self.EditorTab)
        self.FontComboBox.setObjectName("FontComboBox")
        self.FontLayout.addWidget(self.FontComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.FontLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.FontLayout)
        self.FontSizeLayout = QtWidgets.QHBoxLayout()
        self.FontSizeLayout.setObjectName("FontSizeLayout")
        self.FontSizeLabel = QtWidgets.QLabel(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FontSizeLabel.sizePolicy().hasHeightForWidth())
        self.FontSizeLabel.setSizePolicy(sizePolicy)
        self.FontSizeLabel.setObjectName("FontSizeLabel")
        self.FontSizeLayout.addWidget(self.FontSizeLabel)
        self.FontSizeSpinBox = QtWidgets.QSpinBox(self.EditorTab)
        self.FontSizeSpinBox.setObjectName("FontSizeSpinBox")
        self.FontSizeLayout.addWidget(self.FontSizeSpinBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.FontSizeLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.FontSizeLayout)
        self.DefaultImageSizeLayout = QtWidgets.QHBoxLayout()
        self.DefaultImageSizeLayout.setObjectName("DefaultImageSizeLayout")
        self.DefaultImageSizeLabel = QtWidgets.QLabel(self.EditorTab)
        self.DefaultImageSizeLabel.setObjectName("DefaultImageSizeLabel")
        self.DefaultImageSizeLayout.addWidget(self.DefaultImageSizeLabel)
        self.DefImageSizeInputsLayout = QtWidgets.QVBoxLayout()
        self.DefImageSizeInputsLayout.setObjectName("DefImageSizeInputsLayout")
        self.DefImageSizeWidthLineEdit = QtWidgets.QLineEdit(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DefImageSizeWidthLineEdit.sizePolicy().hasHeightForWidth())
        self.DefImageSizeWidthLineEdit.setSizePolicy(sizePolicy)
        self.DefImageSizeWidthLineEdit.setObjectName("DefImageSizeWidthLineEdit")
        self.DefImageSizeInputsLayout.addWidget(self.DefImageSizeWidthLineEdit)
        self.DefImageSizeHeightLineEdit = QtWidgets.QLineEdit(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DefImageSizeHeightLineEdit.sizePolicy().hasHeightForWidth())
        self.DefImageSizeHeightLineEdit.setSizePolicy(sizePolicy)
        self.DefImageSizeHeightLineEdit.setObjectName("DefImageSizeHeightLineEdit")
        self.DefImageSizeInputsLayout.addWidget(self.DefImageSizeHeightLineEdit)
        self.DefaultImageSizeLayout.addLayout(self.DefImageSizeInputsLayout)
        self.DefImageSizeLayoutInner = QtWidgets.QVBoxLayout()
        self.DefImageSizeLayoutInner.setObjectName("DefImageSizeLayoutInner")
        self.DefImageSizeWidthLabel = QtWidgets.QLabel(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DefImageSizeWidthLabel.sizePolicy().hasHeightForWidth())
        self.DefImageSizeWidthLabel.setSizePolicy(sizePolicy)
        self.DefImageSizeWidthLabel.setObjectName("DefImageSizeWidthLabel")
        self.DefImageSizeLayoutInner.addWidget(self.DefImageSizeWidthLabel)
        self.DefImageSizeHeightLabel = QtWidgets.QLabel(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DefImageSizeHeightLabel.sizePolicy().hasHeightForWidth())
        self.DefImageSizeHeightLabel.setSizePolicy(sizePolicy)
        self.DefImageSizeHeightLabel.setObjectName("DefImageSizeHeightLabel")
        self.DefImageSizeLayoutInner.addWidget(self.DefImageSizeHeightLabel)
        self.DefaultImageSizeLayout.addLayout(self.DefImageSizeLayoutInner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.DefaultImageSizeLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.DefaultImageSizeLayout)
        self.ShowImageTooltipsCheckBox = QtWidgets.QCheckBox(self.EditorTab)
        self.ShowImageTooltipsCheckBox.setObjectName("ShowImageTooltipsCheckBox")
        self.verticalLayout_2.addWidget(self.ShowImageTooltipsCheckBox)
        self.ImageToolTipLayout = QtWidgets.QHBoxLayout()
        self.ImageToolTipLayout.setObjectName("ImageToolTipLayout")
        self.ImageToolTipLabel = QtWidgets.QLabel(self.EditorTab)
        self.ImageToolTipLabel.setObjectName("ImageToolTipLabel")
        self.ImageToolTipLayout.addWidget(self.ImageToolTipLabel)
        self.ImageToolTipInputsLayout = QtWidgets.QVBoxLayout()
        self.ImageToolTipInputsLayout.setObjectName("ImageToolTipInputsLayout")
        self.ImageToolTipWidthLineEdit = QtWidgets.QLineEdit(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageToolTipWidthLineEdit.sizePolicy().hasHeightForWidth())
        self.ImageToolTipWidthLineEdit.setSizePolicy(sizePolicy)
        self.ImageToolTipWidthLineEdit.setObjectName("ImageToolTipWidthLineEdit")
        self.ImageToolTipInputsLayout.addWidget(self.ImageToolTipWidthLineEdit)
        self.ImageToolTipHeightLineEdit = QtWidgets.QLineEdit(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageToolTipHeightLineEdit.sizePolicy().hasHeightForWidth())
        self.ImageToolTipHeightLineEdit.setSizePolicy(sizePolicy)
        self.ImageToolTipHeightLineEdit.setObjectName("ImageToolTipHeightLineEdit")
        self.ImageToolTipInputsLayout.addWidget(self.ImageToolTipHeightLineEdit)
        self.ImageToolTipLayout.addLayout(self.ImageToolTipInputsLayout)
        self.ImageToolTipDimLayout = QtWidgets.QVBoxLayout()
        self.ImageToolTipDimLayout.setObjectName("ImageToolTipDimLayout")
        self.ImageToolTipWidthLabel = QtWidgets.QLabel(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageToolTipWidthLabel.sizePolicy().hasHeightForWidth())
        self.ImageToolTipWidthLabel.setSizePolicy(sizePolicy)
        self.ImageToolTipWidthLabel.setObjectName("ImageToolTipWidthLabel")
        self.ImageToolTipDimLayout.addWidget(self.ImageToolTipWidthLabel)
        self.ImageToolTipHeightLabel = QtWidgets.QLabel(self.EditorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageToolTipHeightLabel.sizePolicy().hasHeightForWidth())
        self.ImageToolTipHeightLabel.setSizePolicy(sizePolicy)
        self.ImageToolTipHeightLabel.setObjectName("ImageToolTipHeightLabel")
        self.ImageToolTipDimLayout.addWidget(self.ImageToolTipHeightLabel)
        self.ImageToolTipLayout.addLayout(self.ImageToolTipDimLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ImageToolTipLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.ImageToolTipLayout)
        self.ShowCitationTooltipsCheckBox = QtWidgets.QCheckBox(self.EditorTab)
        self.ShowCitationTooltipsCheckBox.setObjectName("ShowCitationTooltipsCheckBox")
        self.verticalLayout_2.addWidget(self.ShowCitationTooltipsCheckBox)
        self.MainTabWidget.addTab(self.EditorTab, "")
        self.RenderTab = QtWidgets.QWidget()
        self.RenderTab.setObjectName("RenderTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.RenderTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.AllowAutoRenderCheckbox = QtWidgets.QCheckBox(self.RenderTab)
        self.AllowAutoRenderCheckbox.setObjectName("AllowAutoRenderCheckbox")
        self.verticalLayout_3.addWidget(self.AllowAutoRenderCheckbox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AutoRenderDelayLabel = QtWidgets.QLabel(self.RenderTab)
        self.AutoRenderDelayLabel.setObjectName("AutoRenderDelayLabel")
        self.horizontalLayout.addWidget(self.AutoRenderDelayLabel)
        self.AutorenderDelayLineEdit = QtWidgets.QLineEdit(self.RenderTab)
        self.AutorenderDelayLineEdit.setObjectName("AutorenderDelayLineEdit")
        self.horizontalLayout.addWidget(self.AutorenderDelayLineEdit)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.MainTabWidget.addTab(self.RenderTab, "")
        self.ColorsTab = QtWidgets.QWidget()
        self.ColorsTab.setObjectName("ColorsTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ColorsTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ColorSchemaFrame = QtWidgets.QFrame(self.ColorsTab)
        self.ColorSchemaFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ColorSchemaFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ColorSchemaFrame.setObjectName("ColorSchemaFrame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.ColorSchemaFrame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ColorSchemaLayout = QtWidgets.QHBoxLayout()
        self.ColorSchemaLayout.setObjectName("ColorSchemaLayout")
        self.ColorSchemaLabel = QtWidgets.QLabel(self.ColorSchemaFrame)
        self.ColorSchemaLabel.setObjectName("ColorSchemaLabel")
        self.ColorSchemaLayout.addWidget(self.ColorSchemaLabel)
        self.ColorSchemaComboBox = QtWidgets.QComboBox(self.ColorSchemaFrame)
        self.ColorSchemaComboBox.setObjectName("ColorSchemaComboBox")
        self.ColorSchemaLayout.addWidget(self.ColorSchemaComboBox)
        self.NewColorSchemaButton = QtWidgets.QPushButton(self.ColorSchemaFrame)
        self.NewColorSchemaButton.setObjectName("NewColorSchemaButton")
        self.ColorSchemaLayout.addWidget(self.NewColorSchemaButton)
        self.DeleteColorSchemaButton = QtWidgets.QPushButton(self.ColorSchemaFrame)
        self.DeleteColorSchemaButton.setObjectName("DeleteColorSchemaButton")
        self.ColorSchemaLayout.addWidget(self.DeleteColorSchemaButton)
        self.ImportColorSchemaButton = QtWidgets.QPushButton(self.ColorSchemaFrame)
        self.ImportColorSchemaButton.setObjectName("ImportColorSchemaButton")
        self.ColorSchemaLayout.addWidget(self.ImportColorSchemaButton)
        self.ExportColorSchemaButton = QtWidgets.QPushButton(self.ColorSchemaFrame)
        self.ExportColorSchemaButton.setObjectName("ExportColorSchemaButton")
        self.ColorSchemaLayout.addWidget(self.ExportColorSchemaButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ColorSchemaLayout.addItem(spacerItem6)
        self.verticalLayout_5.addLayout(self.ColorSchemaLayout)
        self.ColorsTable = QtWidgets.QTableWidget(self.ColorSchemaFrame)
        self.ColorsTable.setColumnCount(3)
        self.ColorsTable.setObjectName("ColorsTable")
        self.ColorsTable.setRowCount(0)
        self.ColorsTable.horizontalHeader().setVisible(False)
        self.ColorsTable.horizontalHeader().setCascadingSectionResizes(False)
        self.ColorsTable.horizontalHeader().setHighlightSections(False)
        self.ColorsTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_5.addWidget(self.ColorsTable)
        self.verticalLayout_4.addWidget(self.ColorSchemaFrame)
        self.MainTabWidget.addTab(self.ColorsTab, "")
        self.verticalLayout.addWidget(self.MainTabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        self.MainTabWidget.setCurrentIndex(3)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.MainTabWidget.setTabText(self.MainTabWidget.indexOf(self.GeneralTab), _translate("SettingsDialog", "General"))
        self.FontLabel.setText(_translate("SettingsDialog", "Font name"))
        self.FontSizeLabel.setText(_translate("SettingsDialog", "Font size"))
        self.DefaultImageSizeLabel.setText(_translate("SettingsDialog", "Default image size (px)"))
        self.DefImageSizeWidthLabel.setText(_translate("SettingsDialog", "Width"))
        self.DefImageSizeHeightLabel.setText(_translate("SettingsDialog", "Height"))
        self.ShowImageTooltipsCheckBox.setText(_translate("SettingsDialog", "Show image tooltips on mouse hover"))
        self.ImageToolTipLabel.setText(_translate("SettingsDialog", "Image tooltip size (px)"))
        self.ImageToolTipWidthLabel.setText(_translate("SettingsDialog", "Width"))
        self.ImageToolTipHeightLabel.setText(_translate("SettingsDialog", "Height"))
        self.ShowCitationTooltipsCheckBox.setText(_translate("SettingsDialog", "Show citation tooltips on mouse hover"))
        self.MainTabWidget.setTabText(self.MainTabWidget.indexOf(self.EditorTab), _translate("SettingsDialog", "Editor"))
        self.AllowAutoRenderCheckbox.setText(_translate("SettingsDialog", "Allow autorendering of the current file"))
        self.AutoRenderDelayLabel.setText(_translate("SettingsDialog", "Autorender delay (ms)"))
        self.MainTabWidget.setTabText(self.MainTabWidget.indexOf(self.RenderTab), _translate("SettingsDialog", "Render"))
        self.ColorSchemaLabel.setText(_translate("SettingsDialog", "Color Schema"))
        self.NewColorSchemaButton.setText(_translate("SettingsDialog", "New..."))
        self.DeleteColorSchemaButton.setText(_translate("SettingsDialog", "Delete"))
        self.ImportColorSchemaButton.setText(_translate("SettingsDialog", "Import..."))
        self.ExportColorSchemaButton.setText(_translate("SettingsDialog", "Export..."))
        self.MainTabWidget.setTabText(self.MainTabWidget.indexOf(self.ColorsTab), _translate("SettingsDialog", "Colors"))
