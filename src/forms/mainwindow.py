# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MainTabsFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainTabsFrame.sizePolicy().hasHeightForWidth())
        self.MainTabsFrame.setSizePolicy(sizePolicy)
        self.MainTabsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainTabsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainTabsFrame.setObjectName("MainTabsFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.MainTabsFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.EditorTabLabel = QLabelClickable(self.MainTabsFrame)
        self.EditorTabLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.EditorTabLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.EditorTabLabel.setObjectName("EditorTabLabel")
        self.verticalLayout.addWidget(self.EditorTabLabel)
        self.GitTabLabel = QLabelClickable(self.MainTabsFrame)
        self.GitTabLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.GitTabLabel.setObjectName("GitTabLabel")
        self.verticalLayout.addWidget(self.GitTabLabel)
        self.ProjectTabLabel = QLabelClickable(self.MainTabsFrame)
        self.ProjectTabLabel.setObjectName("ProjectTabLabel")
        self.verticalLayout.addWidget(self.ProjectTabLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.SettingsLabel = QtWidgets.QLabel(self.MainTabsFrame)
        self.SettingsLabel.setObjectName("SettingsLabel")
        self.verticalLayout.addWidget(self.SettingsLabel)
        self.UserAccounLabel = QtWidgets.QLabel(self.MainTabsFrame)
        self.UserAccounLabel.setObjectName("UserAccounLabel")
        self.verticalLayout.addWidget(self.UserAccounLabel)
        self.horizontalLayout.addWidget(self.MainTabsFrame)
        self.MainVerticalLayout = QtWidgets.QVBoxLayout()
        self.MainVerticalLayout.setObjectName("MainVerticalLayout")
        self.MainStackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.MainStackedWidget.setObjectName("MainStackedWidget")
        self.WelcomePage = QtWidgets.QWidget()
        self.WelcomePage.setObjectName("WelcomePage")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.WelcomePage)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.WelcomePage)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.MainStackedWidget.addWidget(self.WelcomePage)
        self.EdtiorPage = QtWidgets.QWidget()
        self.EdtiorPage.setObjectName("EdtiorPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.EdtiorPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.EdtiorPage)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.MainEditor = TextEditor(self.tab)
        self.MainEditor.setObjectName("MainEditor")
        self.verticalLayout_3.addWidget(self.MainEditor)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textEdit = TextEditor(self.tab_2)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_5.addWidget(self.textEdit)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.MainStackedWidget.addWidget(self.EdtiorPage)
        self.GitPage = QtWidgets.QWidget()
        self.GitPage.setObjectName("GitPage")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.GitPage)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.GitPage)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.MainStackedWidget.addWidget(self.GitPage)
        self.ProjectPage = QtWidgets.QWidget()
        self.ProjectPage.setObjectName("ProjectPage")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.ProjectPage)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.ProjectPage)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.MainStackedWidget.addWidget(self.ProjectPage)
        self.MainVerticalLayout.addWidget(self.MainStackedWidget)
        self.horizontalLayout.addLayout(self.MainVerticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.MainStackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.EditorTabLabel.setText(_translate("MainWindow", "one"))
        self.GitTabLabel.setText(_translate("MainWindow", "two"))
        self.ProjectTabLabel.setText(_translate("MainWindow", "proj"))
        self.SettingsLabel.setText(_translate("MainWindow", "accou"))
        self.UserAccounLabel.setText(_translate("MainWindow", "opt"))
        self.label_3.setText(_translate("MainWindow", "Welcome page"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.label.setText(_translate("MainWindow", "Git tab"))
        self.label_2.setText(_translate("MainWindow", "Project tab"))
from gui_components.qlabel_clickable import QLabelClickable
from gui_components.text_editor import TextEditor
