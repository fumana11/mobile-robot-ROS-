# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controller.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(855, 378)
        self.btn_forward = QtWidgets.QPushButton(Form)
        self.btn_forward.setGeometry(QtCore.QRect(601, 100, 89, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btn_forward.setFont(font)
        self.btn_forward.setObjectName("btn_forward")
        self.btn_reverse = QtWidgets.QPushButton(Form)
        self.btn_reverse.setGeometry(QtCore.QRect(601, 220, 89, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btn_reverse.setFont(font)
        self.btn_reverse.setObjectName("btn_reverse")
        self.btn_turnRight = QtWidgets.QPushButton(Form)
        self.btn_turnRight.setGeometry(QtCore.QRect(711, 161, 89, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btn_turnRight.setFont(font)
        self.btn_turnRight.setObjectName("btn_turnRight")
        self.btn_turnLeft = QtWidgets.QPushButton(Form)
        self.btn_turnLeft.setGeometry(QtCore.QRect(491, 161, 89, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btn_turnLeft.setFont(font)
        self.btn_turnLeft.setObjectName("btn_turnLeft")
        self.btn_rotateLeft = QtWidgets.QPushButton(Form)
        self.btn_rotateLeft.setGeometry(QtCore.QRect(490, 10, 60, 50))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btn_rotateLeft.setFont(font)
        self.btn_rotateLeft.setObjectName("btn_rotateLeft")
        self.btn_rotateRight = QtWidgets.QPushButton(Form)
        self.btn_rotateRight.setGeometry(QtCore.QRect(741, 10, 60, 50))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btn_rotateRight.setFont(font)
        self.btn_rotateRight.setObjectName("btn_rotateRight")
        self.btn_stop = QtWidgets.QPushButton(Form)
        self.btn_stop.setGeometry(QtCore.QRect(611, 10, 70, 50))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(480, 70, 71, 17))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(730, 70, 91, 17))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(625, 70, 41, 17))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(610, 150, 61, 17))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(615, 270, 61, 17))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(710, 210, 91, 17))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(490, 210, 91, 17))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(460, 320, 111, 20))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.lbl_sensorDepan = QtWidgets.QLabel(Form)
        self.lbl_sensorDepan.setGeometry(QtCore.QRect(470, 340, 91, 41))
        self.lbl_sensorDepan.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sensorDepan.setObjectName("lbl_sensorDepan")
        self.lbl_robotMove = QtWidgets.QLabel(Form)
        self.lbl_robotMove.setGeometry(QtCore.QRect(600, 340, 91, 41))
        self.lbl_robotMove.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_robotMove.setObjectName("lbl_robotMove")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(590, 320, 111, 20))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(710, 320, 121, 20))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.lbl_sensorBelakang = QtWidgets.QLabel(Form)
        self.lbl_sensorBelakang.setGeometry(QtCore.QRect(730, 340, 91, 41))
        self.lbl_sensorBelakang.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sensorBelakang.setObjectName("lbl_sensorBelakang")
        self.lbl_openCv = QtWidgets.QLabel(Form)
        self.lbl_openCv.setGeometry(QtCore.QRect(10, 10, 451, 241))
        self.lbl_openCv.setText("")
        self.lbl_openCv.setObjectName("lbl_openCv")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(80, 320, 351, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(10, 320, 71, 20))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_forward.setText(_translate("Form", "↑"))
        self.btn_reverse.setText(_translate("Form", "↓"))
        self.btn_turnRight.setText(_translate("Form", "→"))
        self.btn_turnLeft.setText(_translate("Form", "←"))
        self.btn_rotateLeft.setText(_translate("Form", "↺"))
        self.btn_rotateRight.setText(_translate("Form", "↻"))
        self.btn_stop.setText(_translate("Form", "⊝"))
        self.label.setText(_translate("Form", "Rotasi Kiri"))
        self.label_2.setText(_translate("Form", "Rotasi Kanan"))
        self.label_3.setText(_translate("Form", "Stop"))
        self.label_4.setText(_translate("Form", "Maju"))
        self.label_5.setText(_translate("Form", "Mundur"))
        self.label_6.setText(_translate("Form", "Belok Kanan"))
        self.label_7.setText(_translate("Form", "Belok Kiri"))
        self.label_8.setText(_translate("Form", "Sensor Depan:"))
        self.lbl_sensorDepan.setText(_translate("Form", "TextLabel"))
        self.lbl_robotMove.setText(_translate("Form", "TextLabel"))
        self.label_11.setText(_translate("Form", "Gerak Robot:"))
        self.label_12.setText(_translate("Form", "Sensor Belakang:"))
        self.lbl_sensorBelakang.setText(_translate("Form", "TextLabel"))
        self.label_10.setText(_translate("Form", "Speed:"))