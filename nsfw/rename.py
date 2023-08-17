#!/usr/bin/env python
import os
import sys
import shutil
import argparse
from PIL import Image
from time import sleep

class Rename:
    def __init__(self, args):
        self.folder = args.folder
        self.prefix = args.prefix
        self.start = args.start
        self.leading = args.leading
        self.backup = args.backup

    def showTitle(self):
        os.system('clear')
        print('+------------------------+')
        print('| RPF - Rename PNG Files |')
        print('+------------------------+', end='\n\n')

    def printNote(self, message):
        print(f'> {message}')

    def printStep(self, message):
        print(f' -- {message}')
    
    def printError(self, message, stop=False):
        print(f'>> {message}')
        if stop:
            print(f'Exiting...')
            sys.exit()

    def collectImages(self, extension):
        imageList = []
        extension = '.' + extension
        for file in os.listdir(args.folder):
            if os.path.splitext(file)[1] == extension:
                imageList.append(file)

        if len(imageList) == 0:
            self.printError(f"No PNG's found in '{self.folder}'")
            sys.exit()
        
        imageList.sort()
        return imageList

    def copyFile(self, src):
        srcpath = os.path.join(self.folder, src)
        dstpath = os.path.join(self.folder, 'backups', src)

        error = False
        try:
            shutil.copy(srcpath, dstpath)
        except shutil.SameFileError:
            self.printError(f'{src} already exists in destination')
            sleep(0.3)
            print('\033[1A', end='\x1b[2K')
            error = True
        except PermissionError:
            self.printError('Permission denied')
            sleep(0.3)
            print('\033[1A', end='\x1b[2K')
            error = True
        except:
            self.printError('An error occurred while copying file')
            sleep(0.3)
            print('\033[1A', end='\x1b[2K')
            error = True
        return error

    def backupImages(self):
        self.printNote('Backing up images...')
        imageList = self.collectImages('png')

        if not os.path.exists(os.path.join(self.folder, 'backups')):
            os.mkdir(os.path.join(self.folder, 'backups'))
        
        errorCount = 0
        for image in imageList:
            error = self.copyFile(image)
            if error:
                errorCount += 1

        if errorCount:
            self.printError(f"{errorCount} errors occurred during backup process...", stop=True)

    def checkImageSize(self, src):
        src = os.path.join(self.folder, src)
        image = Image.open(src)
        imagewidth = image.size[0]
        imageheight = image.size[1]
        if imagewidth != 1920 or imageheight != 1080:
            self.printStep(f'Resizing {src}...')
            newimage = image.resize((1920,1080))
            newimage.save(src)
            sleep(0.5)
            print('\033[1A', end='\x1b[2K')

    def renameFile(self, src, num, total):
        error = False
        dst = f"{self.prefix}-{num:0{self.leading}}.png"
        self.printStep(f"File {num:0{self.leading}}/{total:0{self.leading}}: {src} -> {dst}")
        self.checkImageSize(src)
        src = os.path.join(self.folder, src)
        dst = os.path.join(self.folder, dst)
        try:
            shutil.move(src, dst)
        except shutil.SameFileError:
            self.printError(f'{src} already exists in destination')
            sleep(0.3)
            print('\033[1A', end='\x1b[2K')
            error = True
        except PermissionError:
            self.printError('Permission denied')
            sleep(0.3)
            print('\033[1A', end='\x1b[2K')
            error = True
        except:
            self.printError('An error occurred while copying file')
            sleep(0.3)
            print('\033[1A', end='\x1b[2K')
            error = True

        sleep(0.3)
        print('\033[1A', end='\x1b[2K')
        return error

    def renameImages(self):
        self.printNote('Renaming images...')
        imageList = self.collectImages('png')

        errorCount = 0
        total = len(imageList)
        for num, image in enumerate(imageList, start=self.start):
            error = self.renameFile(image, num, total)
            if error:
                errorCount += 1

        if errorCount:
            self.printError(f"{errorCount} errors occuring during renaming process...", stop=True)
        self.printNote('Renaming done.')

    def run(self):
        self.showTitle()
        self.backupImages()
        self.renameImages()

        # delete the backups unless -b is passed
        if not self.backup:
            self.printNote('Removing backups...')
            shutil.rmtree(os.path.join(self.folder, 'backups'))

        self.printNote('Done!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--folder',
                        required=True,
                        help='Folder containing PNGs')
    parser.add_argument('-p', '--prefix',
                        required=False,
                        default='image',
                        help='Prefix to use')
    parser.add_argument('-s', '--start',
                        required=False,
                        type=int,
                        default=1,
                        help='Where to start counting')
    parser.add_argument('-l', '--leading',
                        required=False,
                        type=int,
                        default=4,
                        help='Number of leading zeroes')
    parser.add_argument('-b', '--backup',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Create backups (default: False)')

    args = parser.parse_args()
    print(args)
    app = Rename(args)
    app.run()
