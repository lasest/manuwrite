# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/git_status_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitStatusWidget(object):
    def setupUi(self, GitStatusWidget):
        GitStatusWidget.setObjectName("GitStatusWidget")
        GitStatusWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitStatusWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(GitStatusWidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)

        self.retranslateUi(GitStatusWidget)
        QtCore.QMetaObject.connectSlotsByName(GitStatusWidget)

    def retranslateUi(self, GitStatusWidget):
        _translate = QtCore.QCoreApplication.translate
        GitStatusWidget.setWindowTitle(_translate("GitStatusWidget", "Status"))