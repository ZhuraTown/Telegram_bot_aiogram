import copy

a = {'string': 1}
b = {}

print(a.get('string'))
print(b.get('string'))


if not b.get('string'):
    b['string'] = 1
    b[b['string']] = 'bbbbbbb'


if not b.get('string'):
    b['string'] = 1
else:
    b['string'] = b['string'] + 1
    b[b['string']] = 'aaaaa'

print(b)