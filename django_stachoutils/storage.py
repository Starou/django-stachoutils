import os
from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            os.unlink(os.path.join(self.location, name))
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name
