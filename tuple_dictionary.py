colors = [['blue', 'green'], ['yellow', 'red']]

for x in range(2):
    for y in range(2):
        rod = {(x, y): colors[x][y]}
        print('rod', x, y, rod[(x, y)])


default_dictionary = {'analysis': 1, 'NODF': 5, 'Boron': 0}
user_values = {'NODF': 7, 'Boron': 1200}

parameters = {**default_dictionary, **user_values}  # dictionary unpacking

print(parameters)

