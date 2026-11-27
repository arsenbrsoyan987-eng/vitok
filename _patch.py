import io

s = io.open('index.html', encoding='utf-8').read()

old = '<link rel="stylesheet" href="assets/css/style.css">\n'
new = ('<link rel="stylesheet" href="assets/css/style.css">\n'
       '<noscript><style>.reveal{opacity:1;transform:none}.hero__scroll{display:none}</style></noscript>\n')

assert s.count(old) == 1
s = s.replace(old, new)
io.open('index.html', 'w', encoding='utf-8').write(s)
print('ok')