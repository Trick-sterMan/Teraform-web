#!/usr/bin/env python3
"""
==============================================================================
HE THONG HA LOCAL - MO PHONG ACTIVE-PASSIVE FAILOVER (THAY THE HAPROXY)
De tai: Can bang tai dua tren noi dung HTTPS voi Terraform
==============================================================================
Kien truc LOCAL:
  Cong 7443 (HTTPS) - HAProxy Python = Diem vao duy nhat (Entry Point)
    -> Health check chu dong vao ALB chinh (8443) moi 2 giay
    -> Neu ALB chinh khoe: proxy tat ca request sang 8443 (PRIMARY)
    -> Neu ALB chinh sap (fall 2 lan): tu dong chuyen sang ALB backup (9443)
    -> Khi ALB chinh hoi phuc (rise 2 lan): tu dong quay ve 8443

  Cong 8443 (HTTPS) - ALB chinh (run_local_demo.py - khong doi)
  Cong 9443 (HTTPS) - ALB backup (server nay - run_ha_local.py khoi dong)
  Cong 9081/9082/9083 - Backend backup (phuc vu tu demo_pages/)

Cach chay:
  python scripts/run_ha_local.py

Sau do mo them terminal khac va chay ALB chinh:
  python scripts/run_local_demo.py
==============================================================================
"""

import http.server
import socketserver
import threading
import ssl
import os
import sys
import time
import urllib.request
import urllib.error
import signal

# --- Duong dan goc ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_DIR = os.path.join(BASE_DIR, "demo_pages")
CERTS_DIR = os.path.join(BASE_DIR, "certs")

# --- Cau hinh cong ---
PRIMARY_HOST   = "127.0.0.1"
PRIMARY_PORT   = 8443      # ALB chinh (run_local_demo.py)
BACKUP_PORT    = 9443      # ALB backup (file nay khoi dong)
ENTRY_PORT     = 7443      # Diem vao duy nhat (HAProxy Python)
BACKEND_B_FE   = 9081      # Backend backup frontend
BACKEND_B_PROD = 9082      # Backend backup products
BACKEND_B_CHK  = 9083      # Backend backup checkout

# --- Tham so health check (giong HAProxy: inter 2s fall 2 rise 2) ---
HEALTH_INTERVAL = 2        # Kiem tra moi 2 giay
FALL_THRESHOLD  = 2        # Sap sau 2 lan loi lien tiep
RISE_THRESHOLD  = 2        # Hoi phuc sau 2 lan thanh cong lien tiep

# =============================================================================
# TRANG THAI FAILOVER (chia se giua cac thread)
# =============================================================================
class FailoverState:
    def __init__(self):
        self._lock         = threading.Lock()
        self.use_backup    = False   # False = dang dung primary, True = dang dung backup
        self._fail_count   = 0
        self._rise_count   = 0

    def record_fail(self):
        """Ghi nhan 1 lan health check that bai."""
        with self._lock:
            self._fail_count += 1
            self._rise_count = 0
            if not self.use_backup and self._fail_count >= FALL_THRESHOLD:
                self.use_backup = True
                self._fail_count = 0
                return "FAILOVER"   # Vua chuyen sang backup
        return None

    def record_success(self):
        """Ghi nhan 1 lan health check thanh cong."""
        with self._lock:
            self._rise_count += 1
            self._fail_count = 0
            if self.use_backup and self._rise_count >= RISE_THRESHOLD:
                self.use_backup = False
                self._rise_count = 0
                return "FAILBACK"   # Vua quay ve primary
        return None

    def current(self):
        with self._lock:
            return "BACKUP" if self.use_backup else "PRIMARY"

    def target_port(self):
        with self._lock:
            return BACKUP_PORT if self.use_backup else PRIMARY_PORT

FAILOVER = FailoverState()

# =============================================================================
# HEALTH CHECK THREAD - Kiem tra ALB chinh moi HEALTH_INTERVAL giay
# =============================================================================
def health_check_loop():
    """
    Kiem tra HTTPS cong 8443 (ALB chinh) moi 2 giay.
    Dung urllib voi context bo qua SSL tu ky (self-signed).
    Chap nhan ma 2xx va 3xx (ke ca redirect 301) la KHOE.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while True:
        try:
            url = f"https://{PRIMARY_HOST}:{PRIMARY_PORT}/"
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=3, context=ctx) as resp:
                code = resp.getcode()
            # 2xx va 3xx deu la KHOE
            if 200 <= code < 400:
                event = FAILOVER.record_success()
                if event == "FAILBACK":
                    ts = time.strftime("%H:%M:%S")
                    print(f"\n[{ts}] *** FAILBACK *** ALB chinh hoi phuc -> Quay ve PRIMARY (:{PRIMARY_PORT})\n")
        except Exception:
            # Loi ket noi hoac timeout -> primary sap
            event = FAILOVER.record_fail()
            if event == "FAILOVER":
                ts = time.strftime("%H:%M:%S")
                print(f"\n[{ts}] *** FAILOVER *** ALB chinh KHONG PHAN HOI -> Chuyen sang BACKUP (:{BACKUP_PORT})\n")

        time.sleep(HEALTH_INTERVAL)

# =============================================================================
# BACKEND BACKUP - Phuc vu noi dung tu demo_pages/ (giong ALB chinh)
# =============================================================================
def make_static_handler(root_dir):
    """Tao handler phuc vu file tinh tu root_dir."""
    class StaticHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=root_dir, **kwargs)

        def log_message(self, fmt, *args):
            pass   # Tat log thieu de khong ran console

        def handle_one_request(self):
            try:
                super().handle_one_request()
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass

    return StaticHandler


def run_static_server(port, folder):
    """Chay HTTP server don gian cho 1 backend."""
    folder_path = os.path.join(DEMO_DIR, folder)
    handler = make_static_handler(folder_path)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", port), handler) as srv:
        srv.serve_forever()

# =============================================================================
# ALB BACKUP (CONG 9443, HTTPS) - Dinh tuyen path giong ALB chinh
# Them header: X-Served-By: backup (de chung minh request qua server nao)
# =============================================================================
class BackupALBHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def translate_path(self, path):
        """Dinh tuyen Path giong ALB chinh (mo phong Listener Rules)."""
        # Strip query string
        path = path.split("?")[0].split("#")[0]

        if path == "/products" or path.startswith("/products/"):
            rel = path.lstrip("/")
            full = os.path.join(DEMO_DIR, "products", rel)
            if os.path.isdir(full):
                full = os.path.join(full, "index.html")
            return full

        elif path == "/checkout" or path.startswith("/checkout/"):
            rel = path.lstrip("/")
            full = os.path.join(DEMO_DIR, "checkout", rel)
            if os.path.isdir(full):
                full = os.path.join(full, "index.html")
            return full

        else:
            rel = path.lstrip("/")
            full = os.path.join(DEMO_DIR, "frontend", rel)
            if os.path.isdir(full):
                full = os.path.join(full, "index.html")
            return full

    def end_headers(self):
        # Header kiem dinh: request nay duoc phuc vu boi SERVER NAO
        self.send_header("X-Served-By",  "backup")
        self.send_header("X-ALB-Node",   f"backup-alb:{BACKUP_PORT}")
        self.send_header("X-HA-Role",    "SECONDARY")

        # Header dinh tuyen (giong ALB chinh)
        p = self.path.split("?")[0]
        if p == "/products" or p.startswith("/products/"):
            self.send_header("X-ALB-Rule", "Priority 10: /products/* -> tg_products (backup)")
        elif p == "/checkout" or p.startswith("/checkout/"):
            self.send_header("X-ALB-Rule", "Priority 20: /checkout/* -> tg_checkout (backup)")
        else:
            self.send_header("X-ALB-Rule", "Default: / -> tg_frontend (backup)")

        super().end_headers()


def run_backup_alb(port=BACKUP_PORT):
    """Chay ALB backup voi HTTPS (dung chung cert/key voi ALB chinh)."""
    cert_path = os.path.join(CERTS_DIR, "cert.pem")
    key_path  = os.path.join(CERTS_DIR, "key.pem")

    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("0.0.0.0", port), BackupALBHandler)

    if os.path.exists(cert_path) and os.path.exists(key_path):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=cert_path, keyfile=key_path)
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        print(f"[Cong {port}] HTTPS ALB Backup san sang (SSL/TLS)")
    else:
        print(f"[Cong {port}] HTTP ALB Backup san sang (khong tim thay cert.pem)")

    httpd.serve_forever()

# =============================================================================
# HAPROXY PYTHON - DIEM VAO DUY NHAT (CONG 7443, HTTPS)
# Proxy toan bo request sang ALB dang hoat dong (primary hoac backup)
# =============================================================================
class HAProxyHandler(http.server.BaseHTTPRequestHandler):
    """
    Proxy HTTPS don gian: nhan request -> chuyen sang target hien tai
    -> tra ve response cho client, giu nguyen header.
    """
    def log_message(self, fmt, *args):
        pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def _proxy(self):
        target_port = FAILOVER.target_port()
        # ALB chinh la HTTPS, backup cung HTTPS
        target_url = f"https://127.0.0.1:{target_port}{self.path}"

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            # Doc body neu co (POST)
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length else None

            req = urllib.request.Request(target_url, data=body, method=self.command)
            # Chuyen mot so header quan trong
            for h in ["Accept", "Accept-Language", "Accept-Encoding", "User-Agent", "Cookie"]:
                val = self.headers.get(h)
                if val:
                    req.add_header(h, val)

            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                self.send_response(resp.getcode())
                # Chuyen header tu upstream ve client
                for key, val in resp.headers.items():
                    if key.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(key, val)
                # Them header cho biet dang dung node nao
                self.send_header("X-HA-Active-Node", FAILOVER.current())
                self.send_header("X-HA-Entry-Port",  str(ENTRY_PORT))
                self.end_headers()
                self.wfile.write(resp.read())

        except Exception as e:
            # Loi proxy -> tra 502
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("X-HA-Active-Node", FAILOVER.current())
            self.end_headers()
            self.wfile.write(
                f"502 Bad Gateway\nHA Proxy khong the ket noi toi {target_url}\nLoi: {e}".encode()
            )

    def do_GET(self):    self._proxy()
    def do_HEAD(self):   self._proxy()
    def do_POST(self):   self._proxy()


def run_ha_entry(port=ENTRY_PORT):
    """Chay HTTPS entry point (HAProxy Python) voi cert/key chung."""
    cert_path = os.path.join(CERTS_DIR, "cert.pem")
    key_path  = os.path.join(CERTS_DIR, "key.pem")

    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("0.0.0.0", port), HAProxyHandler)

    if os.path.exists(cert_path) and os.path.exists(key_path):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=cert_path, keyfile=key_path)
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        print(f"[Cong {port}] HTTPS HA Entry Point (HAProxy Python) san sang")
    else:
        print(f"[Cong {port}] CANH BAO: Khong tim thay cert.pem / key.pem!")

    httpd.serve_forever()

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("HA LOCAL - ACTIVE-PASSIVE FAILOVER (Thay the HAProxy)")
    print("=" * 70)

    # 1. Khoi dong 3 backend BACKUP
    for port, folder in [(BACKEND_B_FE, "frontend"), (BACKEND_B_PROD, "products"), (BACKEND_B_CHK, "checkout")]:
        t = threading.Thread(target=run_static_server, args=(port, folder), daemon=True)
        t.start()
        print(f"  [Cong {port}] Backend Backup {folder} san sang")

    time.sleep(0.5)

    # 2. Khoi dong ALB Backup (HTTPS cong 9443)
    t_backup = threading.Thread(target=run_backup_alb, args=(BACKUP_PORT,), daemon=True)
    t_backup.start()
    time.sleep(0.5)

    # 3. Khoi dong HA Entry Point (HTTPS cong 7443)
    t_entry = threading.Thread(target=run_ha_entry, args=(ENTRY_PORT,), daemon=True)
    t_entry.start()
    time.sleep(0.5)

    # 4. Khoi dong Health Check thread
    t_hc = threading.Thread(target=health_check_loop, daemon=True)
    t_hc.start()

    print()
    print("=" * 70)
    print("HUONG DAN SU DUNG:")
    print("-" * 70)
    print(f"  BUOC 1: Mo terminal KHAC, chay ALB chinh:")
    print(f"            python scripts/run_local_demo.py")
    print()
    print(f"  BUOC 2: Truy cap qua HA Entry Point (diem vao duy nhat):")
    print(f"            https://localhost:{ENTRY_PORT}/")
    print(f"            https://localhost:{ENTRY_PORT}/products/")
    print(f"            https://localhost:{ENTRY_PORT}/checkout/")
    print()
    print(f"  BUOC 3: Tat ALB chinh (Ctrl+C tren terminal run_local_demo.py)")
    print(f"          hoac chay ha_test.sh de load test.")
    print(f"          -> He thong tu dong chuyen sang BACKUP (:{BACKUP_PORT}) sau {FALL_THRESHOLD * HEALTH_INTERVAL}s")
    print()
    print(f"  BUOC 4: Khoi dong lai ALB chinh")
    print(f"          -> He thong tu dong quay ve PRIMARY sau {RISE_THRESHOLD * HEALTH_INTERVAL}s")
    print()
    print(f"  Kiem tra dang phuc vu server nao:")
    print(f"    curl -k -s -I https://localhost:{ENTRY_PORT}/ | grep X-HA-Active-Node")
    print(f"    curl -k -s -I https://localhost:{BACKUP_PORT}/ | grep X-Served-By")
    print("=" * 70)
    print("Nhan Ctrl+C de dung.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDa dung he thong HA local.")
        sys.exit(0)
