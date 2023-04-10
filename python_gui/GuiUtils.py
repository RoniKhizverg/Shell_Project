import os
import subprocess

from header import GuiConsts, WriteStream
def change_working_directory(dir_path):
    if not GuiConsts.base_directory_path.endswith(dir_path.replace('../', '')):
        os.chdir(os.path.join(GuiConsts.base_directory_path, dir_path))


