#!/usr/bin/env python3
"""
CloudMart — Load Balancer (7443) + Node-2 (9443) + Node-3 (9444)

Giải pháp chống quá tải: 1 link duy nhất (7443) nhưng chia đều traffic
sang 3 backend nodes bằng thuật toán Round-Robin.

  Node-1 (Main):     port 8443  → Tab 1: python3 scripts/run_local_demo.py
  Node-2 (Backup-1): port 9443  → script này (tự khởi động)
  Node-3 (Backup-2): port 9444  → script này (tự khởi động)
  Load Balancer:     port 7443  → script này (điểm vào duy nhất)

Luồng traffic khi 100 người truy cập:
  Request  1 → Node-1 (8443)
  Request  2 → Node-2 (9443)
  Request  3 → Node-3 (9444)
  Request  4 → Node-1 (8443)
  ... (lặp lại)

Khi 1 node sập → LB tự loại khỏi pool, 2 node còn lại chia đều
Khi node phục hồi → LB tự thêm lại vào pool

Tab 2: python3 scripts/run_ha_local.py
"""

import ssl
import http.server
import urllib.request
import threading
import time
import json
import sys
import uuid
import subprocess
import mimetypes
from http.cookies import SimpleCookie
from pathlib import Path
from datetime import datetime

# ─── Cấu hình ─────────────────────────────────────────────────────────────────
LB_PORT      = 7443   # Load Balancer — điểm vào duy nhất
NODE2_PORT   = 9443   # Web Support 1 (script này)
NODE3_PORT   = 9444   # Web Support 2 (script này)
MAIN_PORT    = 8443   # Web Chính (run_local_demo.py)

MAIN_MAX_USERS         = 10    # Tối đa 10 người trên Web Chính; người thứ 11+ sang Web Support
USER_SESSION_TTL       = 20.0  # Giây giữ phiên người dùng (hết hạn nếu đóng tab > 20s)
CHECK_INTERVAL         = 2.0   # Giây giữa các health check
FAIL_THRESHOLD         = 2     # Số lần fail liên tiếp → loại khỏi pool
RECOVER_THRESHOLD      = 2     # Số lần ok liên tiếp → thêm lại vào pool
OVERLOAD_RPS_THRESHOLD = 5.0   # Ngưỡng req/s phụ trợ

BASE_DIR  = Path(__file__).parent.parent
DEMO_DIR  = BASE_DIR / "demo_pages"
SSL_DIR   = BASE_DIR / "scripts" / "ssl"
CERT_FILE = SSL_DIR / "server.crt"
KEY_FILE  = SSL_DIR / "server.key"

# ─── Danh sách backend nodes ──────────────────────────────────────────────────
ALL_NODES = [
    {'name': 'Node-1 (Main)',      'port': MAIN_PORT,  'icon': '🟢', 'role': 'main'},
    {'name': 'Node-2 (Support-1)', 'port': NODE2_PORT, 'icon': '🔵', 'role': 'support'},
    {'name': 'Node-3 (Support-2)', 'port': NODE3_PORT, 'icon': '🟣', 'role': 'support'},
]

# ─── Node Pool (Max 10 Users on Main + Overflow to Support) ──────────────────
class NodePool:
    """
    Quản lý pool các backend nodes:
    - Web Chính (Node-1): tối đa MAIN_MAX_USERS (10) người dùng hoạt động.
    - Người thứ 11+ (hoặc khi Node-1 sập): tự động chuyển sang Web Support (Node-2, Node-3).
    """
    def __init__(self, nodes):
        self._all    = nodes
        self._active = list(nodes)
        self._support_idx = 0
        self._lock   = threading.Lock()
        self._fail_count    = {n['name']: 0 for n in nodes}
        self._recover_count = {n['name']: 0 for n in nodes}
        self._stats  = {
            n['name']: {
                'port': n['port'],
                'icon': n['icon'],
                'role': n['role'],
                'healthy': True,
                'req_total': 0,
                'req_ok': 0,
                'req_fail': 0,
                'last_latency_ms': None,
            }
            for n in nodes
        }
        self._events          = []
        self._start_time      = time.time()
        self._req_history     = []
        self._main_sessions   = {}   # uid -> last_seen
        self._support_sessions = {}  # uid -> {'node': name, 'last_seen': ts}
        self._was_overloaded  = False

    def _prune_sessions_locked(self, now):
        cutoff = now - USER_SESSION_TTL
        self._main_sessions = {k: v for k, v in self._main_sessions.items() if v > cutoff}
        self._support_sessions = {k: v for k, v in self._support_sessions.items() if v['last_seen'] > cutoff}

    def _calc_rps_locked(self):
        cutoff = time.time() - 3.0
        self._req_history = [t for t in self._req_history if t > cutoff]
        return round(len(self._req_history) / 3.0, 1)

    def get_overload_state_locked(self):
        now = time.time()
        self._prune_sessions_locked(now)
        rps = self._calc_rps_locked()
        main_cnt = len(self._main_sessions)
        supp_cnt = len(self._support_sessions)
        main_healthy = self._stats['Node-1 (Main)']['healthy']

        is_overloaded = (main_cnt >= MAIN_MAX_USERS and supp_cnt > 0) or (not main_healthy) or (rps >= OVERLOAD_RPS_THRESHOLD)
        reason = []
        if not main_healthy:
            reason.append("Web chính đang bảo trì/sự cố")
        elif main_cnt >= MAIN_MAX_USERS:
            reason.append(f"Web chính đã đầy ({main_cnt}/{MAIN_MAX_USERS} người)")
        if supp_cnt > 0:
            reason.append(f"Đang chuyển {supp_cnt} người dư sang Web Support")
        if rps >= OVERLOAD_RPS_THRESHOLD and main_cnt < MAIN_MAX_USERS:
            reason.append(f"Lưu lượng cao ({rps} req/s)")
        return is_overloaded, rps, " • ".join(reason), main_cnt, supp_cnt

    def _get_node_by_name_locked(self, name):
        for n in self._active:
            if n['name'] == name:
                return n
        return None

    def _next_support_node_locked(self):
        supports = [n for n in self._active if n['role'] == 'support']
        if not supports:
            return None
        node = supports[self._support_idx % len(supports)]
        self._support_idx += 1
        return node

    def assign_node(self, uid, is_asset=False):
        """
        Chọn node cho user `uid`.
        Trả về: (node_dict | None, is_overflow, is_overloaded, rps, reason, main_cnt, supp_cnt)
        """
        with self._lock:
            now = time.time()
            self._prune_sessions_locked(now)
            self._req_history.append(now)

            if not self._active:
                return None, True, True, 0.0, "Tất cả server đều đang quá tải hoặc bảo trì", 0, 0

            main_node = self._get_node_by_name_locked('Node-1 (Main)')
            node = None
            is_overflow = False

            # Nếu chỉ là request tải ảnh/CSS đi kèm và user chưa có session, không chiếm slot mới trên Main
            if uid in self._main_sessions and main_node:
                self._main_sessions[uid] = now
                node = main_node
            elif uid in self._support_sessions:
                supp_info = self._support_sessions[uid]
                supp_info['last_seen'] = now
                node = self._get_node_by_name_locked(supp_info['node']) or self._next_support_node_locked()
                is_overflow = True
            else:
                # Người dùng mới
                if main_node and len(self._main_sessions) < MAIN_MAX_USERS:
                    if not is_asset:
                        self._main_sessions[uid] = now
                    node = main_node
                else:
                    # Web chính đã đủ 10/10 người (hoặc sập) -> đẩy sang Web Support!
                    node = self._next_support_node_locked() or main_node
                    if node and node['role'] == 'support':
                        is_overflow = True
                        if not is_asset:
                            self._support_sessions[uid] = {'node': node['name'], 'last_seen': now}

            if not node:
                return None, True, True, 0.0, "Không có server khả dụng", len(self._main_sessions), len(self._support_sessions)

            self._stats[node['name']]['req_total'] += 1
            is_overloaded, rps, reason, main_cnt, supp_cnt = self.get_overload_state_locked()

            if (main_cnt >= MAIN_MAX_USERS and supp_cnt > 0) or rps >= OVERLOAD_RPS_THRESHOLD:
                if not self._was_overloaded:
                    self._was_overloaded = True
                    msg = f"🔥 QUÁ TẢI WEB CHÍNH ({main_cnt}/{MAIN_MAX_USERS} người) → Đang đẩy {supp_cnt} người dư sang Web Support!"
                    self._events.append({'time': _ts(), 'type': 'OVERLOAD', 'msg': msg})
                    print(_clr(f"\n  [{_ts()}] {msg}\n", 'red', 'bold'))
            elif self._was_overloaded and main_cnt < MAIN_MAX_USERS and supp_cnt == 0 and rps < OVERLOAD_RPS_THRESHOLD * 0.6:
                self._was_overloaded = False
                msg = f"✨ Web chính đã giảm tải ({main_cnt}/{MAIN_MAX_USERS} người)"
                self._events.append({'time': _ts(), 'type': 'RECOVER', 'msg': msg})
                print(_clr(f"\n  [{_ts()}] {msg}\n", 'green'))

            return node, is_overflow, is_overloaded, rps, reason, main_cnt, supp_cnt

    def next_node(self):
        """Fallback helper cho retry."""
        with self._lock:
            supp = self._next_support_node_locked()
            return supp or (self._active[0] if self._active else None)

    def report_ok(self, name, latency_ms):
        with self._lock:
            self._stats[name]['req_ok'] += 1
            self._stats[name]['last_latency_ms'] = latency_ms

    def report_fail(self, name):
        with self._lock:
            self._stats[name]['req_fail'] += 1

    def health_update(self, name, is_healthy):
        """Cập nhật trạng thái health, xử lý failover/recovery."""
        with self._lock:
            st = self._stats[name]
            if is_healthy:
                self._fail_count[name] = 0
                self._recover_count[name] += 1
                # Thêm lại vào pool nếu đủ lần recover
                if (not st['healthy'] and
                        self._recover_count[name] >= RECOVER_THRESHOLD):
                    st['healthy'] = True
                    self._active.append(
                        next(n for n in self._all if n['name'] == name)
                    )
                    self._events.append({
                        'time': _ts(), 'type': 'RECOVER',
                        'msg': f"✅ {name} phục hồi → đã thêm lại vào pool"
                    })
                    print(_clr(
                        f"\n  [{_ts()}] ✅ RECOVER: {name} → thêm lại pool "
                        f"({len(self._active)}/{len(self._all)} nodes)\n",
                        'green', 'bold'))
            else:
                self._recover_count[name] = 0
                self._fail_count[name] += 1
                # Loại khỏi pool nếu fail đủ lần
                if (st['healthy'] and
                        self._fail_count[name] >= FAIL_THRESHOLD):
                    st['healthy'] = False
                    self._active = [n for n in self._active if n['name'] != name]
                    self._support_idx = 0
                    self._events.append({
                        'time': _ts(), 'type': 'DOWN',
                        'msg': f"🔴 {name} đã sập → loại khỏi pool"
                    })
                    print(_clr(
                        f"\n  [{_ts()}] 🔴 DOWN: {name} → loại khỏi pool "
                        f"({len(self._active)}/{len(self._all)} nodes còn hoạt động)\n",
                        'red', 'bold'))

    def get_stats(self):
        """Trả về JSON stats cho endpoint /lb-stats."""
        with self._lock:
            uptime = int(time.time() - self._start_time)
            is_overloaded, rps, overload_reason, main_cnt, supp_cnt = self.get_overload_state_locked()

            total_reqs = sum(s['req_total'] for s in self._stats.values())
            return {
                'active_nodes':       [n['name'] for n in self._active],
                'inactive_nodes':     [n['name'] for n in self._all
                                       if n['name'] not in [a['name'] for a in self._active]],
                'algorithm':          f'Max-{MAIN_MAX_USERS}-Main + Overflow-Support',
                'main_max_users':     MAIN_MAX_USERS,
                'main_users':         main_cnt,
                'support_users':      supp_cnt,
                'total_users':        main_cnt + supp_cnt,
                'total_requests':     total_reqs,
                'req_per_sec':        rps,
                'overload_threshold': OVERLOAD_RPS_THRESHOLD,
                'is_overloaded':      is_overloaded,
                'overload_reason':    overload_reason,
                'uptime_sec':         uptime,
                'nodes':              dict(self._stats),
                'events':             self._events[-20:],
            }

# ─── Khởi tạo pool ────────────────────────────────────────────────────────────
pool = NodePool(ALL_NODES)

# ─── Colors & helpers ─────────────────────────────────────────────────────────
C = {
    'green':   '\033[92m', 'yellow': '\033[93m', 'red':     '\033[91m',
    'blue':    '\033[94m', 'cyan':   '\033[96m', 'magenta': '\033[95m',
    'bold':    '\033[1m',  'dim':    '\033[2m',  'reset':   '\033[0m',
}
def _clr(t, *cs): return ''.join(C[c] for c in cs if c in C) + str(t) + C['reset']
def _ts(): return datetime.now().strftime('%H:%M:%S')

# ─── SSL ──────────────────────────────────────────────────────────────────────
def ensure_ssl():
    SSL_DIR.mkdir(parents=True, exist_ok=True)
    if not CERT_FILE.exists() or not KEY_FILE.exists():
        print(_clr("🔐 Tạo SSL certificate...", 'yellow'))
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", str(KEY_FILE), "-out", str(CERT_FILE),
            "-days", "365", "-nodes",
            "-subj", "/C=VN/ST=HCM/L=HoChiMinh/O=CloudMart/CN=localhost"
        ], capture_output=True)

def server_ssl_ctx():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(str(CERT_FILE), str(KEY_FILE))
    return ctx

def client_ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

_CLIENT_CTX = None
def get_client_ctx():
    global _CLIENT_CTX
    if _CLIENT_CTX is None:
        _CLIENT_CTX = client_ssl_ctx()
    return _CLIENT_CTX

# ─── Shared file resolver ─────────────────────────────────────────────────────
def resolve_path(raw_path):
    path = raw_path.split('?')[0].split('#')[0]
    clean = path.lstrip('/')
    if path == '/' or clean in ('', 'frontend', 'frontend/'):
        return DEMO_DIR / "frontend" / "index.html"
    if clean.startswith('frontend/'):
        return DEMO_DIR / "frontend" / clean[len('frontend/'):]
    if clean in ('products', 'products/'):
        return DEMO_DIR / "products" / "index.html"
    if clean.startswith('products/'):
        return DEMO_DIR / "products" / clean[len('products/'):]
    if clean in ('checkout', 'checkout/'):
        return DEMO_DIR / "checkout" / "index.html"
    if clean.startswith('checkout/'):
        return DEMO_DIR / "checkout" / clean[len('checkout/'):]
    if clean.startswith('assets/'):
        asset = clean[len('assets/'):]
        for base in [DEMO_DIR / "assets",
                     DEMO_DIR / "products" / "assets",
                     DEMO_DIR / "frontend" / "assets"]:
            f = base / asset
            if f.exists():
                return f
        return DEMO_DIR / "assets" / asset
    return DEMO_DIR / clean

# ─── Backend Node Handler (Node-2 & Node-3) ───────────────────────────────────
def make_node_handler(node_name, node_port):
    """Factory: tạo handler class cho từng backend node."""
    class NodeHandler(http.server.BaseHTTPRequestHandler):
        _name = node_name
        _port = node_port

        def do_GET(self):
            fp = resolve_path(self.path)
            if fp.is_dir():
                fp = fp / "index.html"
            if not fp.exists():
                self.send_error(404)
                return
            try:
                data = fp.read_bytes()
            except Exception as e:
                self.send_error(500, str(e))
                return
            ct, _ = mimetypes.guess_type(str(fp))
            self.send_response(200)
            self.send_header('Content-Type', ct or 'application/octet-stream')
            self.send_header('Content-Length', len(data))
            self.send_header('X-Served-By',  self._name)
            self.send_header('X-Node-Port',  str(self._port))
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)

        def do_HEAD(self):
            self.send_response(200)
            self.send_header('X-Served-By', self._name)
            self.end_headers()

        def log_message(self, fmt, *args):
            status = args[1] if len(args) > 1 else '???'
            sc = 'green' if status.startswith('2') else 'yellow'
            path = self.path[:45] + ('…' if len(self.path) > 45 else '')
            print(_clr(f"  [{_ts()}][{self._name}:{self._port}] {path}", 'dim') +
                  " → " + _clr(status, sc))

    return NodeHandler

# ─── Load Balancer Handler ────────────────────────────────────────────────────
class LBHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # Endpoint stats
        if self.path.rstrip('/') == '/lb-stats':
            self._send_stats()
            return
        self._proxy()

    def do_HEAD(self):
        self._proxy()

    def _send_stats(self):
        """Trả về JSON stats cho ha_test.py monitor."""
        data = json.dumps(pool.get_stats(), indent=2, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(data))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)

    def _inject_overload_widget(self, body_bytes, node, is_overflow, is_overloaded, rps, reason, main_cnt, supp_cnt):
        """Chèn thông báo quá tải & auto-polling /lb-stats vào HTML mà không cần sửa demo_pages/."""
        try:
            html = body_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return body_bytes

        if '</body>' not in html.lower():
            return body_bytes

        node_name = node['name']
        show_banner = is_overflow or is_overloaded
        init_display = 'flex' if show_banner else 'none'
        if is_overflow:
            init_msg = (
                f"🔥 <b>WEB CHÍNH ĐANG QUÁ TẢI ({main_cnt}/{MAIN_MAX_USERS} người tối đa)</b> — "
                f"Bạn đã được tự động chuyển sang <b>{node_name}</b> để tiếp tục truy cập mượt mà!"
            )
        elif is_overloaded:
            init_msg = (
                f"⚠️ <b>CẢNH BÁO QUÁ TẢI:</b> {reason} — "
                f"Hệ thống đang chia số người dư sang Web Support (Bạn đang ở <b>{node_name}</b>)"
            )
        else:
            init_msg = ""

        widget = f"""
<!-- CloudMart Load Balancer Overload Notification -->
<style>
  #cm-lb-banner {{
    position: fixed; top: 16px; left: 50%; transform: translateX(-50%);
    z-index: 999999; display: {init_display}; align-items: center; gap: 12px;
    background: linear-gradient(135deg, #dc2626, #ea580c);
    color: #fff; padding: 12px 20px; border-radius: 12px;
    box-shadow: 0 12px 32px rgba(220, 38, 38, 0.45);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 14px; line-height: 1.4; max-width: 92vw;
    border: 1px solid rgba(255,255,255,0.25);
    animation: cmPulse 2s infinite;
  }}
  @keyframes cmPulse {{
    0%, 100% {{ box-shadow: 0 12px 32px rgba(220, 38, 38, 0.45); }}
    50% {{ box-shadow: 0 12px 40px rgba(234, 88, 12, 0.75); }}
  }}
  #cm-lb-banner .cm-close {{
    background: rgba(255,255,255,0.2); border: none; color: #fff;
    width: 24px; height: 24px; border-radius: 50%; cursor: pointer;
    font-weight: bold; flex-shrink: 0;
  }}
  #cm-lb-pill {{
    position: fixed; bottom: 16px; left: 16px; z-index: 999998;
    background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(8px);
    color: #e2e8f0; padding: 7px 14px; border-radius: 999px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 12px; border: 1px solid rgba(255,255,255,0.15);
    display: flex; align-items: center; gap: 7px;
  }}
  #cm-lb-dot {{
    width: 8px; height: 8px; border-radius: 50%;
    background: {'#ef4444' if show_banner else '#22c55e'};
  }}
</style>
<div id="cm-lb-banner">
  <span style="font-size:18px;">🔥</span>
  <span id="cm-lb-text">{init_msg}</span>
  <button class="cm-close" onclick="document.getElementById('cm-lb-banner').style.display='none'">×</button>
</div>
<div id="cm-lb-pill">
  <span id="cm-lb-dot"></span>
  <span id="cm-lb-pill-text">Server: <b>{node_name}</b> • Web chính: {main_cnt}/{MAIN_MAX_USERS} người | Support: {supp_cnt}</span>
</div>
<script>
(function() {{
  let dismissed = false;
  const isOverflow = {'true' if is_overflow else 'false'};
  const closeBtn = document.querySelector('#cm-lb-banner .cm-close');
  if (closeBtn) closeBtn.addEventListener('click', () => {{ dismissed = true; }});
  setInterval(async () => {{
    try {{
      const res = await fetch('/lb-stats', {{ cache: 'no-store' }});
      if (!res.ok) return;
      const st = await res.json();
      const banner = document.getElementById('cm-lb-banner');
      const text = document.getElementById('cm-lb-text');
      const dot = document.getElementById('cm-lb-dot');
      const pill = document.getElementById('cm-lb-pill-text');
      if (pill) {{
        pill.innerHTML = 'Server: <b>{node_name}</b> • Web chính: <b>' + st.main_users + '/' + st.main_max_users + '</b> người | Support: <b>' + st.support_users + '</b>';
      }}
      if (st.is_overloaded || isOverflow) {{
        if (dot) dot.style.background = '#ef4444';
        if (banner && !dismissed) {{
          if (isOverflow) {{
            text.innerHTML = '🔥 <b>WEB CHÍNH ĐÃ ĐẦY (' + st.main_users + '/' + st.main_max_users + ' người)</b> — Bạn đang được hỗ trợ tại <b>{node_name}</b> để tránh quá tải!';
          }} else {{
            text.innerHTML = '⚠️ <b>CẢNH BÁO QUÁ TẢI:</b> ' + (st.overload_reason || 'Lưu lượng cao') +
              ' — Đang điều hướng số người dư sang Web Support (Bạn đang ở <b>{node_name}</b>)';
          }}
          banner.style.display = 'flex';
        }}
      }} else {{
        if (dot) dot.style.background = '#22c55e';
        if (banner) banner.style.display = 'none';
        dismissed = false;
      }}
    }} catch(e) {{}}
  }}, 2500);
}})();
</script>
"""
        idx = html.lower().rfind('</body>')
        new_html = html[:idx] + widget + html[idx:]
        return new_html.encode('utf-8')

    def _send_overload_503(self):
        """Trang thông báo thân thiện khi tất cả server đều quá tải/sập."""
        html = """<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8"><title>Hệ thống đang quá tải — CloudMart</title>
<style>
  body { font-family: -apple-system, sans-serif; background: #0f172a; color: #f8fafc;
         display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
  .card { background: #1e293b; padding: 36px; border-radius: 16px; max-width: 480px;
          text-align: center; border: 1px solid #ef4444; box-shadow: 0 20px 50px rgba(239,68,68,0.25); }
  h1 { color: #f87171; margin-top: 0; }
  p { color: #cbd5e1; line-height: 1.6; }
  .btn { display: inline-block; margin-top: 16px; padding: 10px 24px; background: #3b82f6;
         color: #fff; border-radius: 8px; text-decoration: none; font-weight: 600; }
</style>
<meta http-equiv="refresh" content="5">
</head><body><div class="card">
  <h1>🚨 Hệ Thống Đang Quá Tải</h1>
  <p>Hiện tại lượng người truy cập quá lớn hoặc tất cả máy chủ đang bảo trì.</p>
  <p>Trang sẽ tự động tải lại sau <b>5 giây</b>...</p>
  <a class="btn" href="/">Thử lại ngay</a>
</div></body></html>""".encode('utf-8')
        self.send_response(503)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(html))
        self.send_header('Retry-After', '5')
        self.end_headers()
        self.wfile.write(html)

    def _get_uid_and_is_new(self):
        test_u = self.headers.get('X-Test-User')
        if test_u:
            return test_u, False
        raw_cookie = self.headers.get('Cookie', '')
        if raw_cookie:
            c = SimpleCookie()
            try:
                c.load(raw_cookie)
                if 'cm_uid' in c and c['cm_uid'].value:
                    return c['cm_uid'].value, False
            except Exception:
                pass
        return f"u-{uuid.uuid4().hex[:10]}", True

    def _proxy(self):
        path_only = self.path.split('?')[0].lower()
        is_asset = (
            path_only.startswith('/assets/')
            or any(path_only.endswith(ext) for ext in ('.css', '.js', '.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico', '.woff2'))
        )
        uid, is_new_uid = self._get_uid_and_is_new()
        node, is_overflow, is_overloaded, rps, reason, main_cnt, supp_cnt = pool.assign_node(uid, is_asset=is_asset)
        if node is None:
            self._send_overload_503()
            return

        url = f"https://localhost:{node['port']}{self.path}"
        t0 = time.time()
        try:
            req = urllib.request.Request(url, method=self.command)
            for h in ('Accept', 'Accept-Language', 'User-Agent'):
                v = self.headers.get(h)
                if v:
                    req.add_header(h, v)

            with urllib.request.urlopen(req, context=get_client_ctx(), timeout=5) as resp:
                body = resp.read() if self.command != 'HEAD' else b''
                latency_ms = int((time.time() - t0) * 1000)
                pool.report_ok(node['name'], latency_ms)

                ctype = resp.headers.get('Content-Type', '')
                if body and 'text/html' in ctype.lower():
                    body = self._inject_overload_widget(body, node, is_overflow, is_overloaded, rps, reason, main_cnt, supp_cnt)

                self.send_response(resp.status)
                skip = {'transfer-encoding', 'connection', 'content-length'}
                for k, v in resp.headers.items():
                    if k.lower() not in skip:
                        self.send_header(k, v)

                if is_new_uid and not is_asset:
                    self.send_header('Set-Cookie', f'cm_uid={uid}; Path=/; Max-Age={int(USER_SESSION_TTL)}')

                # LB headers — quan trọng để client biết đang nói chuyện với node nào
                self.send_header('X-LB-Node',          node['name'])
                self.send_header('X-LB-Port',          str(node['port']))
                self.send_header('X-Served-By',        node['name'])
                self.send_header('X-Latency-Ms',       str(latency_ms))
                self.send_header('X-LB-Overload',      'true' if is_overloaded else 'false')
                self.send_header('X-LB-Overflow',      'true' if is_overflow else 'false')
                self.send_header('X-LB-Main-Users',    f'{main_cnt}/{MAIN_MAX_USERS}')
                self.send_header('X-LB-Support-Users', str(supp_cnt))
                self.send_header('X-LB-RPS',           str(rps))
                if body:
                    self.send_header('Content-Length', len(body))
                self.end_headers()
                if body:
                    self.wfile.write(body)

        except Exception as e:
            pool.report_fail(node['name'])
            # Thử lại node tiếp theo ngay lập tức (tránh request bị lỗi)
            fallback = pool.next_node()
            if fallback and fallback['name'] != node['name']:
                url2 = f"https://localhost:{fallback['port']}{self.path}"
                try:
                    req2 = urllib.request.Request(url2, method=self.command)
                    with urllib.request.urlopen(req2, context=get_client_ctx(), timeout=5) as resp2:
                        body2 = resp2.read() if self.command != 'HEAD' else b''
                        ctype2 = resp2.headers.get('Content-Type', '')
                        if body2 and 'text/html' in ctype2.lower():
                            body2 = self._inject_overload_widget(body2, fallback, True, True, rps, f"{node['name']} gặp sự cố", main_cnt, supp_cnt)
                        self.send_response(resp2.status)
                        skip = {'transfer-encoding', 'connection', 'content-length'}
                        for k, v in resp2.headers.items():
                            if k.lower() not in skip:
                                self.send_header(k, v)
                        self.send_header('X-LB-Node',     fallback['name'])
                        self.send_header('X-LB-Fallback', node['name'])
                        self.send_header('X-Served-By',   fallback['name'])
                        self.send_header('X-LB-Overload', 'true')
                        if body2:
                            self.send_header('Content-Length', len(body2))
                        self.end_headers()
                        if body2:
                            self.wfile.write(body2)
                        return
                except Exception:
                    pass
            self._send_overload_503()

    def log_message(self, fmt, *args):
        pass   # Logging được xử lý trong _proxy để có màu đẹp hơn

# ─── Health Checker ───────────────────────────────────────────────────────────
def health_checker_loop():
    ctx = client_ssl_ctx()
    while True:
        for node in ALL_NODES:
            try:
                req = urllib.request.Request(
                    f"https://localhost:{node['port']}/", method='HEAD'
                )
                urllib.request.urlopen(req, context=ctx, timeout=3)
                is_healthy = True
            except Exception:
                is_healthy = False
            pool.health_update(node['name'], is_healthy)
        time.sleep(CHECK_INTERVAL)

# ─── Khởi chạy server ─────────────────────────────────────────────────────────
def run_https_server(port, handler_class, label):
    class ThreadedHTTPSServer(http.server.ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    srv = ThreadedHTTPSServer(('0.0.0.0', port), handler_class)
    ctx = server_ssl_ctx()
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(_clr(f"  ✅ {label} đang chạy tại https://localhost:{port}/", 'green'))
    srv.serve_forever()

# ─── Live stats printer ───────────────────────────────────────────────────────
def stats_printer_loop():
    """In stats phân phối tải ra terminal mỗi 5 giây."""
    time.sleep(3)  # Chờ servers khởi động
    while True:
        time.sleep(5)
        st = pool.get_stats()
        total = st['total_requests'] or 1
        main_u = st.get('main_users', 0)
        main_max = st.get('main_max_users', MAIN_MAX_USERS)
        supp_u = st.get('support_users', 0)
        print(_clr(f"\n  [{_ts()}] 📊 Trạng thái tải (Web Chính: {main_u}/{main_max} người | Web Support: {supp_u} người):", 'cyan', 'bold'))
        for name, info in st['nodes'].items():
            pct = round(info['req_total'] / total * 100)
            bar = '█' * (pct // 5) + '░' * (20 - pct // 5)
            status = _clr('✅ ONLINE ', 'green') if info['healthy'] else _clr('❌ OFFLINE', 'red')
            lat = f" {info['last_latency_ms']}ms" if info['last_latency_ms'] else ''
            print(f"    {info['icon']} {name:<22} {status} "
                  f"{_clr(bar, 'blue')} {pct:3d}% ({info['req_total']} reqs{lat})")
        print(f"    {'─'*65}")
        print(f"    Total: {total} reqs | "
              f"{st['req_per_sec']} req/s | "
              f"{len(st['active_nodes'])}/{len(ALL_NODES)} nodes active\n")

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    ensure_ssl()

    print(_clr("""
╔══════════════════════════════════════════════════════════╗
║  ⚖️   CloudMart — Load Balancer + 2 Backend Nodes       ║
║       Chống quá tải: Phân phối tải tự động             ║
╚══════════════════════════════════════════════════════════╝""", 'bold', 'cyan'))

    print(f"""
  {_clr('⚖️  Load Balancer (điểm vào duy nhất):', 'bold')}
     {_clr(f'🌐 https://localhost:{LB_PORT}/', 'cyan', 'bold')}
     Thuật toán: {_clr('Round-Robin', 'yellow')} (chia đều request sang 3 nodes)

  {_clr('Backend Nodes:', 'bold')}
     🟢 Node-1 (Main)     → https://localhost:{MAIN_PORT}/   [Tab 1]
     🔵 Node-2 (Backup-1) → https://localhost:{NODE2_PORT}/   [script này]
     🟣 Node-3 (Backup-2) → https://localhost:{NODE3_PORT}/   [script này]

  {_clr('Khi quá tải / node sập:', 'yellow')}
     • Load Balancer tự loại node chết sau {FAIL_THRESHOLD * CHECK_INTERVAL:.0f}s
     • Traffic tự động chia đều sang các node còn lại
     • Node phục hồi → tự thêm lại vào pool sau {RECOVER_THRESHOLD * CHECK_INTERVAL:.0f}s

  {_clr('Stats endpoint:', 'dim')}
     curl -k https://localhost:{LB_PORT}/lb-stats
""")

    # Khởi chạy Node-2 và Node-3
    for port, label in [(NODE2_PORT, "Node-2 (Backup-1)"),
                        (NODE3_PORT, "Node-3 (Backup-2)")]:
        handler = make_node_handler(label.split('(')[0].strip(), port)
        threading.Thread(target=run_https_server,
                         args=(port, handler, label),
                         daemon=True).start()
        time.sleep(0.3)

    # Health checker
    threading.Thread(target=health_checker_loop, daemon=True).start()

    # Stats printer
    threading.Thread(target=stats_printer_loop, daemon=True).start()

    # Load Balancer (chạy ở main thread)
    time.sleep(0.5)
    print(f"\n  {_clr('─' * 58, 'dim')}")
    print(f"  {_clr('💡 Mô phỏng quá tải: Ctrl+C ở Tab 1 để tắt Node-1', 'yellow')}")
    print(f"  {_clr('💡 Monitor: python3 scripts/ha_test.py monitor (Tab 3)', 'dim')}")
    print(f"  {_clr('─' * 58, 'dim')}\n")

    try:
        run_https_server(LB_PORT, LBHandler, "Load Balancer")
    except KeyboardInterrupt:
        print(_clr("\n  ⚠️  Load Balancer đã dừng!\n", 'yellow', 'bold'))

if __name__ == '__main__':
    main()
