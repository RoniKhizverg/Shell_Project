import os
from _curses_panel import error

from PyQt5.QtWidgets import QPushButton, QFileDialog

from GuiUtils import change_working_directory
from header import *

import threading
import getpass

user_pass = getpass.getpass();

class Configurations:
    def __init__(self):
        gui.ex.tabWidget_5.setCurrentIndex(0)


class Login:
    def __init__(self):
        self.user = getpass.getuser()
        self.password = user_pass

    def loginAction(self):
        if  gui.ex.lineEdit_username_3.text() == self.user and gui.ex.lineEdit_password_3.text() == self.password:
            gui.ex.lineEdit_username_3.setDisabled(True)
            gui.ex.lineEdit_password_3.setDisabled(True)
            gui.ex.pushButton_login.setDisabled(True)

            gui.ex.tabWidget_2.setEnabled(True)
            gui.ex.tabWidget_5.setCurrentIndex(1)


#####_________System commands________#########
class Df:
    def __init__(self):
        pass

    def dfAction(self):
        change_working_directory(GuiConsts.system_commands_path)
        if gui.ex.comboBox_df.currentText() == 'df -h':
            exe_command = './mydf.pl -h'
        else:
            exe_command = './mydf.pl'
        output = os.popen(exe_command).read()
        WriteStream.write(
            ["textBrowser_terminal_df.append", "" + str(output)])


class Top:
    def __init__(self):
        self.process = None
        self.isStarted = True

    def top_action(self):
        self.isStarted = True
        change_working_directory(GuiConsts.system_commands_path)
        exe_command = './mytop.pl'
        self.process = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while self.isStarted:
            output = self.process.stdout.readline().decode('utf-8')
            if output == '' and self.process.poll() is not None:
                break
            if output:
                WriteStream.write(
                    ["textBrowser_terminal_top.append", "" + str(output)])
        self.process.wait()

    def stop_top_action(self):
        self.isStarted = False


class Ps:
    def __init__(self):
        pass

    def psAction(self):
        change_working_directory(GuiConsts.system_commands_path)
        if gui.ex.comboBox_ps.currentText() == 'ps':
            exe_command = './myps.pl'
        elif gui.ex.comboBox_ps.currentText() == 'ps -e':
            exe_command = './myps.pl -e'
        elif gui.ex.comboBox_ps.currentText() == 'ps -ef':
            exe_command = './myps.pl -ef'
        output = os.popen(exe_command).read()
        WriteStream.write(
            ["textBrowser_terminal_ps.append", "" + str(output)])


class Kill:
    def __init__(self):
        pass

    def killAction(self):
        change_working_directory(GuiConsts.system_commands_path)
        pid = gui.ex.lineEdit_process_id_kill.text()
        exe_command = ['./mykill.pl', pid]
        output, error = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if output:
            WriteStream.write(
                ["textBrowser_terminal_kill.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_kill.append", "" + error.decode()])


#####_________Shell commands________#########

class Ls:
    def __init__(self):
        super().__init__()

    def select_dir(self):
        dir_name = QFileDialog.getExistingDirectory(None, 'Select directory')

        if dir_name:
            print(f'Selected file: {dir_name}')
            WriteStream.write(
                ["lineEdit_loadfile_ls.setText", "" + dir_name])


    def ls_action(self):
        change_working_directory(GuiConsts.shell_commands_path)

        exe_command = ['./myls.pl']

        if gui.ex.comboBox_ls.currentText() == 'ls -l':
            exe_command.append("-l")
        if gui.ex.comboBox_ls.currentText() == 'ls -a':
            exe_command.append("-a")
        if gui.ex.comboBox_ls.currentText() == 'ls -r':
            exe_command.append("-r")


        exe_command.append(gui.ex.lineEdit_loadfile_ls.text())
        print(str(exe_command))
        output, error = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


        if output:
            WriteStream.write(
                ["textBrowser_terminal_ls.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_ls.append", "" + error.decode()])

class Cp:
    def __init__(self):
        super().__init__()

    def select_dir(self):
        dir_name = QFileDialog.getExistingDirectory(None, 'Select directory')

        if dir_name:
            print(f'Selected file: {dir_name}')
            WriteStream.write(
                ["lineEdit_choose_dest_cp.setText", "" + dir_name])

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Select file')

        if file_name:
            print(f'Selected file: {file_name}')
            WriteStream.write(
                ["lineEdit_choose_file_cp.setText", "" + file_name])

    def cp_action(self):
        change_working_directory(GuiConsts.shell_commands_path)

        exe_command = ['./mycp.pl']
        exe_command.append(gui.ex.lineEdit_choose_file_cp.text())
        arr = (gui.ex.lineEdit_choose_file_cp.text()).split('/')
        file_name = ((arr[len(arr)-1]).split('.'))[0]

        exe_command.append(gui.ex.lineEdit_choose_dest_cp.text() +'/' + file_name + '_copy.txt')

        output, error = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if output:
            WriteStream.write(
                ["textBrowser_terminal_cp.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_cp.append", "" + error.decode()])

class Ln:
    def __init__(self):
        super().__init__()

    def select_dir(self):
        dir_name = QFileDialog.getExistingDirectory(None, 'Select directory')

        if dir_name:
            print(f'Selected file: {dir_name}')
            WriteStream.write(
                ["lineEdit_choose_dest_ln.setText", "" + dir_name])

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Select file')

        if file_name:
            print(f'Selected file: {file_name}')
            WriteStream.write(
                ["lineEdit_choose_file_ln.setText", "" + file_name])

    def ln_action(self):
        change_working_directory(GuiConsts.shell_commands_path)

        exe_command = ['./myln.pl']
        exe_command.append(gui.ex.lineEdit_choose_file_ln.text())
        arr = (gui.ex.lineEdit_choose_file_ln.text()).split('/')
        file_name = ((arr[len(arr) - 1]).split('.'))[0]

        exe_command.append(gui.ex.lineEdit_choose_dest_ln.text() + '/' + file_name + '_hardLink.txt')

        output, error = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if output:
            WriteStream.write(
                ["textBrowser_terminal_ln.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_ln.append", "" + error.decode()])

class Mv:
    def __init__(self):
        super().__init__()

    def select_dir(self):
        dir_name = QFileDialog.getExistingDirectory(None, 'Select directory')

        if dir_name:
            print(f'Selected file: {dir_name}')
            WriteStream.write(
                ["lineEdit_choose_dest_mv.setText", "" + dir_name])

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Select file')

        if file_name:
            print(f'Selected file: {file_name}')
            WriteStream.write(
                ["lineEdit_choose_file_mv.setText", "" + file_name])

    def mv_action(self):
        change_working_directory(GuiConsts.shell_commands_path)

        exe_command = ['./mymv.pl']
        exe_command.append(gui.ex.lineEdit_choose_file_mv.text())
        arr = (gui.ex.lineEdit_choose_file_mv.text()).split('/')
        file_name = arr[len(arr) - 1]

        exe_command.append(gui.ex.lineEdit_choose_dest_mv.text() + '/' + file_name)

        output, error = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if output:
            WriteStream.write(
                ["textBrowser_terminal_mv.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_mv.append", "" + error.decode()])

class Wc:
    def __init__(self):
        super().__init__()

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Select file')

        if file_name:
            print(f'Selected file: {file_name}')
            WriteStream.write(
                ["lineEdit_loadfile_wc.setText", "" + file_name])

    def wc_action(self):
        change_working_directory(GuiConsts.shell_commands_path)

        exe_command = ['./mywc.pl', gui.ex.lineEdit_loadfile_wc.text()]

        output, error = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if output:
            WriteStream.write(
                ["textBrowser_terminal_wc.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_wc.append", "" + error.decode()])

#####_________Admin commands________#########


class Chmod:
    def __init__(self):
        super().__init__()

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Select file')

        if file_name:
            print(f'Selected file: {file_name}')
            WriteStream.write(
                ["lineEdit_loadfile_chmod.setText", "" + file_name])


    def chmod_action(self):
        change_working_directory(GuiConsts.admin_commands_path)
        type_of_user = ''
        exe_command = ['./mychmod.pl']


        if gui.ex.comboBox_chmod.currentText() == 'chmod -u':
            type_of_user = "u"
        if gui.ex.comboBox_chmod.currentText() == 'chmod -g':
            type_of_user = "g"
        if gui.ex.comboBox_chmod.currentText() == 'chmod -o':
            type_of_user = "o"

        if gui.ex.checkBox_add_read_chmod.isChecked() or gui.ex.checkBox_add_write_chmod.isChecked() or gui.ex.checkBox_add_execute_chmod.isChecked():
            command_to_exex_add = type_of_user
            command_to_exex_add += "+"
            if gui.ex.checkBox_add_read_chmod.isChecked():
                command_to_exex_add += "r"
            if gui.ex.checkBox_add_write_chmod.isChecked():
                command_to_exex_add += "w"
            if gui.ex.checkBox_add_execute_chmod.isChecked():
                command_to_exex_add += "x"
            exe_command.append(command_to_exex_add)

        if gui.ex.checkBox_remove_read_chmod.isChecked() or gui.ex.checkBox_remove_write_chmod.isChecked() or gui.ex.checkBox_remove_execute_chmod.isChecked():
            command_to_exex_remove = type_of_user
            command_to_exex_remove += "-"
            if gui.ex.checkBox_remove_read_chmod.isChecked():
                command_to_exex_remove += "r"
            if gui.ex.checkBox_remove_write_chmod.isChecked():
                command_to_exex_remove += "w"
            if gui.ex.checkBox_remove_execute_chmod.isChecked():
                command_to_exex_remove += "x"
            exe_command.append(command_to_exex_remove)

        exe_command.append(gui.ex.lineEdit_loadfile_chmod.text())
        print(str(exe_command))

        output, error = subprocess.Popen(exe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if output:
            WriteStream.write(
                ["textBrowser_terminal_chmod.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_chmod.append", "" + error.decode()])


class AddUser:
    def __init__(self):
        self.password = user_pass

    def add_user_action(self):
        change_working_directory(GuiConsts.admin_commands_path)
        user_name = gui.ex.lineEdit_username.text()
        exe_command = ['sudo', '-S', './myadduser.pl', user_name]
        process = subprocess.Popen(exe_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(input=self.password.encode())

        if output:
            WriteStream.write(
                ["textBrowser_terminal_addUser.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_addUser.append", "" + error.decode()])


class Chown:
    def __init__(self):
        self.password = user_pass

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Select file')

        if file_name:
            print(f'Selected file: {file_name}')
            WriteStream.write(
                ["lineEdit_loadfile_chown.setText", "" + file_name])

    def chown_user_action(self):
        change_working_directory(GuiConsts.admin_commands_path)
        user_name = gui.ex.lineEdit_username_chown.text()
        file_path = gui.ex.lineEdit_loadfile_chown.text()
        exe_command = ['sudo', '-S', './mychown.pl', user_name, file_path]
        process = subprocess.Popen(exe_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(input=self.password.encode())
        print(str(exe_command))


        if output:
            WriteStream.write(
                ["textBrowser_terminal_chown_user.append", "" + output.decode()])
        if error:
            WriteStream.write(
                ["textBrowser_terminal_chown_user.append", "" + error.decode()])



class Signals:
    def __init__(self):
        # Login
        gui.ex.pushButton_login.clicked.connect(lambda: threading.Thread(target=login.loginAction).start())

        # Df
        gui.ex.pushButton_run_df.clicked.connect(lambda: threading.Thread(target=df.dfAction).start())

        # Top
        gui.ex.pushButton_run_top.clicked.connect(lambda: threading.Thread(target=top.top_action).start())
        gui.ex.pushButton_stop_top.clicked.connect(lambda: threading.Thread(target=top.stop_top_action).start())

        # ps
        gui.ex.pushButton_run_ps.clicked.connect(lambda: threading.Thread(target=ps.psAction).start())

        # Kill
        gui.ex.pushButton_run_kill.clicked.connect(lambda: threading.Thread(target=kill.killAction).start())

        # ls
        gui.ex.pushButton_load_ls.clicked.connect(lambda: threading.Thread(target=ls.select_dir()).start())
        gui.ex.pushButton_run_ls.clicked.connect(lambda: threading.Thread(target=ls.ls_action()).start())

        # cp
        gui.ex.pushButton_load_file_cp.clicked.connect(lambda: threading.Thread(target=cp.select_file).start())
        gui.ex.pushButton_load_dest_cp.clicked.connect(lambda: threading.Thread(target=cp.select_dir()).start())
        gui.ex.pushButton_run_cp.clicked.connect(lambda: threading.Thread(target=cp.cp_action()).start())

        # ln
        gui.ex.pushButton_load_file_ln.clicked.connect(lambda: threading.Thread(target=ln.select_file).start())
        gui.ex.pushButton_load_dest_ln.clicked.connect(lambda: threading.Thread(target=ln.select_dir()).start())
        gui.ex.pushButton_run_ln.clicked.connect(lambda: threading.Thread(target=ln.ln_action()).start())

        # mv
        gui.ex.pushButton_load_file_mv.clicked.connect(lambda: threading.Thread(target=mv.select_file).start())
        gui.ex.pushButton_load_dest_mv.clicked.connect(lambda: threading.Thread(target=mv.select_dir()).start())
        gui.ex.pushButton_run_mv.clicked.connect(lambda: threading.Thread(target=mv.mv_action()).start())

        # wc
        gui.ex.pushButton_load_wc.clicked.connect(lambda: threading.Thread(target=wc.select_file).start())
        gui.ex.pushButton_run_wc.clicked.connect(lambda: threading.Thread(target=wc.wc_action).start())

        # chmod
        gui.ex.pushButton_load_chmod.clicked.connect(lambda: threading.Thread(target=chmod.select_file()).start())
        gui.ex.pushButton_run_chmod.clicked.connect(lambda: threading.Thread(target=chmod.chmod_action()).start())

        # add user
        gui.ex.pushButton_add_user.clicked.connect(lambda: threading.Thread(target=add_user.add_user_action).start())

        # chown
        gui.ex.pushButton_load_chown.clicked.connect(lambda: threading.Thread(target=chown.select_file).start())
        gui.ex.pushButton_chown_user.clicked.connect(lambda: threading.Thread(target=chown.chown_user_action).start())





if __name__ == '__main__':
    configurations = Configurations()
    login = Login()
    df = Df()
    top = Top()
    ps = Ps()
    kill = Kill()
    ls = Ls()
    cp = Cp()
    ln = Ln()
    mv = Mv()
    wc = Wc()
    chmod = Chmod()
    add_user = AddUser()
    chown = Chown()
    signals = Signals()
    gui.showAndExit()
