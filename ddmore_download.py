import os

for i in range(1, 324):
    os.system(f'wget http://repository.ddmore.eu/model/download/DDMODEL00000{str(i).zfill(3)}' + ' -P ddmore')
