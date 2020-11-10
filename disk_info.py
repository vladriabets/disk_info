import subprocess
import json


def read_device_name(path_to_file):

    """ Reads device name from a file """

    try:
        with open(path_to_file, 'r', 1) as f:
            device_name = f.read()
            return '/dev/' + device_name
    except FileNotFoundError:
        print('path_to_device.txt does not exist')
        exit(1)


def give_device_info(device_name):

    """ Takes device name and returns information about it """

    try:
        lsblk = json.loads(subprocess.check_output(['lsblk', '-b', '--json', '-o',
                                                   'NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE', device_name]))
    except subprocess.CalledProcessError:
        print('Wrong device name')
        exit(1)
    device = lsblk['blockdevices'][0]
    device_type = device['type']
    size = int(int(device['size'])/1073741824)
    result = '{0} {1} {2}GB'.format(device_name, device_type, size)

    if device['fstype']:
        fstype = device['fstype']
        df = subprocess.check_output(['df', '-BM', '--output=source,avail', device_name])
        df = df.decode('utf-8').rstrip()
        space_str = df.split('\n')[1]
        space = space_str.split()[1]
        result += ' {0} {1}'.format(space, fstype)

    if device['mountpoint']:
        mountpoint = device['mountpoint']
        result += ' ' + mountpoint

    return result


def main():
    name = read_device_name('path_to_device.txt')
    device_info = give_device_info(name)
    print(device_info)


if __name__ == '__main__':
    main()
