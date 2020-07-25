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
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 2)
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
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.EditorTabLabel = QLabelClickable(self.MainTabsFrame)
        self.EditorTabLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.EditorTabLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EditorTabLabel.setLineWidth(1)
        self.EditorTabLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.EditorTabLabel.setObjectName("EditorTabLabel")
        self.verticalLayout.addWidget(self.EditorTabLabel)
        self.GitTabLabel = QLabelClickable(self.MainTabsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GitTabLabel.sizePolicy().hasHeightForWidth())
        self.GitTabLabel.setSizePolicy(sizePolicy)
        self.GitTabLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.GitTabLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GitTabLabel.setObjectName("GitTabLabel")
        self.verticalLayout.addWidget(self.GitTabLabel)
        self.ProjectTabLabel = QLabelClickable(self.MainTabsFrame)
        self.ProjectTabLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.ProjectTabLabel.setFrameShadow(QtWidgets.QFrame.Raised)
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
        self.MainVerticalLayout.setSpacing(0)
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
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.EditorTabWidget = QTabWidgetCustom(self.EdtiorPage)
        self.EditorTabWidget.setTabsClosable(True)
        self.EditorTabWidget.setMovable(True)
        self.EditorTabWidget.setObjectName("EditorTabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.MainEditor = TextEditor(self.tab)
        self.MainEditor.setObjectName("MainEditor")
        self.verticalLayout_3.addWidget(self.MainEditor)
        self.EditorTabWidget.addTab(self.tab, "")
        self.verticalLayout_2.addWidget(self.EditorTabWidget)
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
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 35))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.MainStackedWidget.setCurrentIndex(1)
        self.EditorTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ManuWrite"))
        self.EditorTabLabel.setText(_translate("MainWindow", "one"))
        self.GitTabLabel.setText(_translate("MainWindow", "two"))
        self.ProjectTabLabel.setText(_translate("MainWindow", "proj"))
        self.SettingsLabel.setText(_translate("MainWindow", "accou"))
        self.UserAccounLabel.setText(_translate("MainWindow", "opt"))
        self.label_3.setText(_translate("MainWindow", "Welcome page"))
        self.EditorTabWidget.setTabText(self.EditorTabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.label.setText(_translate("MainWindow", "Git tab"))
        self.label_2.setText(_translate("MainWindow", "Project tab"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save as..."))
from gui_components.qlabel_clickable import QLabelClickable
from gui_components.qtabwidget_custom import QTabWidgetCustom
from gui_components.text_editor import TextEditor
