# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_time.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QSizePolicy, QSpacerItem,
    QTimeEdit, QVBoxLayout, QWidget)

class Ui_LaunchTimeDialog(object):
    def setupUi(self, LaunchTimeDialog):
        if not LaunchTimeDialog.objectName():
            LaunchTimeDialog.setObjectName(u"LaunchTimeDialog")
        LaunchTimeDialog.resize(400, 125)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LaunchTimeDialog.sizePolicy().hasHeightForWidth())
        LaunchTimeDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(LaunchTimeDialog)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.launchTimeEdit = QTimeEdit(LaunchTimeDialog)
        self.launchTimeEdit.setObjectName(u"launchTimeEdit")
        font = QFont()
        font.setPointSize(12)
        self.launchTimeEdit.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.launchTimeEdit)

        self.launchTimeLabel = QLabel(LaunchTimeDialog)
        self.launchTimeLabel.setObjectName(u"launchTimeLabel")
        self.launchTimeLabel.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.launchTimeLabel)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(LaunchTimeDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(LaunchTimeDialog)
        self.buttonBox.accepted.connect(LaunchTimeDialog.accept)
        self.buttonBox.rejected.connect(LaunchTimeDialog.reject)

        QMetaObject.connectSlotsByName(LaunchTimeDialog)
    # setupUi

    def retranslateUi(self, LaunchTimeDialog):
        LaunchTimeDialog.setWindowTitle(QCoreApplication.translate("LaunchTimeDialog", u"MEEGA - ELT", None))
        self.launchTimeEdit.setDisplayFormat(QCoreApplication.translate("LaunchTimeDialog", u"HH:mm:ss", None))
        self.launchTimeLabel.setText(QCoreApplication.translate("LaunchTimeDialog", u"Estimated Launch Time", None))
    # retranslateUi

