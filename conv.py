import os

wallpapers = []

if not os.path.exists('jpegs'):
    os.mkdir('jpegs')

for file in os.listdir('.'):
    if file.endswith('.jpg'):
        print(f'Converting {file}...')
        newfile = file.replace('.jpg', '.png')
        os.system(f'convert {file} -resize 1920x1080 {newfile}')
        os.system(f'mv {file} jpegs/{file}')
