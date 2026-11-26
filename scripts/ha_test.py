#!/usr/bin/env python3
"""
CloudMart — HA Monitor Dashboard

Usage:
  python3 scripts/ha_test.py monitor   — Live dashboard (Tab 3)
  python3 scripts/ha_test.py curl      — Xem LB headers
  python3 scripts/ha_test.py once      — Check 1 lần
  python3 scripts/ha_test.py stress N  — Gửi N request liên tiếp để test phân phối

Tab 3: python3 scripts/ha_test.py monitor
"""

import sys
import ssl
import time
import json
import urllib.request
import threading
from datetime import datetime

# ─── Endpoints ────────────────────────────────────────────────────────────────
LB_URL     = "https://localhost:7443"
MAIN_URL   = "https://localhost:8443"
NODE2_URL  = "https://localhost:9443"
NODE3_URL  = "https://localhost:9444"
STATS_URL  = f"{LB_URL}/lb-stats"

REFRESH_SEC = 2

# ─── Colors ───────────────────────────────────────────────────────────────────
C = {
    'green':   '\033[92m', 'yellow': '\033[93m', 'red':     '\033[91m',
    'blue':    '\033[94m', 'cyan':   '\033[96m', 'magenta': '\033[95m',
    'bold':    '\033[1m',  'dim':    '\033[2m',  'reset':   '\033[0m',
}
def clr(t, *cs): return ''.join(C[c] for c in cs if c in C) + str(t) + C['reset']
def ts(): return datetime.now().strftime('%H:%M:%S')

# ─── SSL ──────────────────────────────────────────────────────────────────────
def _ctx():
    c = ssl.create_default_context()
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    return c

CTX = _ctx()

def fetch(url, timeout=3, method='GET'):
    try:
        t0 = time.time()
        req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            ms = int((time.time() - t0) * 1000)
            body = r.read()
            return r.status, dict(r.headers), body, ms
    except Exception as e:
        return None, {}, b'', None

def fetch_stats():
    """Lấy JSON stats từ /lb-stats endpoint."""
    st, h, body, ms = fetch(STATS_URL)
    if st and body:
        try:
            return json.loads(body.decode())
        except Exception:
            pass
    return None

# ─── Bar chart ────────────────────────────────────────────────────────────────
def bar(pct, width=20):
    filled = int(pct / 100 * width)
    return clr('█' * filled, 'blue') + clr('░' * (width - filled), 'dim')

def status_badge(healthy, ms=None):
    if healthy:
        lat = clr(f" {ms}ms", 'dim') if ms else ''
        return clr('● ONLINE', 'green', 'bold') + lat
    return clr('● OFFLINE', 'red', 'bold')

# ─── Monitor ──────────────────────────────────────────────────────────────────
def monitor():
    iteration = 0
    prev_events_count = 0

    print(clr("""
╔══════════════════════════════════════════════════════════╗
║  📊  CloudMart Load Balancer Monitor  (cập nhật 2s)    ║
╚══════════════════════════════════════════════════════════╝
""", 'bold', 'cyan'))
    time.sleep(0.5)

    while True:
        now = ts()
        iteration += 1
        stats = fetch_stats()

        # Check LB health
        lb_st, lb_h, _, lb_ms = fetch(LB_URL + '/', method='HEAD')

        print('\033[2J\033[H', end='')   # clear + home

        W = 60

        # ── Header ────────────────────────────────────────────────────────────
        print(clr(f"  ╔{'═' * W}╗", 'cyan'))
        title = f"  📊  CloudMart LB Monitor  [{now}]  #iter {iteration}"
        print(clr(f"  ║{title:<{W+1}}║", 'cyan', 'bold'))
        print(clr(f"  ╚{'═' * W}╝\n", 'cyan'))

        # ── Load Balancer status ───────────────────────────────────────────────
        lb_ok = lb_st is not None
        print(clr("  ┌─── ⚖️  Load Balancer (Điểm Vào) ─────────────────────┐", 'magenta'))
        print(clr("  │  ", 'magenta') + f"{clr('🌐 ' + LB_URL + '/', 'bold')}  {status_badge(lb_ok, lb_ms)}")
        if stats:
            active_n = len(stats.get('active_nodes', []))
            total_n  = active_n + len(stats.get('inactive_nodes', []))
            rps = stats.get('req_per_sec', 0)
            total_r = stats.get('total_requests', 0)
            uptime = stats.get('uptime_sec', 0)
            is_overloaded = stats.get('is_overloaded', False)
            reason = stats.get('overload_reason', '')
            print(clr("  │  ", 'magenta') +
                  f"Thuật toán: {clr('Round-Robin', 'yellow', 'bold')}  "
                  f"| Nodes: {clr(f'{active_n}/{total_n} active', 'green' if active_n == total_n else 'yellow')}")
            print(clr("  │  ", 'magenta') +
                  f"Total reqs: {clr(str(total_r), 'bold')}  "
                  f"| {clr(str(rps) + ' req/s', 'red' if is_overloaded else 'cyan')}  "
                  f"| Uptime: {uptime}s")
        else:
            is_overloaded = False
            reason = ''
            print(clr("  │  ", 'magenta') + clr("  Chờ load balancer khởi động...", 'dim'))
        print(clr("  └" + "─" * W + "┘\n", 'magenta'))

        if is_overloaded:
            print(clr("  ┌─── 🚨 CẢNH BÁO QUÁ TẢI HỆ THỐNG ────────────────────┐", 'red', 'bold'))
            print(clr("  │  ", 'red') + clr(f"🔥 {reason or 'Lưu lượng vượt ngưỡng'}", 'yellow', 'bold'))
            print(clr("  │  ", 'red') + clr("→ Đang tự động chia tải & bật thông báo trên web!", 'red', 'bold'))
            print(clr("  └" + "─" * W + "┘\n", 'red', 'bold'))

        # ── Backend Nodes ──────────────────────────────────────────────────────
        print(clr("  ┌─── 🖥  Backend Nodes (phân phối tải) ─────────────────┐", 'blue'))
        if stats:
            nodes_data = stats.get('nodes', {})
            total_reqs = stats.get('total_requests', 1) or 1

            for name, info in nodes_data.items():
                pct  = round(info['req_total'] / total_reqs * 100)
                icon = info.get('icon', '◉')
                ok   = info.get('healthy', False)
                lat  = info.get('last_latency_ms')
                reqs = info['req_total']

                badge = status_badge(ok, lat)
                b = bar(pct)
                ok_cnt  = info.get('req_ok', 0)
                fail_cnt= info.get('req_fail', 0)

                print(clr("  │  ", 'blue') +
                      f"{icon} {clr(name, 'bold'):<28} {badge}")
                print(clr("  │      ", 'blue') +
                      f"{b} {pct:3d}%  {clr(str(reqs), 'bold')} reqs"
                      + (clr(f"  ({fail_cnt} fail)", 'red') if fail_cnt > 0 else ''))
        else:
            # Fallback: check each node directly
            for label, url in [("Node-1 (Main)     port 8443", MAIN_URL),
                                ("Node-2 (Backup-1) port 9443", NODE2_URL),
                                ("Node-3 (Backup-2) port 9444", NODE3_URL)]:
                st, h, _, ms = fetch(url + '/', method='HEAD')
                print(clr("  │  ", 'blue') + f"  {label}: {status_badge(st is not None, ms)}")
        print(clr("  └" + "─" * W + "┘\n", 'blue'))

        # ── Traffic flow ──────────────────────────────────────────────────────
        if stats:
            active = stats.get('active_nodes', [])
            if len(active) == 3:
                flow = clr("User → [7443 LB] → Node-1 / Node-2 / Node-3  ✅ Full", 'green')
            elif len(active) == 2:
                flow = clr(f"User → [7443 LB] → {' / '.join(a.split('(')[0].strip() for a in active)}  ⚠️ 1 node down", 'yellow', 'bold')
            elif len(active) == 1:
                flow = clr(f"User → [7443 LB] → {active[0]}  🔴 2 nodes down!", 'red', 'bold')
            else:
                flow = clr("User → [7443 LB] → ❌ Tất cả nodes offline!", 'red', 'bold')
        else:
            flow = clr("Load Balancer chưa sẵn sàng...", 'dim')

        print(f"  📡 {clr('Luồng traffic:', 'bold')}")
        print(f"     {flow}\n")

        # ── Lịch sử sự kiện ───────────────────────────────────────────────────
        if stats:
            events = stats.get('events', [])
            if events:
                print(clr("  📋 Sự kiện gần đây:", 'bold'))
                for ev in events[-6:]:
                    t = ev.get('type', '')
                    c = 'red' if 'DOWN' in t else ('green' if 'RECOVER' in t else 'yellow')
                    print(f"     {clr('[' + ev['time'] + ']', 'dim')} {clr(ev['msg'], c)}")
                print()

        # ── Hints ─────────────────────────────────────────────────────────────
        print(clr("  💡 Stress test: python3 scripts/ha_test.py stress 50", 'dim'))
        print(clr("  💡 Header check: curl -k -s -I https://localhost:7443/ | grep X-LB", 'dim'))
        print(clr("  💡 Mô phỏng quá tải: Ctrl+C ở Tab 1 để tắt Node-1", 'yellow'))
        print()
        print(clr(f"  ⏱  Cập nhật mỗi {REFRESH_SEC}s | Ctrl+C để dừng", 'dim'))

        time.sleep(REFRESH_SEC)

# ─── Curl test ────────────────────────────────────────────────────────────────
def curl_test():
    print(clr("\n📡 Kiểm tra LB Headers:\n", 'cyan', 'bold'))
    for _ in range(6):
        st, h, _, ms = fetch(LB_URL + '/')
        if st:
            node = h.get('X-LB-Node', h.get('X-Served-By', '?'))
            port = h.get('X-LB-Port', '?')
            lat  = h.get('X-Latency-Ms', '?')
            print(f"  {clr('✅', 'green')} → {clr(node, 'bold')} (port {port})  "
                  f"{clr(lat + 'ms', 'dim')}")
        else:
            print(f"  {clr('❌ Không kết nối được', 'red')}")
        time.sleep(0.3)
    print()

# ─── Stress test ──────────────────────────────────────────────────────────────
def stress_test(n):
    n = int(n)
    print(clr(f"\n🔥 Stress test: gửi {n} requests lên Load Balancer...\n", 'yellow', 'bold'))
    counts = {}
    errors = 0
    times  = []
    lock   = threading.Lock()

    def send_one():
        nonlocal errors
        st, h, _, ms = fetch(LB_URL + '/')
        with lock:
            if st:
                node = h.get('X-LB-Node', h.get('X-Served-By', 'unknown'))
                counts[node] = counts.get(node, 0) + 1
                if ms:
                    times.append(ms)
            else:
                errors += 1

    threads = [threading.Thread(target=send_one) for _ in range(n)]
    t0 = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.time() - t0

    total = sum(counts.values())
    print(clr(f"  Kết quả ({elapsed:.2f}s):\n", 'bold'))
    for node, cnt in sorted(counts.items()):
        pct = round(cnt / max(total, 1) * 100)
        print(f"  {bar(pct, 15)}  {clr(node, 'bold')}: {cnt} reqs ({pct}%)")
    if errors:
        print(f"\n  {clr(f'Lỗi: {errors}', 'red')}")
    if times:
        avg_ms = round(sum(times) / len(times))
        print(f"\n  {clr(f'Avg latency: {avg_ms}ms | Total: {total} ok / {errors} fail', 'dim')}")
    print()

# ─── Once ─────────────────────────────────────────────────────────────────────
def once():
    print(clr("\n📊 Kiểm tra nhanh:\n", 'bold'))
    stats = fetch_stats()
    if stats:
        total = stats.get('total_requests', 0)
        active = stats.get('active_nodes', [])
        print(f"  LB online | {len(active)}/{len(stats.get('nodes', {}))} nodes active | {total} total reqs")
        for name, info in stats.get('nodes', {}).items():
            badge = clr('✅', 'green') if info['healthy'] else clr('❌', 'red')
            print(f"  {badge} {name}: {info['req_total']} reqs")
    else:
        # Direct check
        for label, url in [("LB     7443", LB_URL), ("Node-1 8443", MAIN_URL),
                            ("Node-2 9443", NODE2_URL), ("Node-3 9444", NODE3_URL)]:
            st, h, _, ms = fetch(url + '/', method='HEAD')
            print(f"  {label}: {status_badge(st is not None, ms)}")
    print()

# ─── Entry ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'monitor'

    if cmd == 'monitor':
        try:
            monitor()
        except KeyboardInterrupt:
            print(clr("\n\n  Monitor dừng.\n", 'yellow'))
    elif cmd == 'curl':
        curl_test()
    elif cmd == 'stress':
        n = sys.argv[2] if len(sys.argv) > 2 else '30'
        stress_test(n)
    elif cmd == 'once':
        once()
    else:
        print(f"""
{clr('CloudMart HA Monitor', 'bold', 'cyan')}

  {clr('python3 scripts/ha_test.py monitor', 'green')}         — Live dashboard (Tab 3)
  {clr('python3 scripts/ha_test.py curl', 'green')}            — Xem LB headers (6 requests)
  {clr('python3 scripts/ha_test.py stress 100', 'green')}      — Gửi 100 requests đồng thời
  {clr('python3 scripts/ha_test.py once', 'green')}            — Check 1 lần rồi thoát
""")
