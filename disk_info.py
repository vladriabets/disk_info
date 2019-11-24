import subprocess
import os
import json


def read_device_name(path_to_file):

    """ Reads device name from a file """

    if os.path.exists(path_to_file):
        with open(path_to_file, 'r', 1) as f:
            device_name = f.read()
            return '/dev/' + device_name
    else:
        print('path_to_device.txt does not exists')
        exit(1)


def give_device_info(device_name):

    """ Takes device name and returns information about it """
    try:
        lsblk = json.loads(subprocess.check_output(['lsblk', '-b', '--json', '-o',
                                                  'NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE', device_name]))
    except:
        print('Wrong device name')
        exit(1)

    device_type = lsblk['blockdevices'][0]['type']
    size = int(int(lsblk['blockdevices'][0]['size'])/1073741824)
    result = '{0} {1} {2}GB'.format(device_name, device_type, size)

    if lsblk['blockdevices'][0]['fstype']:
        fstype = lsblk['blockdevices'][0]['fstype']
        df = subprocess.check_output(['df', '-BM', '--output=source,avail', device_name])
        df = df.decode('utf-8').rstrip()
        space_str = df.split('\n')[1]
        space = space_str.split()[1]
        result += ' {0} {1}'.format(space, fstype)

    if lsblk['blockdevices'][0]['mountpoint']:
        mountpoint = lsblk['blockdevices'][0]['mountpoint']
        result += ' ' + mountpoint

    return result


name = read_device_name('path_to_device.txt')
device_info = give_device_info(name)
print(device_info)
