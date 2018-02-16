import os
import shutil
import subprocess


def splitzip_to_merged7z(romset):
    for name in iter(romset):
        if (os.path.exists(name)):
            shutil.rmtree(name)

        os.mkdir(name)
        os.chdir(name)
        empty = True
        for child in romset[name]:
            path = '../{0}.zip'.format(child.get('name'))
            if(os.path.exists(path)):
                subprocess.run('unzip -n {0}'.format(path),
                               shell=True, check=True)
                empty = False

        os.chdir('..')
        if (empty):
            subprocess.run('touch MAME/empty/{0}.7z '.format(name),
                           shell=True, check=True)
        else:
            subprocess.run('7z a -t7z -mx9 {0}.7z {0}'.format(name),
                           shell=True, check=True)
            subprocess.run('mv {0}.7z MAME/'.format(name),
                           shell=True, check=True)
        shutil.rmtree(name)


def keep_only_set(romset, folder, remove):
    i = 0
    j = 0
    print('the remove flag is: {0}'.format(remove))
    for filename in sorted(os.listdir(folder)):
        noext=os.path.splitext(filename.lower())[0]
        if (noext not in romset):
            i += 1
            path = '{0}{1}'.format(folder, filename)
            if (os.path.isdir(path)):
                if (remove):
                    shutil.rmtree(path)
                print('remove dir: {0}'.format(path))
            else:
                if (remove):
                    os.remove(path)
                print('remove file: {0}'.format(path))
        else:
            j += 1
    print('Removed {0} files'.format(i))
    print('Found {0} files from the romset'.format(j))
