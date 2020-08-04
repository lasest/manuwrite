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
        MainWindow.resize(793, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MainTabsFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
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
        self.EditorTabLabel.setAutoFillBackground(True)
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
        self.GitTabLabel.setAutoFillBackground(True)
        self.GitTabLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.GitTabLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GitTabLabel.setObjectName("GitTabLabel")
        self.verticalLayout.addWidget(self.GitTabLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.ProjectTabLabel = QLabelClickable(self.MainTabsFrame)
        self.ProjectTabLabel.setAutoFillBackground(True)
        self.ProjectTabLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.ProjectTabLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ProjectTabLabel.setObjectName("ProjectTabLabel")
        self.verticalLayout.addWidget(self.ProjectTabLabel)
        self.SettingsLabel = QLabelClickable(self.MainTabsFrame)
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
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.EdtiorPage)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame = QtWidgets.QFrame(self.EdtiorPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ItalicToolButton = QtWidgets.QToolButton(self.frame)
        self.ItalicToolButton.setIconSize(QtCore.QSize(22, 22))
        self.ItalicToolButton.setObjectName("ItalicToolButton")
        self.horizontalLayout_5.addWidget(self.ItalicToolButton)
        self.BoldToolButton = QtWidgets.QToolButton(self.frame)
        self.BoldToolButton.setIconSize(QtCore.QSize(22, 22))
        self.BoldToolButton.setObjectName("BoldToolButton")
        self.horizontalLayout_5.addWidget(self.BoldToolButton)
        self.BoldItalicToolButton = QtWidgets.QToolButton(self.frame)
        self.BoldItalicToolButton.setIconSize(QtCore.QSize(22, 22))
        self.BoldItalicToolButton.setObjectName("BoldItalicToolButton")
        self.horizontalLayout_5.addWidget(self.BoldItalicToolButton)
        self.StrikethroughToolButton = QtWidgets.QToolButton(self.frame)
        self.StrikethroughToolButton.setIconSize(QtCore.QSize(22, 22))
        self.StrikethroughToolButton.setObjectName("StrikethroughToolButton")
        self.horizontalLayout_5.addWidget(self.StrikethroughToolButton)
        self.SuperscriptToolButton = QtWidgets.QToolButton(self.frame)
        self.SuperscriptToolButton.setIconSize(QtCore.QSize(22, 22))
        self.SuperscriptToolButton.setObjectName("SuperscriptToolButton")
        self.horizontalLayout_5.addWidget(self.SuperscriptToolButton)
        self.SubscriptToolButton = QtWidgets.QToolButton(self.frame)
        self.SubscriptToolButton.setIconSize(QtCore.QSize(22, 22))
        self.SubscriptToolButton.setObjectName("SubscriptToolButton")
        self.horizontalLayout_5.addWidget(self.SubscriptToolButton)
        self.HeadingToolButton = QtWidgets.QToolButton(self.frame)
        self.HeadingToolButton.setIconSize(QtCore.QSize(22, 22))
        self.HeadingToolButton.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.HeadingToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.HeadingToolButton.setArrowType(QtCore.Qt.NoArrow)
        self.HeadingToolButton.setObjectName("HeadingToolButton")
        self.horizontalLayout_5.addWidget(self.HeadingToolButton)
        self.HorizontalRuleToolButton = QtWidgets.QToolButton(self.frame)
        self.HorizontalRuleToolButton.setIconSize(QtCore.QSize(22, 22))
        self.HorizontalRuleToolButton.setObjectName("HorizontalRuleToolButton")
        self.horizontalLayout_5.addWidget(self.HorizontalRuleToolButton)
        self.BlockquoteToolButton = QtWidgets.QToolButton(self.frame)
        self.BlockquoteToolButton.setIconSize(QtCore.QSize(22, 22))
        self.BlockquoteToolButton.setObjectName("BlockquoteToolButton")
        self.horizontalLayout_5.addWidget(self.BlockquoteToolButton)
        self.OrdListToolButton = QtWidgets.QToolButton(self.frame)
        self.OrdListToolButton.setIconSize(QtCore.QSize(22, 22))
        self.OrdListToolButton.setObjectName("OrdListToolButton")
        self.horizontalLayout_5.addWidget(self.OrdListToolButton)
        self.UnordListToolButton = QtWidgets.QToolButton(self.frame)
        self.UnordListToolButton.setIconSize(QtCore.QSize(22, 22))
        self.UnordListToolButton.setObjectName("UnordListToolButton")
        self.horizontalLayout_5.addWidget(self.UnordListToolButton)
        self.LinkToolButton = QtWidgets.QToolButton(self.frame)
        self.LinkToolButton.setIconSize(QtCore.QSize(22, 22))
        self.LinkToolButton.setObjectName("LinkToolButton")
        self.horizontalLayout_5.addWidget(self.LinkToolButton)
        self.ImageToolButton = QtWidgets.QToolButton(self.frame)
        self.ImageToolButton.setIconSize(QtCore.QSize(22, 22))
        self.ImageToolButton.setObjectName("ImageToolButton")
        self.horizontalLayout_5.addWidget(self.ImageToolButton)
        self.CodeToolButton = QtWidgets.QToolButton(self.frame)
        self.CodeToolButton.setIconSize(QtCore.QSize(22, 22))
        self.CodeToolButton.setObjectName("CodeToolButton")
        self.horizontalLayout_5.addWidget(self.CodeToolButton)
        self.AddCitationToolButton = QtWidgets.QToolButton(self.frame)
        self.AddCitationToolButton.setObjectName("AddCitationToolButton")
        self.horizontalLayout_5.addWidget(self.AddCitationToolButton)
        self.RenderFileToolButton = QtWidgets.QToolButton(self.frame)
        self.RenderFileToolButton.setObjectName("RenderFileToolButton")
        self.horizontalLayout_5.addWidget(self.RenderFileToolButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_6.addWidget(self.frame)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.EdtiorPage)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.ProjectWidget = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ProjectWidget.sizePolicy().hasHeightForWidth())
        self.ProjectWidget.setSizePolicy(sizePolicy)
        self.ProjectWidget.setObjectName("ProjectWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ProjectWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ProjectLabel = QtWidgets.QLabel(self.ProjectWidget)
        self.ProjectLabel.setAutoFillBackground(True)
        self.ProjectLabel.setStyleSheet("")
        self.ProjectLabel.setObjectName("ProjectLabel")
        self.verticalLayout_4.addWidget(self.ProjectLabel)
        self.ProjectTreeView = QtWidgets.QTreeView(self.ProjectWidget)
        self.ProjectTreeView.setMinimumSize(QtCore.QSize(150, 0))
        self.ProjectTreeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ProjectTreeView.setObjectName("ProjectTreeView")
        self.verticalLayout_4.addWidget(self.ProjectTreeView)
        self.EditorTabWidget = QTabWidgetCustom(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EditorTabWidget.sizePolicy().hasHeightForWidth())
        self.EditorTabWidget.setSizePolicy(sizePolicy)
        self.EditorTabWidget.setTabsClosable(True)
        self.EditorTabWidget.setMovable(True)
        self.EditorTabWidget.setObjectName("EditorTabWidget")
        self.tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.EditorTabWidget.addTab(self.tab, "")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.verticalLayoutWidget)
        self.webEngineView.setMinimumSize(QtCore.QSize(200, 0))
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.verticalLayout_3.addWidget(self.webEngineView)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
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
        self.MainVerticalLayout.addWidget(self.MainStackedWidget)
        self.horizontalLayout.addLayout(self.MainVerticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 793, 35))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menuBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionBold = QtWidgets.QAction(MainWindow)
        self.actionBold.setObjectName("actionBold")
        self.actionItalic = QtWidgets.QAction(MainWindow)
        self.actionItalic.setObjectName("actionItalic")
        self.actionBoldItalic = QtWidgets.QAction(MainWindow)
        self.actionBoldItalic.setObjectName("actionBoldItalic")
        self.actionHeading1 = QtWidgets.QAction(MainWindow)
        self.actionHeading1.setObjectName("actionHeading1")
        self.actionHeading2 = QtWidgets.QAction(MainWindow)
        self.actionHeading2.setObjectName("actionHeading2")
        self.actionHeading3 = QtWidgets.QAction(MainWindow)
        self.actionHeading3.setObjectName("actionHeading3")
        self.actionHeading4 = QtWidgets.QAction(MainWindow)
        self.actionHeading4.setObjectName("actionHeading4")
        self.actionHeading5 = QtWidgets.QAction(MainWindow)
        self.actionHeading5.setObjectName("actionHeading5")
        self.actionHeading6 = QtWidgets.QAction(MainWindow)
        self.actionHeading6.setObjectName("actionHeading6")
        self.actionHorizontalRule = QtWidgets.QAction(MainWindow)
        self.actionHorizontalRule.setObjectName("actionHorizontalRule")
        self.actionBlockquote = QtWidgets.QAction(MainWindow)
        self.actionBlockquote.setObjectName("actionBlockquote")
        self.actionOrdList = QtWidgets.QAction(MainWindow)
        self.actionOrdList.setObjectName("actionOrdList")
        self.actionUnordList = QtWidgets.QAction(MainWindow)
        self.actionUnordList.setObjectName("actionUnordList")
        self.actionLink = QtWidgets.QAction(MainWindow)
        self.actionLink.setObjectName("actionLink")
        self.actionImage = QtWidgets.QAction(MainWindow)
        self.actionImage.setObjectName("actionImage")
        self.actionCode = QtWidgets.QAction(MainWindow)
        self.actionCode.setObjectName("actionCode")
        self.actionAddCitation = QtWidgets.QAction(MainWindow)
        self.actionAddCitation.setObjectName("actionAddCitation")
        self.actionProjectTab = QtWidgets.QAction(MainWindow)
        self.actionProjectTab.setCheckable(True)
        self.actionProjectTab.setChecked(True)
        self.actionProjectTab.setObjectName("actionProjectTab")
        self.actionOpenProject = QtWidgets.QAction(MainWindow)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionNewProject = QtWidgets.QAction(MainWindow)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionCreateFolder = QtWidgets.QAction(MainWindow)
        self.actionCreateFolder.setObjectName("actionCreateFolder")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionCreateFile = QtWidgets.QAction(MainWindow)
        self.actionCreateFile.setObjectName("actionCreateFile")
        self.actionRename = QtWidgets.QAction(MainWindow)
        self.actionRename.setObjectName("actionRename")
        self.actionRenderFile = QtWidgets.QAction(MainWindow)
        self.actionRenderFile.setObjectName("actionRenderFile")
        self.actionShowPreview = QtWidgets.QAction(MainWindow)
        self.actionShowPreview.setCheckable(True)
        self.actionShowPreview.setChecked(True)
        self.actionShowPreview.setObjectName("actionShowPreview")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionStrikethrough = QtWidgets.QAction(MainWindow)
        self.actionStrikethrough.setObjectName("actionStrikethrough")
        self.actionSuperscript = QtWidgets.QAction(MainWindow)
        self.actionSuperscript.setObjectName("actionSuperscript")
        self.actionSubscript = QtWidgets.QAction(MainWindow)
        self.actionSubscript.setObjectName("actionSubscript")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionNewProject)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpenProject)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSettings)
        self.menuView.addAction(self.actionProjectTab)
        self.menuView.addAction(self.actionShowPreview)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())

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
        self.ItalicToolButton.setText(_translate("MainWindow", "..."))
        self.BoldToolButton.setText(_translate("MainWindow", "..."))
        self.BoldItalicToolButton.setText(_translate("MainWindow", "..."))
        self.StrikethroughToolButton.setText(_translate("MainWindow", "..."))
        self.SuperscriptToolButton.setText(_translate("MainWindow", "..."))
        self.SubscriptToolButton.setText(_translate("MainWindow", "..."))
        self.HeadingToolButton.setText(_translate("MainWindow", "..."))
        self.HorizontalRuleToolButton.setText(_translate("MainWindow", "..."))
        self.BlockquoteToolButton.setText(_translate("MainWindow", "..."))
        self.OrdListToolButton.setText(_translate("MainWindow", "..."))
        self.UnordListToolButton.setText(_translate("MainWindow", "..."))
        self.LinkToolButton.setText(_translate("MainWindow", "..."))
        self.ImageToolButton.setText(_translate("MainWindow", "..."))
        self.CodeToolButton.setText(_translate("MainWindow", "..."))
        self.AddCitationToolButton.setText(_translate("MainWindow", "..."))
        self.RenderFileToolButton.setText(_translate("MainWindow", "..."))
        self.ProjectLabel.setText(_translate("MainWindow", "Project"))
        self.EditorTabWidget.setTabText(self.EditorTabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.label.setText(_translate("MainWindow", "Git tab"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save as..."))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionBold.setText(_translate("MainWindow", "Bold"))
        self.actionBold.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.actionItalic.setText(_translate("MainWindow", "Italic"))
        self.actionItalic.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionBoldItalic.setText(_translate("MainWindow", "BoldItalic"))
        self.actionBoldItalic.setShortcut(_translate("MainWindow", "Ctrl+Shift+B"))
        self.actionHeading1.setText(_translate("MainWindow", "Heading1"))
        self.actionHeading1.setShortcut(_translate("MainWindow", "Ctrl+H, H"))
        self.actionHeading2.setText(_translate("MainWindow", "Heading2"))
        self.actionHeading2.setShortcut(_translate("MainWindow", "Ctrl+H, Ctrl+H"))
        self.actionHeading3.setText(_translate("MainWindow", "Heading3"))
        self.actionHeading3.setShortcut(_translate("MainWindow", "Ctrl+3"))
        self.actionHeading4.setText(_translate("MainWindow", "Heading4"))
        self.actionHeading4.setShortcut(_translate("MainWindow", "Ctrl+4"))
        self.actionHeading5.setText(_translate("MainWindow", "Heading5"))
        self.actionHeading5.setShortcut(_translate("MainWindow", "Ctrl+5"))
        self.actionHeading6.setText(_translate("MainWindow", "Heading6"))
        self.actionHeading6.setShortcut(_translate("MainWindow", "Ctrl+6"))
        self.actionHorizontalRule.setText(_translate("MainWindow", "HorizontalRule"))
        self.actionBlockquote.setText(_translate("MainWindow", "Blockquote"))
        self.actionOrdList.setText(_translate("MainWindow", "OrdList"))
        self.actionOrdList.setShortcut(_translate("MainWindow", "F12"))
        self.actionUnordList.setText(_translate("MainWindow", "UnordList"))
        self.actionUnordList.setShortcut(_translate("MainWindow", "Shift+F12"))
        self.actionLink.setText(_translate("MainWindow", "Link"))
        self.actionLink.setShortcut(_translate("MainWindow", "Ctrl+Shift+K"))
        self.actionImage.setText(_translate("MainWindow", "Image"))
        self.actionCode.setText(_translate("MainWindow", "Code"))
        self.actionAddCitation.setText(_translate("MainWindow", "Add Citation"))
        self.actionAddCitation.setShortcut(_translate("MainWindow", "Ctrl+K"))
        self.actionProjectTab.setText(_translate("MainWindow", "Project tab"))
        self.actionProjectTab.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))
        self.actionOpenProject.setText(_translate("MainWindow", "Open project"))
        self.actionOpenProject.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.actionNewProject.setText(_translate("MainWindow", "New project..."))
        self.actionNewProject.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.actionCreateFolder.setText(_translate("MainWindow", "Create Folder"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionCreateFile.setText(_translate("MainWindow", "Create File"))
        self.actionRename.setText(_translate("MainWindow", "Rename"))
        self.actionRenderFile.setText(_translate("MainWindow", "Render file"))
        self.actionRenderFile.setShortcut(_translate("MainWindow", "F5"))
        self.actionShowPreview.setText(_translate("MainWindow", "Show Preview"))
        self.actionShowPreview.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionStrikethrough.setText(_translate("MainWindow", "Strikethrough"))
        self.actionSuperscript.setText(_translate("MainWindow", "Superscript"))
        self.actionSubscript.setText(_translate("MainWindow", "Subscript"))
from PyQt5 import QtWebEngineWidgets
from gui_components.qlabel_clickable import QLabelClickable
from gui_components.qtabwidget_custom import QTabWidgetCustom
