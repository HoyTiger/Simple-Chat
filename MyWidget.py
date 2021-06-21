import socket
import sys
import threading
from PyQt5 import QtWidgets
from chatUI import Ui_Form
import time

class MyWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setupUi(self)

        self.btn_send_msg.clicked.connect(self.send_message)
        self.setWindowTitle("简易聊天程序-客户端")
        # self.local = '127.0.0.1'
        # self.port = 8500
        # self.flag = False

    flag = False
    port = 8500
    local = '127.0.0.1'
    global cientSock

    def send_message(self):

        message = self.txtEd_send_msg.toPlainText()

        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.txtBr_rsv_messaqe.append("客户端<"+timeNow+">:")
        self.txtBr_rsv_messaqe.append(" "+message)

        if self.flag==True:
            self.cientSock.send(message.encode())
        else:
            self.txtBr_rsv_messaqe.append("您还未与服务器端建立连接，客户端无法接受您的消息\n")

        self.txtEd_send_msg.clear()

    def receive_msg(self):
        try:
            self.cientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cientSock.connect((self.local, self.port))
            self.flag = True

        except:
            self.flag = False
            self.txtBr_rsv_messaqe.append('与服务器建立连接失败，请检查服务器是否已经启动....')
            return

        self.buffer = 1024
        self.cientSock.send("Y".encode())
        while True:
            try:
                if self.flag == True:
                    self.serverMsg = self.cientSock.recv(self.buffer).decode('utf-8')
                    if not self.serverMsg:
                        continue
                    elif self.serverMsg == "Y":
                        self.txtBr_rsv_messaqe.append('服务器已与客户端建立连接......\n')
                    elif self.serverMsg == "N":
                        self.txtBr_rsv_messaqe.append('服务器与客户端建立连接失败......\n')

                    else:
                        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        self.txtBr_rsv_messaqe.append("服务器端<" + timeNow + ">:")
                        self.txtBr_rsv_messaqe.append(" " + self.serverMsg)
                else:
                    break
            except EOFError as msg:
                raise msg
                self.cientSock.close()
                break


    def startNewThread(self):
        thread = threading.Thread(target=self.receive_msg, args=())
        thread.start()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.startNewThread()
    widget.show()
    sys.exit(app.exec_())



