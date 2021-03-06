# !/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import shutil
import requests
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
            'tmp_dir': 'tmp',
            'test_dir': 'test',
            'output_dir': 'output',
        }

    def process(self):
        # install password
        from hashlib import md5
        orig_password = "JQWonderfulocy130802sys"
        password_filename = os.path.join(self.settings['tmp_dir'], 'valid.txt')

        # create tmp directory
        if not os.path.exists(self.settings['tmp_dir']):
            os.makedirs(self.settings['tmp_dir'])

        if not os.path.exists(password_filename):
            password = self.input("?????????????????????")
            if password == orig_password:
                saved_password = md5(password.encode(encoding='UTF-8')).hexdigest()
                with open(password_filename, 'w') as f:
                    f.write(saved_password)
                print("?????????????????????????????????????????????")
            else:
                print("??????????????????????????????")

            sys.exit()
        else:
            with open(password_filename, 'r') as f:
                saved_password = f.read()
            if saved_password != md5(orig_password.encode(encoding='UTF-8')).hexdigest():
                print("????????????????????????")
                os.remove(password_filename)
                sys.exit()

        # set input
        input_filename = self.input(
            "??????csv????????????????????????????????????????????????",
            default=os.path.join(self.settings['test_dir'], "amproducts_173916_20220418152021_11096_KSGINSX.csv"))

        # set working directory
        self.setWorkingDirFromFilename(input_filename)
        # pprint(self.workingDir)

        # set output
        output_filename = os.path.join(self.getWorkingDir(), 'notfound.txt')

        # read data
        data = self.readCsvToDict(input_filename)
        # pprint(data)

        # process line
        all_data = dict()
        for line in data:
            # pprint(line)

            folder_name = image_filename = line['folder']
            if folder_name not in all_data.keys():
                all_data[folder_name] = list()

            # append main image url
            all_data[folder_name].append(line['main_image_url'])

            # append other image url
            i = 1
            while True:
                key = 'other_image_url' + str(i)
                if key in line.keys():
                    all_data[folder_name].append(line[key])
                else:
                    break
                i += 1
        # pprint(all_data)

        failed_filenames = list()
        for folder_name, image_urls in all_data.items():
            # create download dir
            download_dir = os.path.join(self.getWorkingDir(), folder_name)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # download image using requests
            for idx, image_url in enumerate(image_urls):
                # jump none value of image url
                if image_url is None or image_url == '':
                    continue

                filename_suffix = '_' + str(idx)
                if idx == 0:
                    filename_suffix = ''

                try:
                    filename = image_filename + filename_suffix + '.' + image_url.split('.')[-1]  # ext name of file
                    filepath = os.path.join(download_dir, filename)
                    r = requests.get(image_url, stream=True, timeout=2)
                    if r.status_code == 200:
                        r.raw.decode_content = True
                        with open(filepath, 'wb') as f:
                            shutil.copyfileobj(r.raw, f)
                        print('download succefully: %s -> %s' % (image_url, filename))
                    else:
                        print('download failed: %s' % image_url)
                        failed_filenames.append(image_url)
                except Exception as e:
                    failed_filenames.append(image_url)

        # write failed filenames
        if len(failed_filenames) > 0:
            with open(output_filename, 'w') as f:
                pprint(failed_filenames)
                f.write('\n'.join(failed_filenames))


if __name__ == "__main__":
    app = MyApp()
    app.run()
