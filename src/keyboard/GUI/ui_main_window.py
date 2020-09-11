# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1153, 918)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")
        self.keyboard = QtWidgets.QWidget()
        self.keyboard.setObjectName("keyboard")
        self.scrollArea_keyboard = QtWidgets.QScrollArea(self.keyboard)
        self.scrollArea_keyboard.setGeometry(QtCore.QRect(12, 8, 805, 821))
        self.scrollArea_keyboard.setWidgetResizable(False)
        self.scrollArea_keyboard.setObjectName("scrollArea_keyboard")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 775, 815))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.groupBox_keyboard = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_keyboard.setGeometry(QtCore.QRect(8, 8, 773, 797))
        self.groupBox_keyboard.setTitle("")
        self.groupBox_keyboard.setObjectName("groupBox_keyboard")
        self.widget_keyboard = QtWidgets.QWidget(self.groupBox_keyboard)
        self.widget_keyboard.setGeometry(QtCore.QRect(20, 579, 717, 197))
        self.widget_keyboard.setObjectName("widget_keyboard")
        self.scrollArea_keyboard.setWidget(self.scrollAreaWidgetContents)
        self.tabs.addTab(self.keyboard, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.scrollArea_settings = QtWidgets.QScrollArea(self.settings)
        self.scrollArea_settings.setGeometry(QtCore.QRect(4, 4, 761, 557))
        self.scrollArea_settings.setWidgetResizable(True)
        self.scrollArea_settings.setObjectName("scrollArea_settings")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 759, 555))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.groupBox_status = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_status.setGeometry(QtCore.QRect(8, 8, 737, 537))
        self.groupBox_status.setObjectName("groupBox_status")
        self.scrollArea_settings.setWidget(self.scrollAreaWidgetContents_3)
        self.tabs.addTab(self.settings, "")
        self.gridLayout.addWidget(self.tabs, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1153, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Health Monitor"))
        self.tabs.setTabText(self.tabs.indexOf(self.keyboard), _translate("MainWindow", "Keyboard"))
        self.groupBox_status.setTitle(_translate("MainWindow", "Status"))
        self.tabs.setTabText(self.tabs.indexOf(self.settings), _translate("MainWindow", "Settings"))