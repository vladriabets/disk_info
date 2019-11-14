import subprocess

# open file with a string that contains path to the device
with open('path_to_device.txt', 'r') as f:
    device_name = f.read()
    if device_name.startswith('/dev/'):
        device_name = device_name[5:]

# run commands and reformat their output
lsblk = subprocess.check_output(['lsblk', '-b', '-l', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE'])
df = subprocess.check_output(['df', '-BM', '--output=source,avail'])
devices_list = lsblk.decode('utf-8').rstrip().split('\n')
devices = [i.split() for i in devices_list]

# parse commands output to find information about the device
mountpoint = False
for row in devices:
    if device_name == row[0]:
        # size in GB is rounded to integer
        size = int(int(row[1]) / 1073741824)
        typee = row[2]
        result = '/dev/{0} {1} {2}G'.format(device_name, typee, size)
        if len(row) == 4:
            fstype = row[3]
            result += ' {}'.format(fstype)
        elif len(row) == 5:
            mountpoint = row[3]
            fstype = row[4]
            result += ' {0} {1}'.format(mountpoint, fstype)

if mountpoint:
    df = df.decode('utf-8').rstrip().split('\n')
    spaces = [i.split() for i in df]
    for space in spaces:
        if space[0] == '/dev/' + device_name:
            avail_space = space[1]
            result = '/dev/{0} {1} {2}G {3} {4} {5}'.format(device_name, typee, size, avail_space, fstype, mountpoint)

try:
    print(result)
except NameError:
    print('Disk device is not found')
