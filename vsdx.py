import shutil


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
