import socket
import sys
import threading
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread

from chatUI import Ui_Form
import time

class ServerWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(ServerWidget, self).__init__()
        self.setupUi(self)

        self.btn_send_msg.clicked.connect(self.send_message)
        self.setWindowTitle("简易聊天程序-服务器端")

        # self.local = '127.0.0.1'
        # self.port = 8500
        # self.flag = False

    flag = False
    port = 8500
    local = '127.0.0.1'
    global serverSock

    def send_message(self):

        message = self.txtEd_send_msg.toPlainText()

        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.txtBr_rsv_messaqe.append("服务器端<"+timeNow+">:")
        self.txtBr_rsv_messaqe.append(" "+message)

        if self.flag==True:
            self.connection.send(message.encode())
        else:
            self.txtBr_rsv_messaqe.append("您还为与客户端建立连接，客户端无法接受您的消息\n")

        self.txtEd_send_msg.clear()

    def receive_msg(self):
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind((self.local, self.port))
        self.serverSock.listen(15)

        self.buffer = 1024
        self.txtBr_rsv_messaqe.append('服务器已就绪......\n')

        while True:
            self.connection, self.address = self.serverSock.accept()
            self.flag = True
            while True:
                self.cientMsg = self.connection.recv(self.buffer).decode('utf-8')
                if not self.cientMsg:
                    continue
                elif self.cientMsg == "Y":
                    self.txtBr_rsv_messaqe.append('服务器已与客户端建立连接......\n')
                    self.connection.send(b'Y')
                elif self.cientMsg == "N":
                    self.txtBr_rsv_messaqe.append('服务器与客户端建立连接失败......\n')
                    self.connection.send(b'N')

                else:
                    timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    self.txtBr_rsv_messaqe.append("客户端端<" + timeNow + ">:")
                    self.txtBr_rsv_messaqe.append(" " + self.cientMsg)
    def startNewThread(self):
        thread = threading.Thread(target=self.receive_msg, args=())
        thread.start()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = ServerWidget()
    widget.startNewThread()
    widget.show()
    sys.exit(app.exec_())



