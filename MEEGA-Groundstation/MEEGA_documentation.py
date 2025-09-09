# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MEEGA_documentation.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QFrame,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Documentation(object):
    def setupUi(self, Documentation):
        if not Documentation.objectName():
            Documentation.setObjectName(u"Documentation")
        Documentation.resize(600, 600)
        self.verticalLayout = QVBoxLayout(Documentation)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.textBrowser = QTextBrowser(Documentation)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout.addWidget(self.textBrowser)

        self.buttonBox = QDialogButtonBox(Documentation)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Documentation)

        QMetaObject.connectSlotsByName(Documentation)
    # setupUi

    def retranslateUi(self, Documentation):
        Documentation.setWindowTitle(QCoreApplication.translate("Documentation", u"MEEGA - Documentation", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Documentation", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textBrowser.setPlaceholderText(QCoreApplication.translate("Documentation", u"Sieht aus als h\u00e4tte etwas nicht geklappt :/", None))
    # retranslateUi

