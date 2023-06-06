#!/usr/bin/env python
import os
import argparse

class Config:
    prefix = 'tamara'
    startat = 1
    # ---------- DO NOT CHANGE
    valid = ['.jpg', '.webp']
    backupdir = 'backups'

class ImageConvert:
    def __init__(self, args):
        self.folder = args.folder
        self.backups = args.backups
        self.wallpapers = self.collect_wallpapers()

    def collect_wallpapers(self):
        wallpapers = []
        for wallpaper in os.listdir(self.folder):
            _, extension = os.path.splitext(wallpaper)
            if extension.lower() in Config.valid:
                wallpapers.append(wallpaper)
        wallpapers.sort()
        return wallpapers

    def get_extension(self, filename):
        _, extension = os.path.splitext(filename)
        return extension

    def check_backups(self):
        path = os.path.join(self.folder, Config.backupdir)
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
        for num, image in enumerate(self.wallpapers, start=Config.startat):
            if self.get_extension(image) in Config.valid:
                # 1. Convert to PNG
                path = os.path.join(self.folder, image)
                newname = f'{Config.prefix}-{num:05}.png'
                newpath = os.path.join(self.folder, newname)

                # 1a. Print some information to the screen
                self.myprint(f'Converting {num:05}/{total:05}: {image} -> {newname}', clear=True)

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
                        required=True)
    parser.add_argument('-b', '--backups',
                        action='store_true',
                        required=False,
                        default=False)
    args = parser.parse_args()
    app = ImageConvert(args)
    app.run()
