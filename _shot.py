import io, subprocess, os, sys

src = io.open('index.html', encoding='utf-8').read()
head = src[:src.index('</head>')]
head += '<style>.reveal{opacity:1!important;transform:none!important}</style>\n</head>\n<body>\n'

marker = sys.argv[3]
start = src.index(marker)
end = src.index('</section>', start) + len('</section>')
io.open('_inner.html', 'w', encoding='utf-8').write(head + src[start:end] + '\n</body>\n</html>\n')

width = sys.argv[1]
height = sys.argv[2]
io.open('_wrap.html', 'w', encoding='utf-8').write(
    '<!doctype html><html><body style="margin:0;background:#fff">'
    '<iframe src="_inner.html" style="width:%spx;height:%spx;border:0;display:block" '
    'scrolling="no"></iframe></body></html>' % (width, height))

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
os.makedirs('_shots', exist_ok=True)
out = '_shots/%s-%s.png' % (sys.argv[4], width)
subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                '--virtual-time-budget=4000',
                '--window-size=%s,%s' % (int(width) + 20, height),
                '--screenshot=' + out, 'file://' + os.path.abspath('_wrap.html')],
               capture_output=True)
print(out, os.path.getsize(out))