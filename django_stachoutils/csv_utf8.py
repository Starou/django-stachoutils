import csv


class UnicodeWriter(object):
    def __init__(self, f, **kwargs):
        self.writer = csv.writer(f, **kwargs)

    def writerow(self, row):
        self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
