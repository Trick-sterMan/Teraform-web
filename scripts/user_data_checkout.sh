#!/bin/bash
# ==============================================================================
# Script khởi tạo Checkout Server (Trang thanh toán) - Tích hợp đầy đủ cổng thanh toán thực tế
# ==============================================================================
set -e

dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx

mkdir -p /var/www/html/checkout
mkdir -p /usr/share/nginx/html/checkout

cat << 'EOF' > /var/www/html/checkout/index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cổng Thanh Toán Trực Tuyến An Toàn | CloudMart</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #7c3aed;
            --primary-hover: #6d28d9;
            --secondary: #0f172a;
            --accent: #f59e0b;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --success: #10b981;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }

        /* Top Announcement Bar */
        .top-bar { background: #4c1d95; color: #ede9fe; font-size: 0.8rem; padding: 0.5rem 1.5rem; display: flex; justify-content: space-between; align-items: center; }
        .top-bar strong { color: #fff; }
        .top-links a { color: #ede9fe; text-decoration: none; margin-left: 1rem; }

        /* Cloud System Monitor Badge Bar */
        .cloud-badge-bar { background: linear-gradient(90deg, #5b21b6, #7c3aed); color: white; padding: 0.55rem 1.5rem; font-size: 0.85rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.15); }
        .cloud-badge-bar .sys-info { display: flex; gap: 1rem; align-items: center; }
        .cloud-pill { background: rgba(255,255,255,0.2); padding: 0.2rem 0.65rem; border-radius: 9999px; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 0.35rem; }
        .cloud-pill .dot { width: 7px; height: 7px; border-radius: 50%; background: #c4b5fd; display: inline-block; box-shadow: 0 0 8px #c4b5fd; }

        /* Main Navigation */
        header { background: var(--card-bg); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; box-shadow: var(--shadow-sm); }
        .nav-container { max-width: 1240px; margin: 0 auto; padding: 0.9rem 1.5rem; display: flex; align-items: center; justify-content: space-between; }
        .brand-logo { font-size: 1.5rem; font-weight: 800; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }
        .brand-logo span { color: var(--secondary); }
        .secure-badge { display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; color: #059669; font-weight: 700; background: #ecfdf5; padding: 0.4rem 0.85rem; border-radius: 9999px; }

        /* Stepper */
        .stepper-container { max-width: 900px; margin: 2rem auto 0; padding: 0 1.5rem; }
        .stepper { display: flex; justify-content: space-between; position: relative; }
        .stepper::before { content: ""; position: absolute; top: 20px; left: 50px; right: 50px; height: 2px; background: #e2e8f0; z-index: 1; }
        .step-item { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; }
        .step-num { width: 42px; height: 42px; border-radius: 50%; background: white; border: 2px solid #e2e8f0; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.95rem; color: var(--text-muted); margin-bottom: 0.5rem; }
        .step-item.completed .step-num { background: #10b981; border-color: #10b981; color: white; }
        .step-item.active .step-num { background: var(--primary); border-color: var(--primary); color: white; box-shadow: 0 0 0 4px rgba(124,58,237,0.2); }
        .step-label { font-size: 0.85rem; font-weight: 700; color: var(--text-muted); }
        .step-item.active .step-label { color: var(--primary); }

        /* Checkout Layout */
        .checkout-container { max-width: 1240px; margin: 2rem auto 3rem; padding: 0 1.5rem; display: grid; grid-template-columns: 1.35fr 1fr; gap: 2.5rem; align-items: start; }

        /* Left Column: Form Cards */
        .checkout-box { background: white; border: 1px solid var(--border); border-radius: 18px; padding: 2rem; box-shadow: var(--shadow-sm); margin-bottom: 1.5rem; }
        .box-title { font-size: 1.25rem; font-weight: 800; color: var(--secondary); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.6rem; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        .form-group { margin-bottom: 1rem; }
        .form-group.full { grid-column: span 2; }
        .form-label { display: block; font-size: 0.85rem; font-weight: 700; color: #334155; margin-bottom: 0.4rem; }
        .form-input { width: 100%; padding: 0.75rem 1rem; border-radius: 10px; border: 1.5px solid var(--border); outline: none; font-size: 0.95rem; font-family: inherit; transition: 0.2s; background: #f8fafc; }
        .form-input:focus { border-color: var(--primary); background: #fff; box-shadow: 0 0 0 4px rgba(124,58,237,0.1); }

        /* Payment Methods Accordion */
        .payment-options { display: flex; flex-direction: column; gap: 0.85rem; }
        .payment-card { border: 1.5px solid var(--border); border-radius: 14px; overflow: hidden; transition: 0.2s; }
        .payment-card.active { border-color: var(--primary); box-shadow: 0 0 0 2px rgba(124,58,237,0.15); }
        .payment-header { padding: 1.1rem 1.25rem; display: flex; align-items: center; justify-content: space-between; cursor: pointer; background: #fff; }
        .payment-card.active .payment-header { background: #faf5ff; }
        .payment-info { display: flex; align-items: center; gap: 0.85rem; font-size: 0.95rem; font-weight: 700; color: var(--secondary); }
        .payment-badge { font-size: 0.75rem; background: #ede9fe; color: var(--primary); padding: 0.25rem 0.6rem; border-radius: 6px; font-weight: 700; }
        .payment-body { padding: 1.25rem; border-top: 1px solid var(--border); background: #f8fafc; display: none; }
        .payment-card.active .payment-body { display: block; }

        /* VietQR Box Details */
        .vietqr-box { display: flex; gap: 1.5rem; align-items: center; background: white; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 1.25rem; }
        .qr-image-wrapper { width: 140px; height: 140px; background: white; border: 1px solid #cbd5e1; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }
        .qr-placeholder { font-size: 4.5rem; line-height: 1; }
        .qr-badge-sub { font-size: 0.7rem; font-weight: 800; color: #dc2626; margin-top: 0.2rem; }
        .qr-details-table { width: 100%; font-size: 0.85rem; }
        .qr-details-table td { padding: 0.35rem 0; }
        .qr-details-table td:first-child { color: var(--text-muted); width: 40%; }
        .qr-details-table td:last-child { font-weight: 700; color: var(--secondary); }
        .copy-pill { font-size: 0.7rem; background: #ede9fe; color: var(--primary); border: none; padding: 0.2rem 0.5rem; border-radius: 4px; cursor: pointer; font-weight: 700; margin-left: 0.4rem; }

        /* Credit Card Inputs */
        .credit-card-preview { background: linear-gradient(135deg, #1e1b4b, #4338ca); color: white; border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem; width: 100%; max-width: 320px; font-family: monospace; box-shadow: var(--shadow-md); }
        .cc-chip { font-size: 1.5rem; margin-bottom: 1rem; }
        .cc-number { font-size: 1.15rem; letter-spacing: 2px; margin-bottom: 1rem; }
        .cc-bottom { display: flex; justify-content: space-between; font-size: 0.8rem; }

        /* Right Column: Order Summary Card */
        .summary-card { background: white; border: 1px solid var(--border); border-radius: 18px; padding: 2rem; box-shadow: var(--shadow-sm); position: sticky; top: 90px; }
        .summary-title { font-size: 1.25rem; font-weight: 800; color: var(--secondary); margin-bottom: 1.5rem; }
        .cart-item { display: flex; align-items: center; gap: 1rem; padding-bottom: 1rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border); }
        .cart-thumb { width: 60px; height: 60px; background: #f8fafc; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; border: 1px solid var(--border); }
        .cart-details { flex: 1; }
        .cart-name { font-size: 0.9rem; font-weight: 700; color: var(--secondary); margin-bottom: 0.25rem; }
        .cart-meta { font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.6rem; margin-top: 0.2rem; }
        .qty-btn { background: #e2e8f0; border: none; width: 22px; height: 22px; border-radius: 4px; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; }
        .cart-price { font-weight: 800; font-size: 0.95rem; color: #0f172a; }

        /* Promo Box */
        .promo-box { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }
        .promo-input { flex: 1; padding: 0.7rem 1rem; border-radius: 8px; border: 1.5px solid var(--border); outline: none; font-size: 0.875rem; text-transform: uppercase; font-weight: 700; }
        .btn-apply { background: var(--secondary); color: white; border: none; padding: 0 1.2rem; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 0.875rem; }

        /* Price Calculation */
        .calc-row { display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-size: 0.9rem; color: #475569; }
        .calc-row.discount { color: #10b981; font-weight: 600; }
        .calc-row.total { font-size: 1.35rem; font-weight: 800; color: var(--secondary); border-top: 2px dashed var(--border); padding-top: 1rem; margin-top: 1rem; }
        .calc-row.total span:last-child { color: var(--primary); }

        .btn-submit-order { width: 100%; background: linear-gradient(135deg, #7c3aed, #6d28d9); color: white; border: none; padding: 1.1rem; border-radius: 12px; font-size: 1.1rem; font-weight: 800; cursor: pointer; margin-top: 1.5rem; transition: 0.25s; box-shadow: 0 10px 15px -3px rgba(124,58,237,0.3); display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
        .btn-submit-order:hover { transform: translateY(-2px); box-shadow: 0 15px 20px -3px rgba(124,58,237,0.4); }

        /* VAT Box */
        .vat-toggle { margin-top: 1.25rem; padding-top: 1.25rem; border-top: 1px dashed var(--border); font-size: 0.85rem; color: #475569; }

        /* Architecture Banner */
        .arch-banner { background: #0f172a; border-radius: 18px; padding: 1.5rem 2rem; color: #94a3b8; margin-top: 2rem; border: 1px solid #334155; }
        .arch-banner h3 { color: #f8fafc; font-size: 1.1rem; margin-bottom: 0.4rem; }
        .arch-banner p { font-size: 0.85rem; line-height: 1.5; }

        /* Success Modal */
        .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; z-index: 100; }
        .modal-card { background: white; border-radius: 20px; padding: 2.5rem; max-width: 480px; width: 90%; text-align: center; box-shadow: var(--shadow-xl); animation: pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        @keyframes pop { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        .modal-icon { font-size: 4rem; margin-bottom: 1rem; }
        .modal-title { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; }
        .modal-desc { font-size: 0.95rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 1.75rem; text-align: left; background: #f8fafc; padding: 1rem; border-radius: 10px; border: 1px solid var(--border); }
        .btn-modal-close { background: var(--primary); color: white; border: none; padding: 0.75rem 2rem; border-radius: 10px; font-weight: 700; cursor: pointer; text-decoration: none; display: inline-block; font-size: 0.95rem; }

        /* Footer */
        footer { background: #0b1120; color: #64748b; padding: 3.5rem 1.5rem 1.5rem; margin-top: auto; border-top: 1px solid #1e293b; }
        .footer-grid { max-width: 1240px; margin: 0 auto 2.5rem; display: grid; grid-template-columns: 2fr repeat(3, 1fr); gap: 3rem; }
        .footer-brand h4 { color: white; font-size: 1.3rem; margin-bottom: 0.75rem; }
        .footer-brand p { font-size: 0.875rem; line-height: 1.6; max-width: 300px; }
        .footer-col h5 { color: white; font-size: 0.95rem; font-weight: 700; margin-bottom: 1.2rem; }
        .footer-col ul { list-style: none; }
        .footer-col li { margin-bottom: 0.65rem; }
        .footer-col a { color: #94a3b8; text-decoration: none; font-size: 0.875rem; }
        .footer-bottom { max-width: 1240px; margin: 0 auto; padding-top: 1.5rem; border-top: 1px solid #1e293b; display: flex; justify-content: space-between; font-size: 0.825rem; }

        @media (max-width: 860px) {
            .checkout-container { grid-template-columns: 1fr; }
            .vietqr-box { flex-direction: column; text-align: center; }
            .footer-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Top Announcement Bar -->
    <div class="top-bar">
        <div>🔒 <strong>Bảo mật giao dịch:</strong> Mã hóa đường truyền SSL/TLS 256-bit chuẩn quốc tế PCI DSS</div>
        <div class="top-links">
            <a href="/">Hỗ trợ thanh toán: 1800 6868</a>
            <a href="/">Chính sách bảo mật</a>
        </div>
    </div>

    <!-- Live Cloud Architecture Header Badge -->
    <div class="cloud-badge-bar">
        <div class="sys-info">
            <span class="cloud-pill"><span class="dot"></span> AWS ALB Routed</span>
            <span>Target Group: <strong>tg_checkout</strong></span>
            <span>| Path Pattern: <strong>/checkout/*</strong></span>
        </div>
        <div>
            <span class="cloud-pill">Backend Node: EC2 Checkout (Nginx) • Huỳnh Nhật Hòa</span>
        </div>
    </div>

    <!-- Main Navigation Bar -->
    <header>
        <div class="nav-container">
            <a href="/" class="brand-logo">
                🛒 Cloud<span>Mart</span>
            </a>

            <div class="secure-badge">
                <span>🛡️ Cổng Thanh Toán Bảo Mật 256-bit</span>
            </div>
        </div>
    </header>

    <!-- Stepper Navigation -->
    <div class="stepper-container">
        <div class="stepper">
            <div class="step-item completed">
                <div class="step-num">✓</div>
                <div class="step-label">Giỏ hàng</div>
            </div>
            <div class="step-item active">
                <div class="step-num">2</div>
                <div class="step-label">Thanh toán & Giao nhận</div>
            </div>
            <div class="step-item">
                <div class="step-num">3</div>
                <div class="step-label">Hoàn tất đơn</div>
            </div>
        </div>
    </div>

    <!-- Main Checkout Container -->
    <div class="checkout-container">
        <!-- Left: Input Forms -->
        <div>
            <!-- Shipping Information -->
            <div class="checkout-box">
                <h2 class="box-title">📍 1. Thông Tin Nhận Hàng & Vận Chuyển</h2>
                <div class="form-grid">
                    <div class="form-group full">
                        <label class="form-label">Họ và tên người nhận *</label>
                        <input type="text" class="form-input" id="custName" value="Huỳnh Nhật Hòa">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Số điện thoại *</label>
                        <input type="text" class="form-input" id="custPhone" value="0912 345 678">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Email nhận hóa đơn điện tử *</label>
                        <input type="email" class="form-input" id="custEmail" value="hoahuynh@example.com">
                    </div>
                    <div class="form-group full">
                        <label class="form-label">Địa chỉ giao hàng (Số nhà, tên đường, phường/xã) *</label>
                        <input type="text" class="form-input" id="custAddress" value="Khu Công Nghệ Cao, TP. Thủ Đức, TP. Hồ Chí Minh">
                    </div>
                </div>

                <div class="vat-toggle">
                    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 600;">
                        <input type="checkbox" id="vatCheck" onchange="toggleVat()">
                        <span>Yêu cầu xuất hóa đơn điện tử VAT Doanh Nghiệp (Hóa đơn đỏ)</span>
                    </label>
                    <div id="vatForm" style="display: none; margin-top: 1rem;" class="form-grid">
                        <div class="form-group full">
                            <label class="form-label">Tên Công ty / Doanh nghiệp</label>
                            <input type="text" class="form-input" placeholder="Ví dụ: Công ty TNHH Giải Pháp Công Nghệ...">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Mã số thuế</label>
                            <input type="text" class="form-input" placeholder="Ví dụ: 0312345678">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Địa chỉ đăng ký kinh doanh</label>
                            <input type="text" class="form-input" placeholder="Địa chỉ theo giấy phép ĐKKD...">
                        </div>
                    </div>
                </div>
            </div>

            <!-- Payment Methods Selection with Dynamic Views -->
            <div class="checkout-box">
                <h2 class="box-title">💳 2. Chọn Phương Thức Thanh Toán Thuận Tiện</h2>
                <div class="payment-options">

                    <!-- Method 1: VietQR -->
                    <div class="payment-card active" id="cardVietQR">
                        <div class="payment-header" onclick="selectPayment('VietQR')">
                            <div class="payment-info">
                                <input type="radio" name="pay_opt" checked id="radioVietQR" style="accent-color: var(--primary);">
                                <span>Chuyển khoản Ngân hàng qua Mã VietQR (Napas 247)</span>
                            </div>
                            <span class="payment-badge">⚡ Khuyên dùng</span>
                        </div>
                        <div class="payment-body" id="bodyVietQR" style="display: block;">
                            <div class="vietqr-box">
                                <div class="qr-image-wrapper">
                                    <div class="qr-placeholder">📱</div>
                                    <div class="qr-badge-sub">VIETQR NAPAS247</div>
                                </div>
                                <div style="flex: 1;">
                                    <div style="font-size: 0.9rem; font-weight: 700; color: #059669; margin-bottom: 0.5rem;">
                                        ✓ Quét mã bằng bất kỳ App ngân hàng (VCB, MB, Techcombank, VPBank...)
                                    </div>
                                    <table class="qr-details-table">
                                        <tr>
                                            <td>Ngân hàng:</td>
                                            <td>Vietcombank (Hội sở chính)</td>
                                        </tr>
                                        <tr>
                                            <td>Số tài khoản:</td>
                                            <td>
                                                <span>0123456789999</span>
                                                <button class="copy-pill" onclick="copyText('0123456789999')">Sao chép</button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Chủ tài khoản:</td>
                                            <td>CONG TY CO PHAN CLOUDMART</td>
                                        </tr>
                                        <tr>
                                            <td>Nội dung CK:</td>
                                            <td>
                                                <span style="color:#7c3aed;">CMD8899</span>
                                                <button class="copy-pill" onclick="copyText('CMD8899')">Sao chép</button>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Method 2: International Card -->
                    <div class="payment-card" id="cardCC">
                        <div class="payment-header" onclick="selectPayment('CC')">
                            <div class="payment-info">
                                <input type="radio" name="pay_opt" id="radioCC" style="accent-color: var(--primary);">
                                <span>Thẻ Tín Dụng / Ghi Nợ Quốc Tế (Visa, Master, JCB, Amex)</span>
                            </div>
                            <span>💳</span>
                        </div>
                        <div class="payment-body" id="bodyCC">
                            <div class="credit-card-preview">
                                <div class="cc-chip">💳</div>
                                <div class="cc-number" id="previewCCNum">•••• •••• •••• 8899</div>
                                <div class="cc-bottom">
                                    <span id="previewCCHolder">HUYNH NHAT HOA</span>
                                    <span>EXP: 12/28</span>
                                </div>
                            </div>
                            <div class="form-grid">
                                <div class="form-group full">
                                    <label class="form-label">Số thẻ tín dụng</label>
                                    <input type="text" class="form-input" placeholder="4000 1234 5678 8899" oninput="updateCCPreview(this.value)">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Tên in trên thẻ</label>
                                    <input type="text" class="form-input" value="HUYNH NHAT HOA" oninput="document.getElementById('previewCCHolder').innerText = this.value.toUpperCase()">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Hạn thẻ & CVV</label>
                                    <input type="text" class="form-input" placeholder="12/28  |  CVC: 123">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Method 3: E-Wallets -->
                    <div class="payment-card" id="cardWallet">
                        <div class="payment-header" onclick="selectPayment('Wallet')">
                            <div class="payment-info">
                                <input type="radio" name="pay_opt" id="radioWallet" style="accent-color: var(--primary);">
                                <span>Ví Điện Tử (MoMo, ZaloPay, ShopeePay, Apple Pay)</span>
                            </div>
                            <span>📱</span>
                        </div>
                        <div class="payment-body" id="bodyWallet">
                            <p style="font-size: 0.9rem; color: #475569; margin-bottom: 0.75rem;">Liên kết trực tiếp và thanh toán một chạm an toàn:</p>
                            <div style="display: flex; gap: 0.75rem;">
                                <button style="flex:1; padding: 0.7rem; border: 1.5px solid #d946ef; background: #fdf4ff; border-radius: 8px; font-weight: 700; color: #c026d3; cursor: pointer;">Ví MoMo</button>
                                <button style="flex:1; padding: 0.7rem; border: 1.5px solid #0284c7; background: #f0f9ff; border-radius: 8px; font-weight: 700; color: #0284c7; cursor: pointer;">ZaloPay</button>
                                <button style="flex:1; padding: 0.7rem; border: 1.5px solid #000; background: #000; border-radius: 8px; font-weight: 700; color: #fff; cursor: pointer;"> Apple Pay</button>
                            </div>
                        </div>
                    </div>

                    <!-- Method 4: 0% Installment -->
                    <div class="payment-card" id="cardInstallment">
                        <div class="payment-header" onclick="selectPayment('Installment')">
                            <div class="payment-info">
                                <input type="radio" name="pay_opt" id="radioInstallment" style="accent-color: var(--primary);">
                                <span>Trả Góp 0% Lãi Suất (Qua Thẻ Tín Dụng / Kredivo / Fundiin)</span>
                            </div>
                            <span class="payment-badge" style="background:#fef3c7; color:#b45309;">0% Lãi suất</span>
                        </div>
                        <div class="payment-body" id="bodyInstallment">
                            <p style="font-size: 0.85rem; color: #475569; margin-bottom: 0.75rem;">Chọn kỳ hạn trả góp phù hợp với bạn:</p>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; text-align: center;">
                                <div style="border: 1px solid var(--primary); padding: 0.6rem; border-radius: 8px; background: #faf5ff; cursor: pointer;">
                                    <div style="font-weight: 800; font-size: 0.95rem; color: var(--primary);">3 Tháng</div>
                                    <div style="font-size: 0.75rem; color: var(--text-muted);">25.160.000₫/th</div>
                                </div>
                                <div style="border: 1px solid var(--border); padding: 0.6rem; border-radius: 8px; cursor: pointer;">
                                    <div style="font-weight: 800; font-size: 0.95rem;">6 Tháng</div>
                                    <div style="font-size: 0.75rem; color: var(--text-muted);">12.580.000₫/th</div>
                                </div>
                                <div style="border: 1px solid var(--border); padding: 0.6rem; border-radius: 8px; cursor: pointer;">
                                    <div style="font-weight: 800; font-size: 0.95rem;">12 Tháng</div>
                                    <div style="font-size: 0.75rem; color: var(--text-muted);">6.290.000₫/th</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Method 5: COD -->
                    <div class="payment-card" id="cardCOD">
                        <div class="payment-header" onclick="selectPayment('COD')">
                            <div class="payment-info">
                                <input type="radio" name="pay_opt" id="radioCOD" style="accent-color: var(--primary);">
                                <span>Thanh toán Tiền mặt khi nhận hàng (COD)</span>
                            </div>
                            <span>💵</span>
                        </div>
                        <div class="payment-body" id="bodyCOD">
                            <p style="font-size: 0.85rem; color: #059669; font-weight: 600;">
                                ✓ Được đồng kiểm tra hàng (mở hộp kiểm tra ngoại quan máy) trước khi thanh toán cho shipper.
                            </p>
                        </div>
                    </div>

                </div>
            </div>

            <!-- Architecture Banner -->
            <div class="arch-banner">
                <h3>☁️ Cơ Chế Định Tuyến Cân Bằng Tải (AWS ALB Listener Rule)</h3>
                <p>Yêu cầu HTTP tới đường dẫn <code>/checkout/*</code> được Application Load Balancer so khớp bằng <strong>Listener Rule (Priority 20)</strong> và chuyển tiếp toàn bộ lưu lượng tới <strong>Target Group: tg_checkout</strong> nằm tại Subnet 2 (Multi-AZ).</p>
            </div>
        </div>

        <!-- Right: Order Summary with Interactive Quantities -->
        <aside class="summary-card">
            <h2 class="summary-title">Tóm Tắt Đơn Hàng</h2>

            <!-- Items -->
            <div class="cart-item">
                <div class="cart-thumb">💻</div>
                <div class="cart-details">
                    <div class="cart-name">MacBook Pro 16" M3 Max</div>
                    <div class="cart-meta">
                        <span>SL:</span>
                        <button class="qty-btn" onclick="updateQty(-1)">-</button>
                        <strong id="itemQty">1</strong>
                        <button class="qty-btn" onclick="updateQty(1)">+</button>
                        <span>• Space Black</span>
                    </div>
                </div>
                <div class="cart-price" id="itemPriceDisplay">68.990.000 ₫</div>
            </div>

            <div class="cart-item">
                <div class="cart-thumb">🎧</div>
                <div class="cart-details">
                    <div class="cart-name">Sony WH-1000XM5 Wireless</div>
                    <div class="cart-meta">SL: 1 • Màu Bạc Platinum</div>
                </div>
                <div class="cart-price">7.990.000 ₫</div>
            </div>

            <!-- Voucher Box -->
            <div class="promo-box">
                <input type="text" class="promo-input" id="couponCode" value="CLOUDMART10" placeholder="Nhập mã giảm giá...">
                <button class="btn-apply" onclick="applyCoupon()">Áp dụng</button>
            </div>

            <!-- Pricing Breakdown -->
            <div class="calc-row">
                <span>Tạm tính tiền hàng:</span>
                <span id="subTotalDisplay">76.980.000 ₫</span>
            </div>
            <div class="calc-row">
                <span>Phí vận chuyển Express (2H):</span>
                <span style="color: #10b981; font-weight: 700;">Miễn phí</span>
            </div>
            <div class="calc-row discount">
                <span>Khuyến mãi Voucher (<span id="appliedCouponName">CLOUDMART10</span>):</span>
                <span id="discountDisplay">- 1.500.000 ₫</span>
            </div>
            <div class="calc-row total">
                <span>Tổng tiền thanh toán:</span>
                <span id="totalDisplay">75.480.000 ₫</span>
            </div>

            <button class="btn-submit-order" onclick="openSuccessModal()">
                <span>🔒 ĐẶT HÀNG & THANH TOÁN NGAY</span>
            </button>
        </aside>
    </div>

    <!-- Success Modal Pop-up -->
    <div id="successModal" class="modal-overlay">
        <div class="modal-card">
            <div class="modal-icon">🎉</div>
            <h3 class="modal-title">Đặt Hàng Thành Công!</h3>
            <div class="modal-desc">
                <div>• Khách hàng: <strong id="mCustName">Huỳnh Nhật Hòa</strong></div>
                <div>• Số điện thoại: <strong id="mCustPhone">0912 345 678</strong></div>
                <div>• Phương thức: <strong id="mPayMethod">VietQR Chuyển khoản</strong></div>
                <div>• Tổng tiền: <strong id="mTotal" style="color:#7c3aed;">75.480.000 ₫</strong></div>
                <div style="margin-top: 0.5rem; color: #059669; font-weight: 700;">✓ Hệ thống đã ghi nhận mã đơn hàng: #CMD-2026-8899</div>
            </div>
            <a href="/" class="btn-modal-close">Quay lại Trang Chủ &rarr;</a>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <div class="footer-grid">
            <div class="footer-brand">
                <h4>🛒 CloudMart E-Commerce</h4>
                <p>Hệ thống bán hàng trực tuyến ứng dụng kiến trúc cân bằng tải thông minh Application Load Balancer trên nền tảng AWS và Terraform.</p>
            </div>
            <div class="footer-col">
                <h5>Dịch Vụ & Sản Phẩm</h5>
                <ul>
                    <li><a href="/products/">Laptop & MacBook</a></li>
                    <li><a href="/products/">Điện thoại thông minh</a></li>
                    <li><a href="/products/">Phụ kiện & Âm thanh</a></li>
                    <li><a href="/checkout/">Thanh toán đơn hàng</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h5>Hỗ Trợ Khách Hàng</h5>
                <ul>
                    <li><a href="/">Chính sách bảo mật</a></li>
                    <li><a href="/">Hướng dẫn thanh toán</a></li>
                    <li><a href="/">Cam kết chất lượng</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h5>Đồ Án Nhóm</h5>
                <ul>
                    <li><a href="/">1. Phạm Đinh Gia Bảo (Core ALB)</a></li>
                    <li><a href="/">2. Huỳnh Nhật Hòa (Targets & Web)</a></li>
                    <li><a href="/">3. Ngô Khánh Hưng (Security & SSL)</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <div>© 2026 CloudMart E-Commerce System. All Rights Reserved.</div>
            <div>Đồ án Cân bằng tải HTTPS ALB với Terraform</div>
        </div>
    </footer>

    <script>
        var currentMethod = 'VietQR';
        var baseMacPrice = 68990000;
        var sonyPrice = 7990000;
        var qty = 1;
        var discount = 1500000;

        function selectPayment(type) {
            currentMethod = type;
            var methods = ['VietQR', 'CC', 'Wallet', 'Installment', 'COD'];
            methods.forEach(function(m) {
                var card = document.getElementById('card' + m);
                var body = document.getElementById('body' + m);
                var radio = document.getElementById('radio' + m);
                if (m === type) {
                    card.classList.add('active');
                    body.style.display = 'block';
                    radio.checked = true;
                } else {
                    card.classList.remove('active');
                    body.style.display = 'none';
                    radio.checked = false;
                }
            });
        }

        function updateCCPreview(val) {
            document.getElementById('previewCCNum').innerText = val || '•••• •••• •••• 8899';
        }

        function copyText(txt) {
            navigator.clipboard.writeText(txt).then(function() {
                alert('Đã sao chép: ' + txt);
            });
        }

        function toggleVat() {
            var chk = document.getElementById('vatCheck');
            document.getElementById('vatForm').style.display = chk.checked ? 'grid' : 'none';
        }

        function updateQty(delta) {
            qty += delta;
            if (qty < 1) qty = 1;
            document.getElementById('itemQty').innerText = qty;
            recalculate();
        }

        function formatMoney(num) {
            return num.toLocaleString('vi-VN') + ' ₫';
        }

        function recalculate() {
            var macTotal = baseMacPrice * qty;
            document.getElementById('itemPriceDisplay').innerText = formatMoney(macTotal);
            var subTotal = macTotal + sonyPrice;
            document.getElementById('subTotalDisplay').innerText = formatMoney(subTotal);
            var finalTotal = subTotal - discount;
            document.getElementById('totalDisplay').innerText = formatMoney(finalTotal);
        }

        function applyCoupon() {
            var code = document.getElementById('couponCode').value.trim().toUpperCase();
            if (code === 'CLOUDMART10') {
                discount = 1500000;
                document.getElementById('appliedCouponName').innerText = 'CLOUDMART10 (-1.5Tr)';
                alert('Áp dụng mã CLOUDMART10 thành công! Giảm 1.500.000₫');
            } else if (code === 'FREESHIP') {
                discount = 500000;
                document.getElementById('appliedCouponName').innerText = 'FREESHIP (-500k)';
                alert('Áp dụng mã FREESHIP thành công!');
            } else {
                alert('Mã giảm giá không hợp lệ hoặc đã hết hạn.');
                return;
            }
            document.getElementById('discountDisplay').innerText = '- ' + formatMoney(discount);
            recalculate();
        }

        function openSuccessModal() {
            document.getElementById('mCustName').innerText = document.getElementById('custName').value || 'Khách hàng';
            document.getElementById('mCustPhone').innerText = document.getElementById('custPhone').value || '0912 345 678';
            document.getElementById('mPayMethod').innerText = currentMethod;
            document.getElementById('mTotal').innerText = document.getElementById('totalDisplay').innerText;
            document.getElementById('successModal').style.display = 'flex';
        }
    </script>
</body>
</html>
EOF

cp /var/www/html/checkout/index.html /usr/share/nginx/html/checkout/index.html
cp /var/www/html/checkout/index.html /var/www/html/index.html
cp /var/www/html/checkout/index.html /usr/share/nginx/html/index.html
systemctl daemon-reload
systemctl enable nginx
systemctl restart nginx
