# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_connection.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
    QDialogButtonBox, QFormLayout, QFrame, QLabel,
    QRadioButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        if not ConnectionDialog.objectName():
            ConnectionDialog.setObjectName(u"ConnectionDialog")
        ConnectionDialog.resize(400, 300)
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
        self.TCP_Button = QRadioButton(ConnectionDialog)
        self.TCP_Button.setObjectName(u"TCP_Button")

        self.verticalLayout.addWidget(self.TCP_Button)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.label_2 = QLabel(ConnectionDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.label_3 = QLabel(ConnectionDialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.PortEdit = QTextEdit(ConnectionDialog)
        self.PortEdit.setObjectName(u"PortEdit")
        self.PortEdit.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PortEdit.sizePolicy().hasHeightForWidth())
        self.PortEdit.setSizePolicy(sizePolicy1)
        self.PortEdit.setMinimumSize(QSize(0, 28))
        self.PortEdit.setMaximumSize(QSize(16777215, 28))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.PortEdit)

        self.IPEdit = QTextEdit(ConnectionDialog)
        self.IPEdit.setObjectName(u"IPEdit")
        sizePolicy1.setHeightForWidth(self.IPEdit.sizePolicy().hasHeightForWidth())
        self.IPEdit.setSizePolicy(sizePolicy1)
        self.IPEdit.setMinimumSize(QSize(0, 28))
        self.IPEdit.setMaximumSize(QSize(16777215, 28))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.IPEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.line = QFrame(ConnectionDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.RS_Button = QRadioButton(ConnectionDialog)
        self.RS_Button.setObjectName(u"RS_Button")
        self.RS_Button.setChecked(True)

        self.verticalLayout.addWidget(self.RS_Button)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(ConnectionDialog)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.ConnectorBox = QComboBox(ConnectionDialog)
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

        QMetaObject.connectSlotsByName(ConnectionDialog)
    # setupUi

    def retranslateUi(self, ConnectionDialog):
        ConnectionDialog.setWindowTitle(QCoreApplication.translate("ConnectionDialog", u"MEEGA - Connection", None))
        self.TCP_Button.setText(QCoreApplication.translate("ConnectionDialog", u"TCP (Ethernet)", None))
        self.label_2.setText(QCoreApplication.translate("ConnectionDialog", u"Port", None))
        self.label_3.setText(QCoreApplication.translate("ConnectionDialog", u"IP-Adress", None))
        self.RS_Button.setText(QCoreApplication.translate("ConnectionDialog", u"Serial Port (RS-232)", None))
        self.label.setText(QCoreApplication.translate("ConnectionDialog", u"Connector", None))
        self.ConnectorBox.setItemText(0, QCoreApplication.translate("ConnectionDialog", u"Port 1", None))
        self.ConnectorBox.setItemText(1, QCoreApplication.translate("ConnectionDialog", u"Port 2", None))

    # retranslateUi

