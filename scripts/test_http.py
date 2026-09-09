import sys
sys.stdout.reconfigure(encoding='utf-8')
import http.server
import socketserver
import threading
import urllib.request
import time
import os

PORT = 8765
os.chdir('d:/GitHub/SinoGDB_web')

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

httpd = socketserver.TCPServer(('127.0.0.1', PORT), QuietHandler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
time.sleep(0.5)

urls = [
    f'http://127.0.0.1:{PORT}/index.html',
    f'http://127.0.0.1:{PORT}/datasets.md',
    f'http://127.0.0.1:{PORT}/tiles/meta.json',
    f'http://127.0.0.1:{PORT}/tiles/base/1080p.webp',
    f'http://127.0.0.1:{PORT}/tiles/AirSystem/1080p.webp',
    f'http://127.0.0.1:{PORT}/icons/SinoGDB.svg',
]

print('Testing HTTP endpoints...')
for u in urls:
    try:
        req = urllib.request.urlopen(u)
        content = req.read()
        print(f'[HTTP {req.status}] {u} ({len(content)} bytes)')
    except Exception as e:
        print(f'[FAIL] {u}: {e}')

httpd.shutdown()
print('All HTTP tests passed!')
