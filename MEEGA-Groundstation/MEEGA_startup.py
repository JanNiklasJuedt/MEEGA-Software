# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_startup.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QDialogButtonBox, QFormLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QToolButton, QWidget)

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        if not StartDialog.objectName():
            StartDialog.setObjectName(u"StartDialog")
        StartDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        StartDialog.setEnabled(True)
        StartDialog.resize(564, 271)
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
        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.verticalSpacer_2, 4, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

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
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 2, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.modeLabel = QLabel(StartDialog)
        self.modeLabel.setObjectName(u"modeLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.modeLabel)

        self.modeComboBox = QComboBox(StartDialog)
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.setObjectName(u"modeComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.modeComboBox)

        self.connectionLabel = QLabel(StartDialog)
        self.connectionLabel.setObjectName(u"connectionLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.connectionLabel)

        self.connectionComboBox = QComboBox(StartDialog)
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.addItem("")
        self.connectionComboBox.setObjectName(u"connectionComboBox")
        self.connectionComboBox.setEnabled(True)
        self.connectionComboBox.setEditable(False)
        self.connectionComboBox.setFrame(True)
        self.connectionComboBox.setModelColumn(0)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.connectionComboBox)

        self.saveFileLabel = QLabel(StartDialog)
        self.saveFileLabel.setObjectName(u"saveFileLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.saveFileLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.saveFileEdit = QLineEdit(StartDialog)
        self.saveFileEdit.setObjectName(u"saveFileEdit")

        self.horizontalLayout_3.addWidget(self.saveFileEdit)

        self.saveFileButton = QToolButton(StartDialog)
        self.saveFileButton.setObjectName(u"saveFileButton")
        self.saveFileButton.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout_3.addWidget(self.saveFileButton)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.languageLabel = QLabel(StartDialog)
        self.languageLabel.setObjectName(u"languageLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.languageLabel)

        self.languageComboBox = QComboBox(StartDialog)
        self.languageComboBox.addItem("")
        self.languageComboBox.addItem("")
        self.languageComboBox.setObjectName(u"languageComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.languageComboBox)


        self.gridLayout.addLayout(self.formLayout, 1, 1, 1, 1)


        self.retranslateUi(StartDialog)
        self.buttonBox.rejected.connect(StartDialog.reject)
        self.buttonBox.accepted.connect(StartDialog.accept)

        self.connectionComboBox.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(StartDialog)
    # setupUi

    def retranslateUi(self, StartDialog):
        StartDialog.setWindowTitle(QCoreApplication.translate("StartDialog", u"Groundstation Start", None))
        self.modeLabel.setText(QCoreApplication.translate("StartDialog", u"Mode", None))
        self.modeComboBox.setItemText(0, QCoreApplication.translate("StartDialog", u"Automatic", None))
        self.modeComboBox.setItemText(1, QCoreApplication.translate("StartDialog", u"Testing", None))
        self.modeComboBox.setItemText(2, QCoreApplication.translate("StartDialog", u"Recording", None))
        self.modeComboBox.setItemText(3, QCoreApplication.translate("StartDialog", u"Replaying", None))

        self.connectionLabel.setText(QCoreApplication.translate("StartDialog", u"Connection", None))
        self.connectionComboBox.setItemText(0, QCoreApplication.translate("StartDialog", u"Automatic", None))
        self.connectionComboBox.setItemText(1, QCoreApplication.translate("StartDialog", u"Try Once", None))
        self.connectionComboBox.setItemText(2, QCoreApplication.translate("StartDialog", u"Manual", None))
        self.connectionComboBox.setItemText(3, QCoreApplication.translate("StartDialog", u"None", None))

        self.saveFileLabel.setText(QCoreApplication.translate("StartDialog", u"Save File", None))
        self.saveFileEdit.setText(QCoreApplication.translate("StartDialog", u"*\\default.meega", None))
        self.saveFileButton.setText(QCoreApplication.translate("StartDialog", u"...", None))
        self.languageLabel.setText(QCoreApplication.translate("StartDialog", u"Language", None))
        self.languageComboBox.setItemText(0, QCoreApplication.translate("StartDialog", u"English", None))
        self.languageComboBox.setItemText(1, QCoreApplication.translate("StartDialog", u"Deutsch", None))

    # retranslateUi

