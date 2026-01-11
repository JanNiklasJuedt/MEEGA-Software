# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_export.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Export(object):
    def setupUi(self, Export):
        if not Export.objectName():
            Export.setObjectName(u"Export")
        Export.resize(400, 280)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Export.sizePolicy().hasHeightForWidth())
        Export.setSizePolicy(sizePolicy)
        Export.setMinimumSize(QSize(0, 0))
        Export.setBaseSize(QSize(400, 280))
        self.verticalLayoutWidget = QWidget(Export)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 19, 371, 251))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.dataComboBox = QComboBox(self.verticalLayoutWidget)
        self.dataComboBox.addItem("")
        self.dataComboBox.addItem("")
        self.dataComboBox.addItem("")
        self.dataComboBox.setObjectName(u"dataComboBox")

        self.verticalLayout.addWidget(self.dataComboBox)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.startComboBox = QComboBox(self.verticalLayoutWidget)
        self.startComboBox.addItem("")
        self.startComboBox.addItem("")
        self.startComboBox.addItem("")
        self.startComboBox.addItem("")
        self.startComboBox.setObjectName(u"startComboBox")

        self.verticalLayout.addWidget(self.startComboBox)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.endComboBox = QComboBox(self.verticalLayoutWidget)
        self.endComboBox.addItem("")
        self.endComboBox.addItem("")
        self.endComboBox.addItem("")
        self.endComboBox.addItem("")
        self.endComboBox.setObjectName(u"endComboBox")

        self.verticalLayout.addWidget(self.endComboBox)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Export)
        self.buttonBox.accepted.connect(Export.accept)
        self.buttonBox.rejected.connect(Export.reject)

        self.dataComboBox.setCurrentIndex(2)
        self.startComboBox.setCurrentIndex(2)
        self.endComboBox.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Export)
    # setupUi

    def retranslateUi(self, Export):
        Export.setWindowTitle(QCoreApplication.translate("Export", u"Export", None))
        self.label.setText(QCoreApplication.translate("Export", u"Considered Data:", None))
        self.dataComboBox.setItemText(0, QCoreApplication.translate("Export", u"Householding", None))
        self.dataComboBox.setItemText(1, QCoreApplication.translate("Export", u"Measurement", None))
        self.dataComboBox.setItemText(2, QCoreApplication.translate("Export", u"Full Dataset", None))

        self.label_2.setText(QCoreApplication.translate("Export", u"Starting Point", None))
        self.startComboBox.setItemText(0, QCoreApplication.translate("Export", u"System Power", None))
        self.startComboBox.setItemText(1, QCoreApplication.translate("Export", u"Lift Off", None))
        self.startComboBox.setItemText(2, QCoreApplication.translate("Export", u"Start Of Experiment", None))
        self.startComboBox.setItemText(3, QCoreApplication.translate("Export", u"End Of Experiment", None))

        self.label_3.setText(QCoreApplication.translate("Export", u"Ending Point", None))
        self.endComboBox.setItemText(0, QCoreApplication.translate("Export", u"Lift Off", None))
        self.endComboBox.setItemText(1, QCoreApplication.translate("Export", u"Start Of Experiment", None))
        self.endComboBox.setItemText(2, QCoreApplication.translate("Export", u"End Of Experiment", None))
        self.endComboBox.setItemText(3, QCoreApplication.translate("Export", u"System Shutdown", None))

    # retranslateUi

