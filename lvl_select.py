import os
import random

print('Finding maps...')
lvl_map = os.listdir('maps')[random.randint(0, len(os.listdir('maps'))-1)]

print(f'Loading complete. {lvl_map} chosen.')