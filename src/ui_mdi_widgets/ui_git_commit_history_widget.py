# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/git_commit_history_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitCommitHistoryWidget(object):
    def setupUi(self, GitCommitHistoryWidget):
        GitCommitHistoryWidget.setObjectName("GitCommitHistoryWidget")
        GitCommitHistoryWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitCommitHistoryWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(GitCommitHistoryWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(GitCommitHistoryWidget)
        QtCore.QMetaObject.connectSlotsByName(GitCommitHistoryWidget)

    def retranslateUi(self, GitCommitHistoryWidget):
        _translate = QtCore.QCoreApplication.translate
        GitCommitHistoryWidget.setWindowTitle(_translate("GitCommitHistoryWidget", "Commit history"))