import os

lvl_map = []
WIDTH = 0
HEIGHT = 0

def intCheck(raw_in, prompt):
    while True:
        try:
            raw_in = int(input(prompt))
            break
        except ValueError:
            print('Please only enter integers.')

    return raw_in

WIDTH = intCheck(WIDTH, 'Width: ')
HEIGHT = intCheck(HEIGHT, 'Height: ')
lvl_name = input('Filename: ')

for row in range(HEIGHT):
    output = []

    if row == 0 or row == HEIGHT-1:
        for i in range(WIDTH):
            output.append(1)
    else:
        output.append(1)
        for i in range(WIDTH-2):
            output.append(0)
        output.append(1)
    
    lvl_map.append(output)

for i in range(HEIGHT):
    print(lvl_map[i])

if 'maps' not in os.listdir('.'):
    os.mkdir('maps')

with open(f'maps/{lvl_name}.py', 'w') as file:
    file.write('lvl_map = ' + str(lvl_map))

file.close()