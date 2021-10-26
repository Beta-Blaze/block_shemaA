import os
import shutil
import subprocess
import time

from visio import FILE_DIRECTORY


class Vsdx:
    def __init__(self, filename):
        self.filename = filename

        try:
            subproces = subprocess.Popen('taskkill /F /IM VISIO.exe', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            time.sleep(0.1)
        except Exception:
            ...
        try:
            shutil.rmtree(FILE_DIRECTORY + "temp")
        except Exception:
            ...
        shutil.copytree(FILE_DIRECTORY + "empty-doc", FILE_DIRECTORY + "temp")

    def save_vsdx_file(self):
        shutil.make_archive("temp", 'zip', FILE_DIRECTORY + 'temp')
        shutil.move('temp.zip', self.filename)
        shutil.rmtree(FILE_DIRECTORY + "temp")
        try:
            os.system("start new.vsdx")
        except Exception:
            ...
