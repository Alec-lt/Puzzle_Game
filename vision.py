# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vision.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1095, 680)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AI = QtWidgets.QPushButton(self.centralwidget)
        self.AI.setGeometry(QtCore.QRect(850, 275, 171, 51))
        self.AI.setObjectName("AI")
        self.saveProgress = QtWidgets.QPushButton(self.centralwidget)
        self.saveProgress.setGeometry(QtCore.QRect(850, 372, 171, 51))
        self.saveProgress.setObjectName("saveProgress")
        self.readProgress = QtWidgets.QPushButton(self.centralwidget)
        self.readProgress.setGeometry(QtCore.QRect(850, 465, 171, 51))
        self.readProgress.setObjectName("readProgress")
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(850, 555, 171, 51))
        self.reset.setObjectName("reset")
        self.pictureChoose = QtWidgets.QPushButton(self.centralwidget)
        self.pictureChoose.setGeometry(QtCore.QRect(850, 35, 171, 51))
        self.pictureChoose.setObjectName("pictureChoose")
        self.upset = QtWidgets.QPushButton(self.centralwidget)
        self.upset.setGeometry(QtCore.QRect(850, 175, 171, 51))
        self.upset.setObjectName("upset")
        self.showView = QtWidgets.QGraphicsView(self.centralwidget)
        self.showView.setGeometry(QtCore.QRect(60, 50, 723, 543))
        self.showView.setObjectName("showView")
        self.selectHard = QtWidgets.QSpinBox(self.centralwidget)
        self.selectHard.setGeometry(QtCore.QRect(960, 115, 61, 31))
        self.selectHard.setObjectName("selectHard")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(860, 120, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1095, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "拼图小游戏"))
        self.AI.setText(_translate("MainWindow", "AI还原"))
        self.saveProgress.setText(_translate("MainWindow", "保存进度"))
        self.readProgress.setText(_translate("MainWindow", "读取进度"))
        self.reset.setText(_translate("MainWindow", "重置"))
        self.pictureChoose.setText(_translate("MainWindow", "选择图片"))
        self.upset.setText(_translate("MainWindow", "打乱"))
        self.label.setText(_translate("MainWindow", "选择阶数："))
