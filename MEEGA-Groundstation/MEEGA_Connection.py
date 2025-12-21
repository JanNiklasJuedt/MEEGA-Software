# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_connection.ui'
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
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        if not ConnectionDialog.objectName():
            ConnectionDialog.setObjectName(u"ConnectionDialog")
        ConnectionDialog.resize(400, 172)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConnectionDialog.sizePolicy().hasHeightForWidth())
        ConnectionDialog.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        ConnectionDialog.setFont(font)
        self.verticalLayout = QVBoxLayout(ConnectionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.label_2 = QLabel(ConnectionDialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(ConnectionDialog)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.ConnectorBox = QComboBox(ConnectionDialog)
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.addItem("")
        self.ConnectorBox.setObjectName(u"ConnectorBox")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.ConnectorBox)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ConnectionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        font1 = QFont()
        font1.setPointSize(9)
        self.buttonBox.setFont(font1)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ConnectionDialog)
        self.buttonBox.accepted.connect(ConnectionDialog.accept)
        self.buttonBox.rejected.connect(ConnectionDialog.reject)

        self.ConnectorBox.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(ConnectionDialog)
    # setupUi

    def retranslateUi(self, ConnectionDialog):
        ConnectionDialog.setWindowTitle(QCoreApplication.translate("ConnectionDialog", u"MEEGA - Connection", None))
        self.label_2.setText(QCoreApplication.translate("ConnectionDialog", u"Serial Port (RS-232)", None))
        self.label.setText(QCoreApplication.translate("ConnectionDialog", u"Connector", None))
        self.ConnectorBox.setItemText(0, QCoreApplication.translate("ConnectionDialog", u"COM1", None))
        self.ConnectorBox.setItemText(1, QCoreApplication.translate("ConnectionDialog", u"COM2", None))
        self.ConnectorBox.setItemText(2, QCoreApplication.translate("ConnectionDialog", u"COM3", None))
        self.ConnectorBox.setItemText(3, QCoreApplication.translate("ConnectionDialog", u"COM4", None))
        self.ConnectorBox.setItemText(4, QCoreApplication.translate("ConnectionDialog", u"COM5", None))
        self.ConnectorBox.setItemText(5, QCoreApplication.translate("ConnectionDialog", u"COM6", None))
        self.ConnectorBox.setItemText(6, QCoreApplication.translate("ConnectionDialog", u"COM7", None))
        self.ConnectorBox.setItemText(7, QCoreApplication.translate("ConnectionDialog", u"COM8", None))
        self.ConnectorBox.setItemText(8, QCoreApplication.translate("ConnectionDialog", u"COM9", None))

    # retranslateUi

