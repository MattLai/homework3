import sys
import os

image_path = '/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/positive/'

fns = os.listdir(image_path)
with open('positive.txt', 'w') as f:
    for fn in fns:
        path = os.path.join(image_path, fn)
        #print('{}\n'.format(path+' 1 0 0 20 20'))
        f.write('{}\n'.format(path+' 1 0 0 20 20'))
