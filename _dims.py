import io, re

dims = {
    'hero-krylatskoe.jpg': (1400, 1050),
    'ski.jpg': (1100, 825),
    'cycling.jpg': (1100, 744),
    'triathlon.jpg': (1100, 733),
    'portrait.jpg': (900, 900),
}

s = io.open('index.html', encoding='utf-8').read()

for name, (w, h) in dims.items():
    pat = re.compile(r'<img src="assets/img/' + re.escape(name) + r'"(?![^>]*\bwidth=)')
    s, n = pat.subn('<img src="assets/img/%s" width="%d" height="%d"' % (name, w, h), s)
    print(name, n)

io.open('index.html', 'w', encoding='utf-8').write(s)
