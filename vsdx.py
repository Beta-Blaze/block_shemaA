import shutil
import zipfile


class Vsdx_old:
    def __init__(self, filename):
        self.filename = filename
        self.base_filename = self.filename[:-5]
        self.directory = '\\'.join(__file__.split("\\")[:-1]) + '\\'

    def open_vsdx_file(self):
        with zipfile.ZipFile(self.filename, "r") as zip_ref:
            zip_ref.extractall(self.directory + "\\temp")

    def save_vsdx_file(self):
        shutil.make_archive(self.base_filename, 'zip', self.directory + "\\temp")
        shutil.move(self.base_filename + '.zip', self.base_filename + '_new.vsdx')
        shutil.rmtree(self.directory + "\\temp")


class Vsdx:
    def __init__(self, filename):
        self.filename = filename
        self.directory = '\\'.join(__file__.split("\\")[:-1]) + '\\'
        try:
            shutil.rmtree("temp")
        except Exception:
            ...
        shutil.copytree(self.directory + "empty-doc", self.directory + "temp")

    def save_vsdx_file(self):
        shutil.make_archive("temp", 'zip', self.directory + 'temp')
        shutil.move('temp.zip', self.filename)
        shutil.rmtree("temp")
