from gui import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
import sys
import os, subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsOpacityEffect, QMessageBox
from queue import Queue


class GuiConsts:
    base_directory_path = os.getcwd()
    admin_commands_path = '../commands_scripts/Admin_commands'
    system_commands_path = '../commands_scripts/System_commands'
    shell_commands_path = '../commands_scripts/shell_commands'


class WriteStream(object):
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)


class GUI():
    def __init__(self):
        self.registers_path_isChoose = False
        self.registers_path = False

        self.QMessageBox_toSave = -1

        self.op = QGraphicsOpacityEffect()

        self.app = QApplication(sys.argv)  # open application
        self.win = QMainWindow()  # will open the  window

        # self.win = Windows()
        self.app.setActiveWindow(self.win)

        # m = QtGui.QWidget()
        self.ex = Ui_MainWindow()  # all the params in Ui_MainWindow (at gui.py file)
        self.ex.widget = QWidget()
        self.ex.setupUi(self.win)  # put all this into win

    def showAndExit(self):
        #        self.win.showFullScreen()
        self.win.show()  # show win
        # logger.write ("[waiting for exit]")

        self.app.exec_()

        subprocess.Popen("taskkill /PID " + str(os.getpid()) + " /F ")

    def appendText(self, text):
        try:

            if(len(text) == 2):
                eval("self.ex." + str(text[0]))(text[1])
            else:
                eval("self.ex." + str(text[0]))

        except Exception as err:
            print(err)

class ReceiveLog(QObject):
    mySignal = pyqtSignal(list)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mySignal.emit(text)

gui = GUI()

queue = Queue()
WriteStream = WriteStream(queue)

thread_log = QThread()
my_rec_log = ReceiveLog(queue)
my_rec_log.mySignal.connect(gui.appendText)
my_rec_log.moveToThread(thread_log)
thread_log.started.connect(my_rec_log.run)
gui.main_thread = thread_log
thread_log.start()

