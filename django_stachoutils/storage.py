import os

from django.core.files.storage import FileSystemStorage
from django.core.files import File
from sorl.thumbnail import delete


class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            img = File(open(os.path.join(self.location, name), "w"))
            delete(img)
        return super(OverwriteStorage, self)._save(name, content)
    def get_available_name(self, name):
        return name
