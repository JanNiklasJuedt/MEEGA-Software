# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_startup.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateTimeEdit,
    QDialog, QDialogButtonBox, QFormLayout, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QTimeEdit, QToolButton, QWidget)

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        if not StartDialog.objectName():
            StartDialog.setObjectName(u"StartDialog")
        StartDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        StartDialog.setEnabled(True)
        StartDialog.resize(386, 314)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StartDialog.sizePolicy().hasHeightForWidth())
        StartDialog.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        StartDialog.setFont(font)
        StartDialog.setLocale(QLocale(QLocale.English, QLocale.Germany))
        StartDialog.setSizeGripEnabled(False)
        StartDialog.setModal(True)
        self.gridLayout = QGridLayout(StartDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonBox = QDialogButtonBox(StartDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(9)
        self.buttonBox.setFont(font1)
        self.buttonBox.setLocale(QLocale(QLocale.English, QLocale.Germany))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.modeLabel = QLabel(StartDialog)
        self.modeLabel.setObjectName(u"modeLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.modeLabel)

        self.modeComboBox = QComboBox(StartDialog)
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.setObjectName(u"modeComboBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.modeComboBox)

        self.connectionLabel = QLabel(StartDialog)
        self.connectionLabel.setObjectName(u"connectionLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.connectionLabel)

        self.connectionComboBox = QComboBox(StartDialog)
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.setObjectName(u"connectionComboBox")
        self.connectionComboBox.setEnabled(True)
        self.connectionComboBox.setEditable(False)
        self.connectionComboBox.setFrame(True)
        self.connectionComboBox.setModelColumn(0)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.connectionComboBox)

        self.saveFileLabel = QLabel(StartDialog)
        self.saveFileLabel.setObjectName(u"saveFileLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.saveFileLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.saveFileEdit = QLineEdit(StartDialog)
        self.saveFileEdit.setObjectName(u"saveFileEdit")

        self.horizontalLayout_3.addWidget(self.saveFileEdit)

        self.saveFileButton = QToolButton(StartDialog)
        self.saveFileButton.setObjectName(u"saveFileButton")
        self.saveFileButton.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout_3.addWidget(self.saveFileButton)


        self.formLayout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)

        self.languageLabel = QLabel(StartDialog)
        self.languageLabel.setObjectName(u"languageLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.languageLabel)

        self.languageComboBox = QComboBox(StartDialog)
        self.languageComboBox.addItem(u"English")
        self.languageComboBox.addItem(u"Deutsch")
        self.languageComboBox.setObjectName(u"languageComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.languageComboBox)

        self.launchTimeLabel = QLabel(StartDialog)
        self.launchTimeLabel.setObjectName(u"launchTimeLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.launchTimeLabel)

        self.launchTimeTimeEdit = QTimeEdit(StartDialog)
        self.launchTimeTimeEdit.setObjectName(u"launchTimeTimeEdit")
        self.launchTimeTimeEdit.setCurrentSection(QDateTimeEdit.Section.HourSection)
        self.launchTimeTimeEdit.setTimeSpec(Qt.TimeSpec.LocalTime)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.launchTimeTimeEdit)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)


        self.retranslateUi(StartDialog)
        self.buttonBox.rejected.connect(StartDialog.reject)
        self.buttonBox.accepted.connect(StartDialog.accept)

        self.connectionComboBox.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(StartDialog)
    # setupUi

    def retranslateUi(self, StartDialog):
        StartDialog.setWindowTitle(QCoreApplication.translate("StartDialog", u"MEEGA - Start", None))
        self.modeLabel.setText(QCoreApplication.translate("StartDialog", u"Mode", None))
        self.modeComboBox.setItemText(0, QCoreApplication.translate("StartDialog", u"Test Mode", None))
        self.modeComboBox.setItemText(1, QCoreApplication.translate("StartDialog", u"Flight Mode", None))

        self.connectionLabel.setText(QCoreApplication.translate("StartDialog", u"Connector", None))
        self.connectionComboBox.setItemText(0, QCoreApplication.translate("StartDialog", u"COM1", None))
        self.connectionComboBox.setItemText(1, QCoreApplication.translate("StartDialog", u"COM2", None))
        self.connectionComboBox.setItemText(2, QCoreApplication.translate("StartDialog", u"COM3", None))
        self.connectionComboBox.setItemText(3, QCoreApplication.translate("StartDialog", u"COM4", None))
        self.connectionComboBox.setItemText(4, QCoreApplication.translate("StartDialog", u"COM5", None))
        self.connectionComboBox.setItemText(5, QCoreApplication.translate("StartDialog", u"COM6", None))
        self.connectionComboBox.setItemText(6, QCoreApplication.translate("StartDialog", u"COM7", None))
        self.connectionComboBox.setItemText(7, QCoreApplication.translate("StartDialog", u"COM8", None))
        self.connectionComboBox.setItemText(8, QCoreApplication.translate("StartDialog", u"COM9", None))

        self.saveFileLabel.setText(QCoreApplication.translate("StartDialog", u"Save File", None))
        self.saveFileEdit.setText(QCoreApplication.translate("StartDialog", u"*\\default.meega", None))
        self.saveFileButton.setText(QCoreApplication.translate("StartDialog", u"...", None))
        self.languageLabel.setText(QCoreApplication.translate("StartDialog", u"Language", None))

        self.launchTimeLabel.setText(QCoreApplication.translate("StartDialog", u"Launch Time", None))
        self.launchTimeTimeEdit.setDisplayFormat(QCoreApplication.translate("StartDialog", u"HH:mm:ss", None))
    # retranslateUi

