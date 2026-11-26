#!/usr/bin/env python3
"""
CloudMart — ALB Chính (Main Load Balancer)
HTTPS port 8443 | Phục vụ từ demo_pages/

Tab 1: python3 scripts/run_local_demo.py
Ctrl+C để mô phỏng node sập → HA sẽ tự failover sang backup
"""

import ssl
import http.server
import os
import sys
import subprocess
import mimetypes
from pathlib import Path
from datetime import datetime

# ─── Cấu hình ─────────────────────────────────────────────────────────────────
PORT      = 8443
NODE_NAME = "main"
BASE_DIR  = Path(__file__).parent.parent
DEMO_DIR  = BASE_DIR / "demo_pages"
SSL_DIR   = BASE_DIR / "scripts" / "ssl"
CERT_FILE = SSL_DIR / "server.crt"
KEY_FILE  = SSL_DIR / "server.key"

# ─── Màu sắc terminal ──────────────────────────────────────────────────────────
C = {
    'green':   '\033[92m', 'yellow': '\033[93m', 'red':     '\033[91m',
    'blue':    '\033[94m', 'cyan':   '\033[96m', 'magenta': '\033[95m',
    'bold':    '\033[1m',  'dim':    '\033[2m',  'reset':   '\033[0m',
}
def clr(t, *cs): return ''.join(C[c] for c in cs if c in C) + str(t) + C['reset']
def ts(): return datetime.now().strftime('%H:%M:%S')

# ─── SSL Certificate ───────────────────────────────────────────────────────────
def ensure_ssl_cert():
    SSL_DIR.mkdir(parents=True, exist_ok=True)
    if not CERT_FILE.exists() or not KEY_FILE.exists():
        print(clr("🔐 Tạo SSL certificate tự ký...", 'yellow'))
        r = subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", str(KEY_FILE), "-out", str(CERT_FILE),
            "-days", "365", "-nodes",
            "-subj", "/C=VN/ST=HCM/L=HoChiMinh/O=CloudMart/OU=Demo/CN=localhost"
        ], capture_output=True, text=True)
        if r.returncode != 0:
            print(clr(f"❌ Lỗi tạo SSL: {r.stderr}", 'red'))
            sys.exit(1)
        print(clr("✅ SSL cert đã tạo!", 'green'))
    return str(CERT_FILE), str(KEY_FILE)

# ─── ALB Handler ───────────────────────────────────────────────────────────────
class ALBHandler(http.server.BaseHTTPRequestHandler):

    def _resolve(self):
        """Phân giải path sang file thực tế trong demo_pages/"""
        path = self.path.split('?')[0].split('#')[0]
        clean = path.lstrip('/')

        if path == '/' or clean == '' or clean == 'frontend' or clean == 'frontend/':
            return DEMO_DIR / "frontend" / "index.html"
        if clean.startswith('frontend/'):
            return DEMO_DIR / "frontend" / clean[len('frontend/'):]

        if clean == 'products' or clean == 'products/':
            return DEMO_DIR / "products" / "index.html"
        if clean.startswith('products/'):
            return DEMO_DIR / "products" / clean[len('products/'):]

        if clean == 'checkout' or clean == 'checkout/':
            return DEMO_DIR / "checkout" / "index.html"
        if clean.startswith('checkout/'):
            return DEMO_DIR / "checkout" / clean[len('checkout/'):]

        if clean.startswith('assets/'):
            asset = clean[len('assets/'):]
            for base in [DEMO_DIR / "assets",
                         DEMO_DIR / "products" / "assets",
                         DEMO_DIR / "frontend" / "assets",
                         DEMO_DIR / "checkout" / "assets"]:
                f = base / asset
                if f.exists():
                    return f
            return DEMO_DIR / "assets" / asset

        return DEMO_DIR / clean

    def _send_file(self, file_path):
        try:
            data = file_path.read_bytes()
        except Exception as e:
            self.send_error(500, str(e))
            return
        ct, _ = mimetypes.guess_type(str(file_path))
        self.send_response(200)
        self.send_header('Content-Type',  ct or 'application/octet-stream')
        self.send_header('Content-Length', len(data))
        self.send_header('X-Served-By',   NODE_NAME)
        self.send_header('X-HA-Node',     f'{NODE_NAME}-{PORT}')
        self.send_header('Cache-Control', 'no-cache, no-store')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        fp = self._resolve()
        if fp.is_dir():
            fp = fp / "index.html"
        if not fp.exists():
            self.send_error(404, f"Not found: {self.path}")
            return
        self._send_file(fp)

    def do_HEAD(self):
        """Health-check endpoint cho HA Entry"""
        fp = self._resolve()
        if fp.is_dir():
            fp = fp / "index.html"
        if fp.exists():
            self.send_response(200)
            self.send_header('X-Served-By', NODE_NAME)
            self.send_header('X-HA-Node', f'{NODE_NAME}-{PORT}')
            self.end_headers()
        else:
            self.send_error(404)

    def log_message(self, fmt, *args):
        status = args[1] if len(args) > 1 else '???'
        sc = 'green' if status.startswith('2') else ('yellow' if status.startswith('3') else 'red')
        path = self.path[:55] + ('…' if len(self.path) > 55 else '')
        print(clr(f"  [{ts()}][MAIN:{PORT}] {self.command} {path}", 'dim') +
              " → " + clr(status, sc))

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    cert, key = ensure_ssl_cert()

    print(clr("""
╔══════════════════════════════════════════════════════╗
║   🏪  CloudMart — ALB CHÍNH (Main Load Balancer)   ║
╚══════════════════════════════════════════════════════╝""", 'bold', 'green'))

    print(f"""
  {clr('🌐 URL:', 'cyan')}    {clr(f'https://localhost:{PORT}/', 'bold', 'cyan')}
  {clr('📦 Nguồn:', 'blue')}  {DEMO_DIR}
  {clr('📡 Node:', 'blue')}   {NODE_NAME} | Port {PORT}

  {clr('Routes:', 'yellow')}
    /              → Frontend (trang chủ)
    /products      → Danh sách sản phẩm (114 SP)
    /checkout      → Thanh toán
    /assets/*      → Tài nguyên tĩnh

  {clr('⚡ Nhấn Ctrl+C để mô phỏng node sập → HA tự failover!', 'bold', 'green')}
  {clr('─' * 54, 'dim')}
""")

    class ThreadedHTTPSServer(http.server.ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    server = ThreadedHTTPSServer(('0.0.0.0', PORT), ALBHandler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(clr(f"\n  ⚠️  ALB Chính (Port {PORT}) ĐÃ SẬP! HA sẽ failover sang backup…\n",
                  'red', 'bold'))
        server.server_close()

if __name__ == '__main__':
    main()
