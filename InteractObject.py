from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import sys


class InteractObj(QObject):
    # web端会监听到这个信号
    SigSendMessageToJS = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, msg):
        # 在命令行打印相关消息
        print(__file__, sys._getframe().f_lineno, 'Msg from web: %s' % msg)

    @pyqtSlot(result=str)
    def fun(self):
        print(__file__, self.fun.__name__)
        # 将结果返回给js
        return 'The response from Qt'
