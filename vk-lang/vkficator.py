filename = input("path:")

with open(filename) as file:
    code = file.read()

lang = [
    ('дизлайк', '-'),
    ('лайк', '+'),
    ('отписка', '/'),
    ('репост', '*'),
    ('коммент', 'input'),
    ('пост', 'print'),
]

for word, command in lang:
    if code.count(command) != 0:
        print("error")
        exit()

for word, command in lang:
    code = code.replace(word, command)

exec(code)
