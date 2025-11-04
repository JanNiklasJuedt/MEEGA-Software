# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_error.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_ErrorDialog(object):
    def setupUi(self, ErrorDialog):
        if not ErrorDialog.objectName():
            ErrorDialog.setObjectName(u"ErrorDialog")
        ErrorDialog.resize(400, 100)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ErrorDialog.sizePolicy().hasHeightForWidth())
        ErrorDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ErrorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.Error = QLabel(ErrorDialog)
        self.Error.setObjectName(u"Error")
        self.Error.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.Error)

        self.buttonBox = QDialogButtonBox(ErrorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ErrorDialog)
        self.buttonBox.accepted.connect(ErrorDialog.accept)
        self.buttonBox.rejected.connect(ErrorDialog.reject)

        QMetaObject.connectSlotsByName(ErrorDialog)
    # setupUi

    def retranslateUi(self, ErrorDialog):
        ErrorDialog.setWindowTitle(QCoreApplication.translate("ErrorDialog", u"MEEGA - Error", None))
        self.Error.setText(QCoreApplication.translate("ErrorDialog", u"UH OH Something went wrong!", None))
    # retranslateUi

