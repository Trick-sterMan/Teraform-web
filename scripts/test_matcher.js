// Test intelligent matcher prototype
function cleanVietnamese(str) {
    return (str || "").toLowerCase()
        .replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, "a")
        .replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, "e")
        .replace(/ì|í|ị|ỉ|ĩ/g, "i")
        .replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, "o")
        .replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, "u")
        .replace(/ỳ|ý|ỵ|ỷ|ỹ/g, "y")
        .replace(/đ/g, "d")
        .trim();
}

function findExactProductMatch(query, catalog) {
    if (!query || !catalog || catalog.length === 0) return null;
    var rawQ = query.trim();
    var lowerQ = rawQ.toLowerCase();
    
    // 0. Khớp tên 100% (ví dụ khi nhấn nút Hỏi Giá từ Modal hay Dropdown)
    for (var i = 0; i < catalog.length; i++) {
        var p = catalog[i];
        if (rawQ === p.name || lowerQ === p.name.toLowerCase()) return p;
        if (lowerQ.includes(p.name.toLowerCase())) return p;
    }

    // Làm sạch các từ đệm tiếng Việt
    var cleanQ = lowerQ
        .replace(/giá|bao nhiêu|báo giá|bao nhieu|cho hỏi|máy|chi tiết|thông tin|tư vấn|giới thiệu|muốn biết|cần biết|hỏi về|xem|thế nào|sao|tiền|tôi|mình|cho em|cho anh|cho chị|shop ơi|ad ơi/g, " ")
        .replace(/\s+/g, " ")
        .trim();
    
    if (!cleanQ) return null;

    // Chuẩn hóa khoảng trắng số (fold 5 -> fold5, s 24 -> s24...)
    var normQ = cleanQ
        .replace(/fold\s*([0-9]+)/g, "fold$1")
        .replace(/flip\s*([0-9]+)/g, "flip$1")
        .replace(/s\s*([0-9]+)\s*\+/g, "s$1+")
        .replace(/s\s*([0-9]+)\s*plus/g, "s$1+")
        .replace(/s\s*([0-9]+)/g, "s$1")
        .replace(/gt\s*([0-9]+)/g, "gt$1")
        .replace(/xm\s*([0-9]+)/g, "xm$1")
        .replace(/note\s*([0-9]+)/g, "note$1");

    // 1. Nhận diện HÃNG YÊU CẦU từ câu hỏi
    var targetBrand = null;
    if (normQ.includes("apple") || normQ.includes("iphone") || normQ.includes("macbook") || normQ.includes("ipad") || normQ.includes("airpods") || normQ.includes("imac")) {
        targetBrand = "Apple";
    } else if (normQ.includes("samsung") || normQ.includes("galaxy") || normQ.includes("z fold") || normQ.includes("z flip") || normQ.includes("fold5") || normQ.includes("fold6") || normQ.includes("flip6")) {
        targetBrand = "Samsung";
    } else if (normQ.includes("sony") || normQ.includes("playstation") || normQ.includes("ps5") || normQ.includes("xperia") || normQ.includes("dualsense") || normQ.includes("bravia")) {
        targetBrand = "Sony";
    } else if (normQ.includes("dell") || normQ.includes("alienware") || normQ.includes("xps")) {
        targetBrand = "Dell";
    } else if (normQ.includes("asus") || normQ.includes("rog") || normQ.includes("tuf") || normQ.includes("zenbook") || normQ.includes("zephyrus")) {
        targetBrand = "ASUS";
    } else if (normQ.includes("oppo") || normQ.includes("reno") || normQ.includes("find x") || normQ.includes("find n")) {
        targetBrand = "OPPO";
    } else if (normQ.includes("huawei") || normQ.includes("mate") || normQ.includes("pura") || normQ.includes("matepad")) {
        targetBrand = "Huawei";
    } else if (normQ.includes("realme") || normQ.includes("celmi")) {
        targetBrand = "Realme";
    }

    // 2. Nhận diện hậu tố phiên bản (Pro Max, Pro, Plus, Ultra, SE, FE, Fold, Flip, Mini, Air...)
    var hasProMax = normQ.includes("pro max") || normQ.includes("promax");
    var hasPro = !hasProMax && normQ.includes("pro");
    var hasPlus = normQ.includes("plus") || normQ.includes("+");
    var hasUltra = normQ.includes("ultra");
    var hasFE = normQ.includes("fe");
    var hasAir = normQ.includes("air");
    var hasMini = normQ.includes("mini");

    var scored = [];

    catalog.forEach(function(prod) {
        var t = prod.name.toLowerCase();
        var cat = (prod.category || "").toLowerCase();
        var specs = (prod.specs || "").toLowerCase();
        var brand = prod.brand || "";

        var normT = t
            .replace(/fold\s*([0-9]+)/g, "fold$1")
            .replace(/flip\s*([0-9]+)/g, "flip$1")
            .replace(/s\s*([0-9]+)\s*\+/g, "s$1+")
            .replace(/s\s*([0-9]+)\s*plus/g, "s$1+")
            .replace(/s\s*([0-9]+)/g, "s$1")
            .replace(/gt\s*([0-9]+)/g, "gt$1")
            .replace(/xm\s*([0-9]+)/g, "xm$1");

        var score = 0;

        // A. CÔ LẬP THƯƠNG HIỆU: Nếu khách hỏi hãng A mà máy thuộc hãng B -> LOẠI THẲNG!
        if (targetBrand && brand !== targetBrand) {
            return; // Khách hỏi Sony không bao giờ trả lời OPPO, khách hỏi Samsung không trả lời Apple!
        }
        if (targetBrand && brand === targetBrand) {
            score += 1500;
        }

        // B. Khớp chuỗi hoàn hảo
        if (normT.includes(normQ)) {
            score += 3000 + normQ.length * 30;
        }

        // C. Phạt hoặc thưởng theo thế hệ / số dòng chính (18, 17, 16, 15, 14, 13, 12, 11, 25, 24, 23...)
        var genNumbers = ["18", "17", "16", "15", "14", "13", "12", "11", "25", "24", "23", "9", "8", "7", "6", "5", "4", "3", "2", "1"];
        genNumbers.forEach(function(num) {
            var re = new RegExp("\\b" + num + "\\b");
            var inQ = re.test(normQ) || normQ.includes("s" + num) || normQ.includes("fold" + num) || normQ.includes("flip" + num) || normQ.includes("gt" + num) || normQ.includes("m" + num);
            var inT = re.test(normT) || normT.includes("s" + num) || normT.includes("fold" + num) || normT.includes("flip" + num) || normT.includes("gt" + num) || normT.includes("m" + num);
            if (inQ && inT) {
                score += 2000;
            } else if (inQ && !inT) {
                score -= 4000; // Phạt nặng nếu sai số thế hệ (ví dụ hỏi S24 nhưng máy là S25)
            }
        });

        // D. Phạt / Thưởng theo phân cấp Hậu Tố (Pro Max, Pro, Plus, Ultra, FE, Air, Fold...)
        var tHasProMax = normT.includes("pro max") || normT.includes("promax");
        var tHasPro = !tHasProMax && normT.includes("pro");
        var tHasPlus = normT.includes("plus") || normT.includes("+");
        var tHasUltra = normT.includes("ultra");
        var tHasFE = normT.includes("fe");
        var tHasAir = normT.includes("air");

        // PRO MAX
        if (hasProMax) {
            if (tHasProMax) score += 3500;
            else score -= 4500;
        } else if (tHasProMax) {
            // Khách KHÔNG hỏi Pro Max mà máy là Pro Max -> trừ điểm
            score -= 1500;
        }

        // PRO
        if (hasPro) {
            if (tHasPro) score += 3000;
            else score -= 3000;
        } else if (tHasPro && !hasProMax) {
            score -= 1200;
        }

        // ULTRA
        if (hasUltra) {
            if (tHasUltra) score += 3500;
            else score -= 4000;
        } else if (tHasUltra) {
            score -= 1500;
        }

        // PLUS
        if (hasPlus) {
            if (tHasPlus) score += 3500;
            else score -= 4000;
        } else if (tHasPlus) {
            score -= 1500;
        }

        // FE
        if (hasFE) {
            if (tHasFE) score += 3500;
            else score -= 4000;
        } else if (tHasFE) {
            score -= 1500;
        }

        // AIR
        if (hasAir) {
            if (tHasAir) score += 3500;
            else score -= 4000;
        } else if (tHasAir) {
            score -= 1500;
        }

        // E. Khớp danh mục thiết bị (tai nghe, laptop, dong ho, man hinh, may tinh bang...)
        var isHeadphone = normQ.includes("tai nghe") || normQ.includes("headphone") || normQ.includes("earphone") || normQ.includes("buds") || normQ.includes("airpods") || normQ.includes("xm5");
        if (isHeadphone) {
            if (t.includes("tai nghe") || t.includes("buds") || t.includes("airpods") || t.includes("xm5") || cat.includes("tai nghe")) score += 2500;
            else score -= 3000;
        }

        var isLaptop = normQ.includes("laptop") || normQ.includes("macbook") || normQ.includes("xps") || normQ.includes("zenbook") || normQ.includes("tuf");
        if (isLaptop) {
            if (t.includes("macbook") || t.includes("xps") || t.includes("zenbook") || t.includes("laptop") || cat.includes("laptop")) score += 2500;
            else score -= 3000;
        }

        var isTablet = normQ.includes("ipad") || normQ.includes("may tinh bang") || normQ.includes("tab") || normQ.includes("matepad");
        if (isTablet) {
            if (t.includes("ipad") || t.includes("tab") || t.includes("matepad") || cat.includes("may tinh bang") || cat.includes("tablet")) score += 2500;
            else score -= 3000;
        }

        var isWatch = normQ.includes("dong ho") || normQ.includes("watch");
        if (isWatch) {
            if (t.includes("watch") || cat.includes("dong ho")) score += 2500;
            else score -= 3000;
        }

        // F. Khớp từng token từ vựng
        var tokens = normQ.split(/\s+/);
        tokens.forEach(function(tok) {
            if (tok.length >= 2) {
                if (normT.includes(tok)) score += 300 * tok.length;
                else if (cat.includes(tok)) score += 100 * tok.length;
                else if (specs.includes(tok)) score += 50 * tok.length;
            }
        });

        if (score > 100) {
            scored.push({ prod: prod, score: score });
        }
    });

    if (scored.length === 0) return null;
    scored.sort(function(a, b) { return b.score - a.score; });
    return scored[0].prod;
}
