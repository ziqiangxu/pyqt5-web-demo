# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtCore import QUrl, pyqtSignal
from InteractObject import InteractObj


class MainWindow(QWidget):
    SigSendMessageToJS = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # ---Qt widget and layout---
        # 创建Qt控件
        self.mpQtSendLineEdit = QLineEdit("输入要发送的内容")

        self.btn_send_msg_by_obj = QPushButton('send msg by obj')

        self.btn_run_js = QPushButton('run js')

        self.pQtTotalVLayout = QVBoxLayout()
        self.pQtTotalVLayout.addWidget(self.mpQtSendLineEdit)
        self.pQtTotalVLayout.addWidget(self.btn_send_msg_by_obj)
        self.pQtTotalVLayout.addWidget(self.btn_run_js)

        self.pQtGroup = QGroupBox('Qt View', self)
        self.pQtGroup.setLayout(self.pQtTotalVLayout)

        # ---Web widget and layout---
        # 创建web view
        self.mpJSWebView = QWebEngineView(self)
        self.pWebChannel = QWebChannel(self.mpJSWebView.page())
        self.pInteractObj = InteractObj(self)
        self.pWebChannel.registerObject("interactObj", self.pInteractObj)
        self.mpJSWebView.page().setWebChannel(self.pWebChannel)
        # 设置页面
        self.url = 'file:///home/xu/PycharmProjects/pyqtweb/JSTest.html'
        # self.url = 'http://www.baidu.com'
        self.mpJSWebView.page().load(QUrl(self.url))

        self.pJSTotalVLayout = QVBoxLayout()
        self.pJSTotalVLayout.addWidget(self.mpJSWebView)
        self.pWebGroup = QGroupBox('Web View', self)
        self.pWebGroup.setLayout(self.pJSTotalVLayout)

        # ---TMainWindow total layout---
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.pQtGroup, 2)
        self.mainLayout.addWidget(self.pWebGroup, 5)
        self.setLayout(self.mainLayout)

        self.showMaximized()
        self.signal_slot()

    def signal_slot(self):
        self.btn_send_msg_by_obj.clicked.connect(self.send_msg_by_obj)
        self.btn_run_js.clicked.connect(self.run_js)

    def send_msg_by_obj(self):
        """
        通过Object对象来发送参数，这个需要在网页进行绑定
        :return:
        """
        msg = self.mpQtSendLineEdit.text()
        self.pInteractObj.SigSendMessageToJS.emit(msg)

    def run_js(self):
        """
        通过直接调用js代码来发送参数，执行代码
        :return:
        """
        msg = self.mpQtSendLineEdit.text()
        msg = 'Received string from Qt:' + msg
        self.mpJSWebView.page().runJavaScript("output('%s');" % msg)
        self.mpJSWebView.page().runJavaScript("showAlert('%s');" % msg)

        # 也可以直接传入一段js代码
        # self.mpJSWebView.page().runJavaScript("function test() { return document.cookie }")
        # self.mpJSWebView.page().runJavaScript("test();", self.callback)

    @staticmethod
    def callback(res):
        print("result:", res)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dlg = MainWindow()
    dlg.show()

    app.exec_()
