#!/usr/bin/env python
import os
import argparse


class ImageConvert:
    def __init__(self, args):
        self.valid = ['.jpg', '.webp']
        self.backupdir = 'backups'
        self.folder = args.folder
        self.backups = args.backups
        self.prefix = args.prefix
        self.startat = args.start
        self.wallpapers = self.collect_wallpapers()

    def collect_wallpapers(self):
        wallpapers = []
        for wallpaper in os.listdir(self.folder):
            _, extension = os.path.splitext(wallpaper)
            if extension.lower() in self.valid:
                wallpapers.append(wallpaper)
        wallpapers.sort()
        return wallpapers

    def get_extension(self, filename):
        _, extension = os.path.splitext(filename)
        return extension

    def check_backups(self):
        path = os.path.join(self.folder, self.backupdir)
        if not os.path.exists(path):
            os.mkdir(path)

    def myprint(self, line, clear=False, nl=False):
        newline = '\n\n' if nl else '\n'
        if clear:
            print('\033[1A', end='\x1b[2K')
        print(line, end=newline)

    def run(self):
        if self.backups:
            self.check_backups()

        os.system('clear')
        self.myprint('.-= CONVERT WALLPAPERS =-.', nl=True)
        print()

        total = len(self.wallpapers)
        for num, image in enumerate(self.wallpapers, start=self.startat):
            if self.get_extension(image) in self.valid:
                # 1. Convert to PNG
                path = os.path.join(self.folder, image)
                newname = f'{self.prefix}-{num:05}.png'
                newpath = os.path.join(self.folder, newname)

                # 1a. Print some information to the screen
                counter = num - self.startat
                self.myprint(f'Converting {counter:05}/{total:05}: {image} -> {newname}', clear=True)

                # 1b. Actually convert the image
                os.system(f'convert {path} -resize 1920x1080 {newpath}')
                
                # 3. Create a backup
                if self.backups:
                    backuppath = os.path.join(self.folder, 'backups', image)
                    os.system(f'mv {path} {backuppath}')
                else:
                    os.remove(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder',
                        required=True,
                        help='Folder with images to convert')
    parser.add_argument('-p', '--prefix',
                        required=True,
                        default='image',
                        help='Define prefix of the files')
    parser.add_argument('-s', '--start',
                        required=False,
                        type=int,
                        default=1,
                        help='Where to start counting')
    parser.add_argument('-b', '--backups',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Create backups (default: False)')
    
    args = parser.parse_args()
    app = ImageConvert(args)
    app.run()
