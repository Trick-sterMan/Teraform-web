#!/usr/bin/env python3
"""
==============================================================================
HA_TEST.PY - Script kiem tra failover Active-Passive (moi truong LOCAL)
De tai: Can bang tai dua tren noi dung HTTPS voi Terraform
==============================================================================
Chuc nang:
  1. Vong lap theo doi: in gio, ma HTTP, header X-Served-By moi 2 giay
  2. Load test vao ALB CHINH (cong 8443) bang nhieu thread dong thoi
  3. Do thoi gian: phat hien, chuyen link, quay ve
  4. Phuong an du phong: huong dan dung "systemctl stop nginx" tren AWS
                         hoac tat tien trinh Python tren local

Su dung:
  python scripts/ha_test.py [lenh]

  Cac lenh:
    monitor   - Theo doi trang thai failover moi 2 giay (mac dinh)
    loadtest  - Load test vao ALB chinh (tao qua tai)
    dig       - Kiem tra DNS/routing (Windows: dung nslookup thay dig)
    full      - Chay ca monitor + loadtest dong thoi
    measure   - Do thoi gian failover tu dong
==============================================================================
"""

import sys
import time
import threading
import ssl
import urllib.request
import urllib.error
import subprocess
import os
import datetime
import statistics

# --- Cau hinh cong (dong bo voi run_ha_local.py) ---
ENTRY_PORT   = 7443   # Diem vao duy nhat (HAProxy Python)
PRIMARY_PORT = 8443   # ALB chinh
BACKUP_PORT  = 9443   # ALB backup

# --- Cau hinh load test ---
LOAD_THREADS    = 50    # So luong ket noi dong thoi
LOAD_REQUESTS   = 500   # Tong so request
LOAD_TARGET     = f"https://localhost:{PRIMARY_PORT}"  # Ban vao ALB CHINH (khong qua HA)

# --- SSL context bo qua self-signed cert ---
def make_ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx

SSL_CTX = make_ssl_ctx()

# =============================================================================
# MODULE 1: VONG LAP THEO DOI
# =============================================================================
def get_status(url, timeout=3):
    """
    Lay ma HTTP va header X-Served-By tu mot URL.
    Tra ve (ma_http, x_served_by, ha_active_node) hoac ("ERR", "?", "?") neu loi.
    """
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            code = resp.getcode()
            served_by  = resp.headers.get("X-Served-By",    "-")
            ha_node    = resp.headers.get("X-HA-Active-Node", "-")
            alb_rule   = resp.headers.get("X-ALB-Rule",     "-")
            return code, served_by, ha_node, alb_rule
    except urllib.error.HTTPError as e:
        return e.code, "?", "?", "?"
    except Exception:
        return "ERR", "?", "?", "?"


def monitor_loop(stop_event=None, results_list=None):
    """
    Vong lap theo doi moi 2 giay:
      - Thoi gian
      - Ma HTTP qua Entry Point (7443) - giao dien nguoi dung thuc te
      - Ma HTTP truc tiep Primary (8443) - kiem tra suc khoe ALB chinh
      - Header X-Served-By: primary / backup
      - X-HA-Active-Node: PRIMARY / BACKUP
    """
    print()
    print("=" * 90)
    print("THEO DOI TRANG THAI FAILOVER (Ctrl+C de dung)")
    print("-" * 90)
    print(f"{'Thoi gian':<12} | {'Entry:7443':>12} | {'X-Served-By':>14} | {'HA-Node':>10} | {'Primary:8443':>14} | Ghi chu")
    print("-" * 90)

    prev_served_by = None

    while True:
        ts = datetime.datetime.now().strftime("%H:%M:%S")

        # Lay trang thai tu Entry Point (7443)
        code_e, served_by, ha_node, alb_rule = get_status(f"https://localhost:{ENTRY_PORT}/")

        # Kiem tra truc tiep ALB chinh (8443)
        code_p, _, _, _ = get_status(f"https://localhost:{PRIMARY_PORT}/")

        # Phat hien su kien failover / failback
        note = ""
        if prev_served_by is not None and prev_served_by != served_by:
            if served_by == "backup":
                note = "*** FAILOVER -> BACKUP ***"
            elif served_by == "-":
                note = "PRIMARY (direct)"
            else:
                note = "*** FAILBACK -> PRIMARY ***"
        prev_served_by = served_by

        status_e = f"{code_e:>3}" if isinstance(code_e, int) else "ERR"
        status_p = f"{code_p:>3}" if isinstance(code_p, int) else "ERR"

        # To mau cho ham cuoi (console khong to mau tren Windows CMD, dung plaintext)
        line = f"{ts:<12} | {status_e:>12} | {served_by:>14} | {ha_node:>10} | {status_p:>14} | {note}"
        print(line)

        if results_list is not None:
            results_list.append({
                "ts": ts, "code_entry": code_e, "served_by": served_by,
                "ha_node": ha_node, "code_primary": code_p
            })

        if stop_event and stop_event.is_set():
            break

        time.sleep(2)


# =============================================================================
# MODULE 2: LOAD TEST VAO ALB CHINH (cong 8443)
# =============================================================================
_load_lock   = threading.Lock()
_load_ok     = 0
_load_err    = 0
_load_times  = []

def _single_request(path="/"):
    global _load_ok, _load_err
    t0 = time.time()
    try:
        url = f"{LOAD_TARGET}{path}"
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=5, context=SSL_CTX) as resp:
            resp.read()
            with _load_lock:
                _load_ok += 1
                _load_times.append(time.time() - t0)
    except Exception:
        with _load_lock:
            _load_err += 1


def run_loadtest(n_threads=LOAD_THREADS, n_requests=LOAD_REQUESTS):
    """
    Load test: ban n_requests request vao ALB CHINH (8443) qua n_threads thread.
    Muc dich: lam qua tai ALB chinh de kich hoat failover (gia lap tren local).

    Luu y thuc te:
      - Tren local (Python server), server Python co the bi block do GIL.
      - Neu muon gia lap sap hoan toan: Ctrl+C tren terminal run_local_demo.py
        hoac chay: scripts/ha_test.py --stop-primary
    """
    global _load_ok, _load_err, _load_times
    _load_ok = _load_err = 0
    _load_times = []

    paths = ["/", "/products/", "/checkout/"]

    print()
    print("=" * 60)
    print(f"LOAD TEST -> ALB CHINH {LOAD_TARGET}")
    print(f"Threads: {n_threads} | Requests: {n_requests}")
    print("=" * 60)

    t_start = time.time()
    threads = []
    for i in range(n_requests):
        path = paths[i % len(paths)]
        t = threading.Thread(target=_single_request, args=(path,), daemon=True)
        threads.append(t)

    # Chay theo lo n_threads
    for i in range(0, len(threads), n_threads):
        batch = threads[i:i + n_threads]
        for t in batch:
            t.start()
        for t in batch:
            t.join(timeout=8)

    elapsed = time.time() - t_start
    rps = (_load_ok + _load_err) / elapsed if elapsed > 0 else 0
    avg_ms = statistics.mean(_load_times) * 1000 if _load_times else 0

    print(f"\n--- Ket qua Load Test ---")
    print(f"  Thanh cong   : {_load_ok}")
    print(f"  That bai     : {_load_err}")
    print(f"  Tong thoi gian: {elapsed:.1f}s | RPS: {rps:.1f}")
    print(f"  Latency TB   : {avg_ms:.1f}ms")
    print()
    print(">>> Neu load test khong du manh de lam sap Python server:")
    print("    Phuong an B: Mo terminal chay run_local_demo.py -> Nhan Ctrl+C")
    print("    Phuong an C (AWS): ssh vao EC2 primary -> sudo systemctl stop nginx")


# =============================================================================
# MODULE 3: KIEM TRA DNS (thay dig bang nslookup tren Windows)
# =============================================================================
def run_dig():
    """
    Kiem tra DNS resolution (dung nslookup tren Windows thay cho dig).
    Trong moi truong local, ALB chinh co the truy cap qua localhost:8443.
    """
    print()
    print("=" * 60)
    print("KIEM TRA DNS / ROUTING")
    print("=" * 60)
    print()
    print("Luu y moi truong LOCAL:")
    print("  - Khong co Route 53 that -> dung direct URL thay CNAME")
    print("  - Entry Point : https://localhost:7443/  (HAProxy Python)")
    print("  - Primary ALB : https://localhost:8443/  (run_local_demo.py)")
    print("  - Backup  ALB : https://localhost:9443/  (run_ha_local.py)")
    print()

    # Gia lap lenh dig bang nslookup
    try:
        result = subprocess.run(["nslookup", "localhost"], capture_output=True, text=True, timeout=5)
        print(">>> nslookup localhost:")
        print(result.stdout)
    except Exception as e:
        print(f"nslookup loi: {e}")

    # Hien thi routing hien tai bang curl (Windows: dung curl neu co)
    print()
    print("Lenh kiem tra routing thu cong (chay tren terminal):")
    print(f"  curl -k -s -I https://localhost:{ENTRY_PORT}/         | Qua HA Entry Point")
    print(f"  curl -k -s -I https://localhost:{ENTRY_PORT}/products/ | Products qua HA")
    print(f"  curl -k -s -I https://localhost:{ENTRY_PORT}/checkout/ | Checkout qua HA")
    print()
    print("Xem header X-HA-Active-Node va X-Served-By de biet dang dung server nao.")


# =============================================================================
# MODULE 4: DO THOI GIAN FAILOVER
# =============================================================================
def measure_failover():
    """
    Do thoi gian failover tu dong:
      t0: Bat dau (ALB chinh hoat dong binh thuong)
      t1: Lan dau X-Served-By doi tu primary/- sang backup
      t2: Request dau tien qua backup thanh cong
      (failback do tu tay)
    """
    print()
    print("=" * 70)
    print("DO THOI GIAN FAILOVER")
    print("-" * 70)
    print("BUOC 1: Dung ALB chinh (Ctrl+C tren terminal run_local_demo.py)")
    print("        hoac tren AWS: ssh EC2 primary -> sudo systemctl stop nginx")
    print()
    input("Nhan Enter khi san sang bat dau do thoi gian failover...")
    print()

    t0 = time.time()
    t0_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[t0 = {t0_str}] Bat dau do. TAT ALB CHINH NGAY BAY GIO!")
    print()

    t1 = t2 = None
    t1_str = t2_str = "?"
    prev_code = None

    for i in range(60):   # Theo doi toi da 120 giay (60 chu ky * 2s)
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        code_e, served_by, ha_node, _ = get_status(f"https://localhost:{ENTRY_PORT}/")

        print(f"  [{ts}] Entry:{code_e} | X-Served-By:{served_by} | HA-Node:{ha_node}")

        if t1 is None and served_by == "backup":
            t1 = time.time()
            t1_str = ts
            print(f"\n  [t1 = {t1_str}] *** PHAT HIEN FAILOVER! Chuyen sang BACKUP ***")
            print(f"  Thoi gian phat hien: {t1 - t0:.1f}s\n")

        if t1 is not None and t2 is None and isinstance(code_e, int) and 200 <= code_e < 400:
            t2 = time.time()
            t2_str = ts
            print(f"\n  [t2 = {t2_str}] *** REQUEST THANH CONG QUA BACKUP! ***")
            print(f"  Thoi gian chuyen link: {t2 - t0:.1f}s")
            break

        time.sleep(2)

    print()
    print("-" * 70)
    print("BUOC 2: Khoi dong lai ALB chinh de do thoi gian FAILBACK")
    print("        (Chay lai run_local_demo.py hoac: sudo systemctl start nginx)")
    print()
    input("Nhan Enter khi da khoi dong lai ALB chinh...")
    print()

    t3 = None
    t3_str = "?"
    for i in range(30):
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        code_e, served_by, ha_node, _ = get_status(f"https://localhost:{ENTRY_PORT}/")
        print(f"  [{ts}] Entry:{code_e} | X-Served-By:{served_by} | HA-Node:{ha_node}")

        if served_by not in ("backup", "?", "-") and t2 is not None:
            t3 = time.time()
            t3_str = ts
            print(f"\n  [t3 = {t3_str}] *** FAILBACK THANH CONG! Quay ve PRIMARY ***")
            break
        time.sleep(2)

    print()
    print("=" * 70)
    print("BANG KET QUA THOI GIAN FAILOVER")
    print("=" * 70)
    print(f"  t0 (bat dau tan cong)         : {t0_str}")
    print(f"  t1 (health check Unhealthy)    : {t1_str}  | +{(t1-t0):.1f}s" if t1 else "  t1: Chua phat hien")
    print(f"  t2 (chuyen sang backup xong)   : {t2_str}  | +{(t2-t0):.1f}s" if t2 else "  t2: Chua hoan thanh")
    print(f"  t3 (quay ve primary xong)      : {t3_str}  | +{(t3-t2):.1f}s" if (t3 and t2) else "  t3: Chua hoan thanh")
    print()
    if t1 and t2:
        print(f"  Thoi gian phat hien su co    : {t1-t0:.1f}s  (fall={2}*interval={2}s = {2*2}s ly thuyet)")
        print(f"  Thoi gian chuyen link        : {t2-t0:.1f}s  (phat hien + proxy switch)")
    if t2 and t3:
        print(f"  Thoi gian khoi phuc (RTO)    : {t3-t2:.1f}s  (rise={2}*interval={2}s = {2*2}s ly thuyet)")
    print("=" * 70)
    print()
    print("BANG MAU BIET QUA TEST (dung cho bao cao):")
    print("-" * 70)
    print(f"| Su kien                     | Thoi gian tuyet doi | Delta    |")
    print(f"|-----------------------------|---------------------|----------|")
    print(f"| t0: Bat dau tan cong ALB    | {t0_str:<19} | +0.0s    |")
    if t1: print(f"| t1: Health check Unhealthy  | {t1_str:<19} | +{t1-t0:.1f}s   |")
    if t2: print(f"| t2: Chuyen sang backup      | {t2_str:<19} | +{t2-t0:.1f}s   |")
    if t3: print(f"| t3: Quay ve primary (RTO)   | {t3_str:<19} | +{t3-t2:.1f}s (tu t2)|")
    print("-" * 70)


# =============================================================================
# MAIN
# =============================================================================
def print_help():
    print(__doc__)
    print("Vi du:")
    print("  python scripts/ha_test.py monitor    # Theo doi")
    print("  python scripts/ha_test.py loadtest   # Load test ALB chinh")
    print("  python scripts/ha_test.py full       # Monitor + loadtest dong thoi")
    print("  python scripts/ha_test.py measure    # Do thoi gian failover")
    print("  python scripts/ha_test.py dig        # Kiem tra DNS/routing")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "monitor"

    print()
    print("=" * 70)
    print("HA TEST - KIEM TRA FAILOVER ACTIVE-PASSIVE")
    print(f"Entry Point : https://localhost:{ENTRY_PORT}/")
    print(f"Primary ALB : https://localhost:{PRIMARY_PORT}/")
    print(f"Backup  ALB : https://localhost:{BACKUP_PORT}/")
    print("=" * 70)

    try:
        if cmd == "monitor":
            monitor_loop()

        elif cmd == "loadtest":
            run_loadtest()

        elif cmd == "dig":
            run_dig()

        elif cmd == "measure":
            measure_failover()

        elif cmd == "full":
            # Chay monitor va loadtest dong thoi
            stop_evt = threading.Event()
            results  = []
            t_mon = threading.Thread(target=monitor_loop, args=(stop_evt, results), daemon=True)
            t_mon.start()

            time.sleep(3)  # Cho monitor hien thi vai dong truoc
            run_loadtest()

            print()
            print("Load test xong. Tiep tuc theo doi 10 giay...")
            time.sleep(10)
            stop_evt.set()

        else:
            print_help()

    except KeyboardInterrupt:
        print("\nDa dung.")
        sys.exit(0)
