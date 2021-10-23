import shutil
from visio import FILE_DIRECTORY


class Vsdx:
    def __init__(self, filename):
        self.filename = filename
        try:
            shutil.rmtree("temp")
        except Exception:
            ...
        shutil.copytree(FILE_DIRECTORY + "empty-doc", FILE_DIRECTORY + "temp")

    def save_vsdx_file(self):
        shutil.make_archive("temp", 'zip', FILE_DIRECTORY + 'temp')
        shutil.move('temp.zip', self.filename)
        shutil.rmtree(FILE_DIRECTORY + "\\temp")
