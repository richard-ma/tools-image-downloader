# !/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import shutil
from pprint import pprint


class App:
    def __init__(self):
        self.title_line = sys.argv[0]
        self.counter = 1
        self.workingDir = None

    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1

    def initCounter(self, value=1):
        self.counter = value

    def run(self):
        self.usage()
        self.process()

    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print(" " * ((80 - 12 - len(self.title_line)) // 2),
              self.title_line,
              " " * ((80 - 12 - len(self.title_line)) // 2))
        print("*", " " * 76, "*")
        print("*" * 80)

    def input(self, notification, default=None):
        var = input(notification)

        if len(var) == 0:
            return default
        else:
            return var

    def readTxtToList(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            for row in f.readlines():
                # remove \n and \r
                data.append(row.replace('\n', '').replace('\r', ''))
        return data

    def readCsvToDict(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding="GBK", newline=''):
        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f,
                                    fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext

    def getWorkingDir(self):
        return self.workingDir

    def setWorkingDir(self, wd):
        self.workingDir = wd
        return self.workingDir

    def setWorkingDirFromFilename(self, filename):
        return self.setWorkingDir(os.path.dirname(filename))

    def process(self):
        pass


class MyApp(App):
    def __init__(self):
        super().__init__()
        self.settings = {
            'test_dir': 'test',
            'output_dir': 'output',
        }

    def process(self):
        # set input
        input_filename = self.input(
            "请将csv文件拖动到此窗口，然后按回车键。",
            default=os.path.join(self.settings['test_dir'], "amproducts_173916_20220414093004_22468_N84NIXW.csv"))

        # set working directory
        self.setWorkingDirFromFilename(input_filename)
        # pprint(self.workingDir)

        # set output
        output_filename = os.path.join(self.getWorkingDir(), 'notfound.txt')

        # read data
        data = self.readCsvToDict(input_filename)
        # pprint(data)

        # process line
        for line in data:
            folder_name = line['folder']
            os.makedirs(os.path.join(self.getWorkingDir(), folder_name))


if __name__ == "__main__":
    app = MyApp()
    app.run()
