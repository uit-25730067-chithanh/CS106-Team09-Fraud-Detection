const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9'; // 10" x 5.625"

// -------------------------------------------------------------
// CS115 UIT Academic Design System
// -------------------------------------------------------------
const C = {
  // Theme Colors
  navyBg: '1E295C',      // Deep Academic Navy (Cover / Dividers)
  whiteBg: 'FFFFFF',     // Clean Pure White for Content
  lightGrayBg: 'F8FAFC', // Subtle section / code background
  navyTitle: '21295C',   // Title Color on White
  goldSub: 'AB997A',     // UIT Gold / Academic Subtitle
  textDark: '1F2937',    // Primary Body Text
  textMuted: '4B5563',   // Secondary / Bullet Text
  textDim: '6B7280',     // Footer / Page Number Text
  blueAccent: '2563EB',  // UIT Primary Blue
  skyBox: 'EFF6FF',      // Highlight box fill (Light Sky)
  skyBorder: 'BFDBFE',   // Highlight box border
  redBox: 'FEF2F2',      // Warning box fill
  redBorder: 'FECACA',   // Warning box border
  dangerRed: 'DC2626',   // Warning / Fraud Red
  tblHdrBg: '21295C',    // Table Header Navy
  tblAltBg: 'F1F5F9'     // Table Row Alt
};

const F = {
  fontTitle: 'Montserrat',
  fontBody: 'Calibri',
  fontNumber: 'Cambria',
  coverTitle: 32,
  slideTitle: 20,
  subTitle: 15,
  body: 12,
  bodyBold: 12,
  small: 10,
  caption: 9
};

const SW = 10.0;
const SH = 5.625;
const M = 0.55;
const CW = SW - 2 * M; // 8.9

// Slide Header / Footer Helper (Exact CS115 Structure)
function addAcademicHeader(slide, title, pageNum, totalPages = 20) {
  slide.background = { color: C.whiteBg };

  // Top University Banner
  slide.addText('TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐHQG-HCM', {
    x: M, y: 0.22, w: CW, h: 0.22,
    fontSize: 8.5, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  // Slide Title (Left Aligned, Montserrat, Navy)
  slide.addText(title, {
    x: M, y: 0.52, w: CW, h: 0.48,
    fontSize: F.slideTitle, fontFace: F.fontTitle, color: C.navyTitle, bold: true, shrinkText: true
  });

  // Bottom Footer
  slide.addText('CS106 — Nhóm 09 — Phát hiện Gian lận Tài chính trên PaySim', {
    x: M, y: SH - 0.35, w: 6.0, h: 0.2,
    fontSize: 8.5, fontFace: F.fontBody, color: C.textDim
  });

  // Bottom Page Number
  slide.addText(`${pageNum} / ${totalPages}`, {
    x: SW - M - 1.5, y: SH - 0.35, w: 1.5, h: 0.2,
    fontSize: 8.5, fontFace: F.fontBody, color: C.textDim, align: 'right'
  });
}

// Helper: Open Notation / Explanation Box (Right Column)
function addNotationTable(slide, x, y, w, rows) {
  const tableData = rows.map(([label, symbol, desc]) => [
    { text: label, options: { fill: { color: 'E2E8F0' }, color: C.navyTitle, bold: true, fontSize: 9.5 } },
    { text: symbol, options: { fill: { color: 'F1F5F9' }, color: C.blueAccent, bold: true, fontSize: 10, align: 'center' } },
    { text: desc, options: { fill: { color: '1E295C' }, color: 'FFFFFF', fontSize: 9 } }
  ]);

  slide.addTable(tableData, {
    x, y, w,
    colW: [w * 0.35, w * 0.15, w * 0.5],
    border: { pt: 0.5, color: 'CBD5E1' },
    margin: [2, 3, 2, 3]
  });
}

// Helper: Academic Highlight Block
function addHighlightBlock(slide, { x, y, w, h, title, bullets = [], text = '', type = 'blue' }) {
  const isBlue = type === 'blue';
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: isBlue ? C.skyBox : C.redBox },
    line: { color: isBlue ? C.skyBorder : C.redBorder, width: 1 }
  });

  let curY = y + 0.1;
  if (title) {
    slide.addText(title, {
      x: x + 0.2, y: curY, w: w - 0.4, h: 0.28,
      fontSize: 11.5, fontFace: F.fontTitle, color: isBlue ? C.navyTitle : C.dangerRed, bold: true
    });
    curY += 0.28;
  }

  if (text) {
    slide.addText(text, {
      x: x + 0.2, y: curY, w: w - 0.4, h: h - (curY - y) - 0.08,
      fontSize: F.body, fontFace: F.fontBody, color: C.textDark, shrinkText: true
    });
  } else if (bullets && bullets.length > 0) {
    const textArr = bullets.map((b, idx) => ({
      text: b,
      options: { bullet: true, breakLine: idx < bullets.length - 1, color: C.textDark, fontSize: F.body }
    }));
    slide.addText(textArr, {
      x: x + 0.2, y: curY, w: w - 0.4, h: h - (curY - y) - 0.08,
      fontSize: F.body, fontFace: F.fontBody, shrinkText: true
    });
  }
}

// =========================================================================
// SLIDE 1: COVER (Exact CS115 Style - Deep Navy Elegance)
// =========================================================================
{
  const s = pptx.addSlide();
  s.background = { color: C.navyBg };

  s.addText('TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐHQG-HCM\nKHOA KHOA HỌC MÁY TÍNH', {
    x: M, y: 0.5, w: CW, h: 0.5,
    fontSize: 9.5, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  s.addText('PHÁT HIỆN GIAN LẬN TÀI CHÍNH', {
    x: M, y: 1.45, w: CW, h: 0.75,
    fontSize: 34, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText('Ứng dụng Học máy & Học sâu trên Bộ dữ liệu Mô phỏng PaySim', {
    x: M, y: 2.25, w: CW, h: 0.4,
    fontSize: 15, fontFace: 'Georgia', color: '93C5FD', align: 'center', italic: true
  });

  s.addText('Giảng viên hướng dẫn: PGS.TS. Nguyễn Đình Hiển', {
    x: M, y: 3.0, w: CW, h: 0.35,
    fontSize: 13, fontFace: F.fontBody, color: 'FFFFFF', align: 'center'
  });

  s.addShape(pptx.shapes.LINE, {
    x: M + 2.8, y: 3.48, w: 1.2, h: 0,
    line: { color: '93C5FD', width: 2 }
  });
  s.addText('Nhóm 09', {
    x: M + 4.1, y: 3.38, w: 0.9, h: 0.25,
    fontSize: 12.5, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });
  s.addShape(pptx.shapes.LINE, {
    x: M + 5.1, y: 3.48, w: 1.2, h: 0,
    line: { color: '93C5FD', width: 2 }
  });

  s.addText('Trần Hoàng Hôn  ·  Đặng Chí Thanh  ·  Nguyễn Duy Khang  ·  Hoàng Cao Sơn  ·  Vũ Văn Duy  ·  Bùi Thị Mỹ Cẩm  ·  Phạm Thanh Trung', {
    x: M, y: 3.85, w: CW, h: 0.35,
    fontSize: 10, fontFace: F.fontBody, color: 'CBD5E1', align: 'center'
  });
}

// =========================================================================
// SLIDE 2: AGENDA (CS115 Minimalist Number Grid)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'NỘI DUNG TRÌNH BÀY', 2);

  const agenda = [
    { num: '01', title: 'Giới thiệu & Phát biểu Bài toán', color: '60A5FA' },
    { num: '02', title: 'Phân tích Dữ liệu Khám phá & Kỹ thuật Đặc trưng', color: '3B82F6' },
    { num: '03', title: 'Phương pháp Đề xuất & Kiến trúc Pipeline', color: '2563EB' },
    { num: '04', title: 'Kết quả Thực nghiệm & Phân tích Sai số', color: '1D4ED8' },
    { num: '05', title: 'Bản Demo Trực quan & Hướng Phát triển', color: '1E3A8A' }
  ];

  const rowH = 0.65;
  agenda.forEach((item, idx) => {
    const cy = 1.2 + idx * (rowH + 0.18);
    // Number Block
    s.addShape(pptx.shapes.RECTANGLE, {
      x: M + 0.5, y: cy, w: 0.75, h: rowH,
      fill: { color: item.color },
      line: { type: 'none' }
    });
    s.addText(item.num, {
      x: M + 0.5, y: cy, w: 0.75, h: rowH,
      fontSize: 20, fontFace: F.fontNumber, color: 'FFFFFF', align: 'center', bold: true
    });
    // Title
    s.addText(item.title, {
      x: M + 1.5, y: cy + 0.1, w: 6.5, h: rowH - 0.1,
      fontSize: 15.5, fontFace: F.fontTitle, color: C.navyTitle, bold: true
    });
  });
}

// =========================================================================
// SLIDE 3: PROBLEM MOTIVATION & TECHNICAL CHALLENGES
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Động lực Nghiên cứu & Thách thức Kỹ thuật', 3);

  // Left Content
  s.addText([
    { text: '1. Bối cảnh Thực tiễn\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• Giao dịch tiền di động (Mobile Money) tăng trưởng bùng nổ, kéo theo các thủ đoạn gian lận tinh vi.\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Hệ thống phòng thủ đòi hỏi độ trễ suy luận cực thấp (< 100ms) trước khi dòng tiền bị rút khỏi hệ thống.\n\n', options: { fontSize: 11.5, color: C.textDark } },
    
    { text: '2. Mất cân bằng Dữ liệu Cực đoan (~0.13%)\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• Giao dịch gian lận chỉ chiếm ~1 trên 800 giao dịch, khiến các bộ phân loại thông thường bị suy sụp.\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Bất đối xứng chi phí (Cost Asymmetry): Bỏ sót gian lận (False Negative) gây thiệt hại tài chính nặng nề hơn rất nhiều so với cảnh báo nhầm.\n', options: { fontSize: 11.5, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 4.8, h: 3.8
  });

  // Right Notation Box
  addNotationTable(s, M + 5.1, 1.2, 3.8, [
    ['Nhãn mục tiêu', 'Y', '1 = Gian lận, 0 = Hợp lệ'],
    ['Mất cân bằng', 'IR', '0.13% mẫu dương tính (thiểu số)'],
    ['Chỉ số tối ưu', 'Recall', 'Tối đa hóa độ bao phủ gian lận thực tế'],
    ['Tỷ lệ chi phí', 'C_FN / C_FP', 'Trọng số phạt tổn thất bất đối xứng (>> 1)']
  ]);

  addHighlightBlock(s, {
    x: M + 5.1, y: 3.1, w: 3.8, h: 1.85,
    title: 'Mục tiêu Nghiên cứu',
    bullets: [
      'Xây dựng pipeline xử lý dữ liệu chuẩn chỉnh, chống rò rỉ (leak-free).',
      'Tối ưu hóa PR-AUC & Recall trên tập dữ liệu gian lận cực hiếm.',
      'Đối chuẩn mô hình Ensemble có giám sát với Học sâu Bất thường không giám sát.'
    ]
  });
}

// =========================================================================
// SLIDE 4: PAYSIM SYNTHETIC DATASET OVERVIEW
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Bộ dữ liệu PaySim: Đặc trưng Thống kê', 4);

  // Top Stat Cards
  const stats = [
    { num: '6.36M -> 200K', label: 'Kích thước sau Lấy mẫu', desc: 'Bảo toàn 100% mẫu gian lận' },
    { num: '8,213', label: 'Mẫu Gian lận (isFraud = 1)', desc: 'Nhãn thiểu số hiếm trong thực tế' },
    { num: '11', label: 'Thuộc tính Gốc Ban đầu', desc: 'Trường thời gian, loại giao dịch & số dư' }
  ];

  const colW = (CW - 0.4) / 3;
  stats.forEach((st, i) => {
    const cx = M + i * (colW + 0.2);
    s.addShape(pptx.shapes.RECTANGLE, {
      x: cx, y: 1.15, w: colW, h: 1.1,
      fill: { color: C.lightGrayBg },
      line: { color: 'E2E8F0', width: 1 }
    });
    s.addText(st.num, {
      x: cx, y: 1.22, w: colW, h: 0.4,
      fontSize: 18, fontFace: F.fontNumber, color: C.navyTitle, align: 'center', bold: true
    });
    s.addText(`${st.label}\n${st.desc}`, {
      x: cx, y: 1.62, w: colW, h: 0.55,
      fontSize: 9.5, fontFace: F.fontBody, color: C.textMuted, align: 'center'
    });
  });

  // Table of fields
  const tableData = [
    [
      { text: 'Tên Đặc trưng', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Kiểu Dữ liệu', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Miền Giá trị & Ý nghĩa Nghiệp vụ', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } }
    ],
    [{ text: 'step', options: { bold: true } }, { text: 'Số nguyên' }, { text: 'Bước thời gian theo giờ (1..744, tương ứng 30 ngày mô phỏng)' }],
    [{ text: 'type', options: { bold: true } }, { text: 'Phân loại' }, { text: 'Loại giao dịch: CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT' }],
    [{ text: 'amount', options: { bold: true } }, { text: 'Liên tục' }, { text: 'Số tiền thực hiện giao dịch (đơn vị tiền tệ cục bộ)' }],
    [{ text: 'oldbalanceOrg / newbalanceOrig', options: { bold: true } }, { text: 'Liên tục' }, { text: 'Số dư tài khoản nguồn trước và ngay sau khi phát sinh giao dịch' }],
    [{ text: 'oldbalanceDest / newbalanceDest', options: { bold: true } }, { text: 'Liên tục' }, { text: 'Số dư tài khoản đích trước và ngay sau khi phát sinh giao dịch' }]
  ];

  s.addTable(tableData, {
    x: M, y: 2.45, w: CW, h: 2.5,
    border: { pt: 0.5, color: 'CBD5E1' },
    margin: [3, 4, 3, 4],
    fontSize: 9.5
  });
}

// =========================================================================
// SLIDE 5: EXPLORATORY DATA ANALYSIS (EDA)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Khám phá Dữ liệu: Dấu vết Hành vi Cốt lõi', 5);

  const findings = [
    {
      title: 'Phát hiện 1: Khu biệt Loại Giao dịch',
      desc: '100% gian lận chỉ xuất hiện ở 2 loại: TRANSFER và CASH_OUT.\nCác loại PAYMENT, CASH_IN và DEBIT hoàn toàn không có gian lận (0%).\n-> Giải pháp: Lọc dữ liệu chỉ giữ lại TRANSFER & CASH_OUT để triệt tiêu nhiễu.'
    },
    {
      title: 'Phát hiện 2: Rút cạn Tài khoản Nguồn',
      desc: '97.56% giao dịch gian lận làm số dư tài khoản nguồn về đúng bằng 0 (newbalanceOrig == 0).\nKẻ gian luôn tìm cách vét sạch toàn bộ số dư của nạn nhân trong 1 lần chuyển tiền duy nhất.'
    },
    {
      title: 'Phát hiện 3: Bất thường Số dư Đích',
      desc: 'Tỷ lệ lớn giao dịch gian lận có độ lệch biến động số dư tại đích bằng 0.\nTài khoản nhận tiền lớn nhưng số dư đích được ghi nhận không tăng tương ứng.'
    }
  ];

  const fw = (CW - 0.3) / 3;
  findings.forEach((f, i) => {
    const fx = M + i * (fw + 0.15);
    addHighlightBlock(s, {
      x: fx, y: 1.2, w: fw, h: 3.75,
      title: f.title,
      text: f.desc,
      type: i === 1 ? 'red' : 'blue'
    });
  });
}

// =========================================================================
// SLIDE 6: FEATURE ENGINEERING (14 FEATURES)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kỹ thuật Đặc trưng: 14 Biến Dự báo Tổng hợp', 6);

  s.addText([
    { text: 'Công thức Toán học của Đặc trưng Nghiệp vụ:\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '1. Sai lệch Số dư Tài khoản Nguồn:\n   errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig\n', options: { fontSize: 11, color: C.textDark } },
    { text: '2. Sai lệch Số dư Tài khoản Đích:\n   errorBalanceDest = oldbalanceDest + amount - newbalanceDest\n', options: { fontSize: 11, color: C.textDark } },
    { text: '3. Cờ Báo Rút cạn Tài khoản:\n   is_drain_account = 1 nếu (oldbalanceOrg > 0 và newbalanceOrig == 0) ngược lại 0\n', options: { fontSize: 11, color: C.textDark } },
    { text: '4. Tỷ lệ Số tiền & Động lực Thời gian:\n   amount_ratio = amount / (oldbalanceOrg + 1), hour = step % 24\n', options: { fontSize: 11, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.2, h: 3.8
  });

  addNotationTable(s, M + 5.4, 1.2, 3.5, [
    ['Số lượng đặc trưng', 'd = 14', 'Không gian đặc trưng tổng hợp sau chế tác'],
    ['Lỗi số dư nguồn', 'Err_org', 'Bắt trọn sai lệch sổ cái tài khoản nguồn'],
    ['Lỗi số dư đích', 'Err_dst', 'Ghi nhận bất thường luân chuyển tiền đích'],
    ['Cờ rút cạn', 'I_drain', 'Dấu hiệu nhị phân vét sạch tài khoản'],
    ['Cờ ban đêm', 'I_night', 'Khung giờ trong khoảng [0..5] sáng']
  ]);
}

// =========================================================================
// SLIDE 7: IMBALANCE MITIGATION STRATEGY
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Xử lý Mất cân bằng Lớp: SMOTE vs ADASYN', 7);

  addHighlightBlock(s, {
    x: M, y: 1.2, w: 4.3, h: 3.75,
    title: 'Nghịch lý Độ chính xác (Accuracy Paradox)',
    text: '• Một bộ phân loại ngây thơ luôn dự đoán "Hợp lệ" sẽ đạt Accuracy 99.87% nhưng bỏ sót 100% các cuộc tấn công gian lận.\n\n• Nguyên tắc Đánh giá Bắt buộc: Lựa chọn mô hình phải được dẫn dắt tuyệt đối bởi Precision, Recall, F1-Score và PR-AUC.',
    type: 'red'
  });

  s.addText([
    { text: 'Chiến lược Tái lấy mẫu Tổng hợp:\n\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '1. SMOTE (Synthetic Minority Over-sampling Technique):\n', options: { bold: true, color: C.blueAccent, fontSize: 11.5 } },
    { text: 'Tạo mẫu thiểu số nhân tạo dọc theo đoạn thẳng nối các điểm lân cận k-NN trong không gian đặc trưng.\n\n', options: { color: C.textDark, fontSize: 11 } },
    { text: '2. ADASYN (Adaptive Synthetic Sampling):\n', options: { bold: true, color: C.blueAccent, fontSize: 11.5 } },
    { text: 'Tự động gán trọng số cho các mẫu thiểu số dựa trên độ khó phân loại, sinh nhiều mẫu hơn ở vùng ranh giới quyết định.', options: { color: C.textDark, fontSize: 11 } }
  ], {
    x: M + 4.6, y: 1.2, w: 4.3, h: 3.75
  });
}

// =========================================================================
// SLIDE 8: END-TO-END SYSTEM PIPELINE
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Pipeline Học máy Toàn diện Chuẩn Chống Rò rỉ Dữ liệu', 8);

  const steps = [
    { n: '1', t: 'Lọc dữ liệu', d: 'Chỉ giữ TRANSFER & CASH_OUT' },
    { n: '2', t: 'Kỹ thuật Đặc trưng', d: 'Tính toán 14 biến toán học' },
    { n: '3', t: 'Phân tầng', d: 'Chia 80/20 Train/Test' },
    { n: '4', t: 'Tái lấy mẫu', d: 'SMOTE/ADASYN CHỈ trên Train' },
    { n: '5', t: 'Huấn luyện', d: 'Fit RF, XGBoost & Autoencoder' },
    { n: '6', t: 'Đánh giá', d: 'Suy luận tập Test (N=40,000)' }
  ];

  const colW = (CW - 0.12 * 5) / 6;
  steps.forEach((st, idx) => {
    const cx = M + idx * (colW + 0.12);
    s.addShape(pptx.shapes.RECTANGLE, {
      x: cx, y: 1.2, w: colW, h: 2.2,
      fill: { color: C.lightGrayBg },
      line: { color: C.blueAccent, width: 1 }
    });
    s.addText(st.n, {
      x: cx, y: 1.25, w: colW, h: 0.35,
      fontSize: 16, fontFace: F.fontNumber, color: C.blueAccent, align: 'center', bold: true
    });
    s.addText(st.t, {
      x: cx + 0.05, y: 1.6, w: colW - 0.1, h: 0.4,
      fontSize: 10.5, fontFace: F.fontTitle, color: C.navyTitle, align: 'center', bold: true
    });
    s.addText(st.d, {
      x: cx + 0.05, y: 2.0, w: colW - 0.1, h: 1.3,
      fontSize: 9, fontFace: F.fontBody, color: C.textMuted, align: 'center'
    });
  });

  addHighlightBlock(s, {
    x: M, y: 3.65, w: CW, h: 1.3,
    title: 'Quy chuẩn Khắt khe Chống Rò rỉ Dữ liệu (Data Leakage)',
    text: '• Việc nhân bản dữ liệu nhân tạo (SMOTE/ADASYN) tuyệt đối CHỈ thực hiện SAU KHI đã phân chia tập Train/Test.\n• Bộ chuẩn hóa StandardScaler chỉ học thông số (mean/std) trên tập Train và biến đổi mù trên tập Test.',
    type: 'blue'
  });
}

// =========================================================================
// SLIDE 9: RANDOM FOREST CLASSIFIER
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kiến trúc Giám sát 1: Random Forest Ensemble', 9);

  s.addText([
    { text: 'Kiến trúc Ensemble Bagging:\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• Xây dựng tập hợp các Cây Quyết định (Decision Trees) độc lập huấn luyện trên các mẫu con bootstrap.\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Giảm phương sai (variance) mà không làm tăng độ chệch (bias), chống hiện tượng đồng tuyến tính cực tốt.\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Cung cấp xếp hạng tầm quan trọng đặc trưng dựa trên Mean Decrease in Impurity (Gini MDI).\n\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: 'Bộ Siêu tham số Tối ưu:\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• n_estimators: 200 (SMOTE) / 500 (ADASYN)\n', options: { fontSize: 11, color: C.textDark } },
    { text: '• max_depth: 20 | min_samples_split: 2 | max_features: sqrt', options: { fontSize: 11, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.0, h: 3.8
  });

  addNotationTable(s, M + 5.3, 1.2, 3.6, [
    ['Kích thước Ensemble', 'B = 200/500', 'Số lượng cây trong rừng'],
    ['Giới hạn Độ sâu', 'd_max = 20', 'Tránh overfitting trên từng cây đơn lẻ'],
    ['Tiêu chí Tách', 'Gini', 'Độ đo độ vấy bẩn thông tin'],
    ['Trọng số Lớp', 'balanced', 'Bù trừ nghịch đảo tần suất xuất hiện']
  ]);
}

// =========================================================================
// SLIDE 10: XGBOOST CLASSIFIER
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kiến trúc Giám sát 2: Extreme Gradient Boosting (XGBoost)', 10);

  s.addText([
    { text: 'Cây Quyết định Tăng cường Độ dốc (GBDT):\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• Tối ưu hóa khai triển Taylor bậc hai của các hàm mất mát khả vi tùy ý.\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Tích hợp điều chuẩn (regularization) L1/L2 trực tiếp để kiểm soát độ phức tạp của các nút lá.\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Tốc độ tính toán vượt trội: Huấn luyện chỉ mất ~41s (nhanh hơn 28 lần so với Random Forest ~1180s).\n\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: 'Bộ Siêu tham số Đã tinh chỉnh:\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• learning_rate (eta): 0.2 | n_estimators: 300\n', options: { fontSize: 11, color: C.textDark } },
    { text: '• max_depth: 8 | subsample: 0.85 | colsample_bytree: 1.0', options: { fontSize: 11, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.0, h: 3.8
  });

  addNotationTable(s, M + 5.3, 1.2, 3.6, [
    ['Hàm mục tiêu', 'Loss + Omega', 'Hàm mục tiêu có thành phần điều chuẩn'],
    ['Tốc độ học', 'eta = 0.2', 'Bước co ngót (shrinkage step size)'],
    ['Độ sâu cây', 'max_depth = 8', 'Mức phân tầng tối đa mỗi vòng boost'],
    ['Lấy mẫu dòng', 'rho = 0.85', 'Tỷ lệ lấy mẫu hàng ngẫu nhiên']
  ]);
}

// =========================================================================
// SLIDE 11: DEEP AUTOENCODER ANOMALY DETECTION
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kiến trúc Không Giám sát 3: Deep Autoencoder', 11);

  s.addText([
    { text: 'Phát hiện Bất thường Bán giám sát Một lớp (One-Class):\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• Mạng được huấn luyện HOÀN TOÀN trên các giao dịch hợp lệ (N = 122,744 mẫu chuẩn).\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Học cấu trúc đa tạp (manifold) biểu diễn không gian giao dịch thông thường.\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Cơ chế phát hiện: Giao dịch gian lận không thể tái tạo chuẩn -> Sai số Tái tạo (MSE) tăng vọt.\n\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: 'Thông số Kiến trúc Mạng:\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• Cấu trúc Đối xứng: 16 -> 8 -> 4 (Nút thắt ẩn) -> 8 -> 16\n', options: { fontSize: 11, color: C.textDark } },
    { text: '• Ngưỡng Quyết định: tau = 0.045456 (Phân vị thứ 95 trên tập Validation)', options: { fontSize: 11, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.0, h: 3.8
  });

  addNotationTable(s, M + 5.3, 1.2, 3.6, [
    ['Nút thắt cổ chai', 'z in R^4', 'Không gian biểu diễn ẩn nén'],
    ['Hàm mất mát', 'MSE(x, x_hat)', 'Sai số bình phương trung bình tái tạo'],
    ['Hàm kích hoạt', 'ReLU', 'Kích hoạt phi tuyến tính các tầng ẩn'],
    ['Ngưỡng cắt', 'tau = 0.0455', 'Điểm ngưỡng quyết định phân vị 95th']
  ]);
}

// =========================================================================
// SLIDE 12: COMPREHENSIVE EXPERIMENTAL BENCHMARK
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kết quả Thực nghiệm: So sánh Đối chuẩn (N = 40,000)', 12);

  const headers = [
    { text: 'Kiến trúc Mô hình', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Tái lấy mẫu', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Precision', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Recall', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'F1-Score', options: { fill: { color: C.tblHdrBg }, color: 'FDE047', bold: true } },
    { text: 'ROC-AUC', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Thời gian Train', options: { fill: { color: C.tblHdrBg }, color: 'CBD5E1', bold: true } }
  ];

  const rows = [
    ['Random Forest', 'SMOTE', '0.9994', '0.9951', '0.9973 (Tốt nhất)', '0.9994', '1187.7s'],
    ['Random Forest', 'ADASYN', '0.9982', '0.9951', '0.9966', '0.9992', '1167.5s'],
    ['XGBoost', 'SMOTE', '0.9976', '0.9951', '0.9963', '0.9993', '41.6s'],
    ['XGBoost', 'ADASYN', '0.9957', '0.9951', '0.9954', '0.9994', '41.5s'],
    ['Autoencoder', 'Không (One-Class)', '0.3822', '0.7523', '0.5069', '0.9318', '215.3s']
  ];

  const tableData = [headers];
  rows.forEach((r, idx) => {
    const isBest = idx === 0;
    const rowCells = r.map((c, cIdx) => ({
      text: c,
      options: {
        fill: { color: isBest ? 'DBEAFE' : (idx % 2 === 0 ? C.tblAltBg : C.whiteBg) },
        color: isBest ? C.navyTitle : (cIdx === 4 ? C.blueAccent : C.textDark),
        bold: isBest || cIdx === 4,
        fontSize: 10
      }
    }));
    tableData.push(rowCells);
  });

  s.addTable(tableData, {
    x: M, y: 1.15, w: CW, h: 2.3,
    border: { pt: 0.5, color: 'CBD5E1' },
    align: 'center',
    margin: [3, 3, 3, 3]
  });

  addHighlightBlock(s, {
    x: M, y: 3.65, w: CW, h: 1.3,
    title: 'Đúc kết Thực nghiệm Cốt lõi',
    bullets: [
      'RF + SMOTE đạt đỉnh F1 (99.73%) với chỉ duy nhất 1 ca Báo động nhầm (FP=1) trên 38,357 giao dịch hợp lệ.',
      'XGBoost đạt năng lực phân loại tương đương (F1 99.63%) nhưng thời gian huấn luyện nhanh hơn 28.5 lần.',
      'Autoencoder đạt Recall 75.23% dù hoàn toàn không được gán nhãn gian lận khi học.'
    ]
  });
}

// =========================================================================
// SLIDE 13: CONFUSION MATRIX COMPARISON
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Ma trận Nhầm lẫn & Phân tích Phân phối Sai số', 13);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_confusion_matrices.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: CW, h: 2.45
    });
  }

  addHighlightBlock(s, {
    x: M, y: 3.75, w: CW, h: 1.25,
    title: 'Đánh đổi giữa False Negative và False Positive',
    bullets: [
      'Cả RF và XGBoost chỉ bỏ sót 8 ca gian lận trên tổng số 1,643 ca gian lận thực tế (Recall = 99.51%).',
      'RF-SMOTE chỉ sinh 1 ca cảnh báo nhầm (FP=1), trong khi Autoencoder sinh 1,998 ca FP do đặc thù cắt ngưỡng không giám sát.'
    ],
    type: 'blue'
  });
}

// =========================================================================
// SLIDE 14: FEATURE IMPORTANCE RANKING
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Tầm quan trọng Đặc trưng: Giá trị Giải thích của Biến Tổng hợp', 14);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_feature_importance.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: 4.6, h: 3.8
    });
  }

  s.addText([
    { text: 'Điểm nhấn từ Trọng số Gain của XGBoost:\n\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• errorBalanceOrig đóng góp tới ~49.9% vào các quyết định phân nhánh của mô hình.\n\n', options: { color: C.textDark, fontSize: 11.5 } },
    { text: '• newbalanceOrig bổ sung thêm ~47.2% sức mạnh dự báo cho cây quyết định.\n\n', options: { color: C.textDark, fontSize: 11.5 } },
    { text: '• Tác động Kết hợp: Các biến độ lệch sổ cái nắm giữ hơn 97% động lực phân loại gian lận, chứng minh hiệu quả vượt bậc của kỹ thuật chế tác đặc trưng nghiệp vụ.', options: { color: C.textDark, fontSize: 11.5 } }
  ], {
    x: M + 4.8, y: 1.2, w: 4.1, h: 3.75
  });
}

// =========================================================================
// SLIDE 15: VISUAL METRICS COMPARISON
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Đánh giá So sánh: Precision, Recall & F1-Score', 15);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_metrics_comparison.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: 4.8, h: 3.8
    });
  }

  s.addText([
    { text: 'Phân tích Hiệu năng Kỹ thuật Tái lấy mẫu:\n\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• SMOTE vượt trội hơn ADASYN một cách nhất quán trên mọi kiến trúc cây.\n\n', options: { color: C.textDark, fontSize: 11.5 } },
    { text: '• ADASYN sinh nhiều mẫu nhiễu ở vùng giao thoa ranh giới, làm tăng nhẹ số ca cảnh báo nhầm.\n\n', options: { color: C.textDark, fontSize: 11.5 } },
    { text: '• Khuyến nghị Vận hành: Kết hợp SMOTE với XGBoost để đạt thông lượng cao nhất và độ chính xác tối ưu trong môi trường sản xuất.', options: { color: C.textDark, fontSize: 11.5 } }
  ], {
    x: M + 5.0, y: 1.2, w: 3.9, h: 3.75
  });
}

// =========================================================================
// SLIDE 16: AUTOENCODER RECONSTRUCTION ERROR ANALYSIS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Cắt ngưỡng Anomaly của Autoencoder & Ranh giới Quyết định', 16);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_autoencoder_dist.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: 4.6, h: 3.8
    });
  }

  s.addText([
    { text: 'Động lực Quét Ngưỡng (Threshold Sweep):\n\n', options: { bold: true, color: C.navyTitle, fontSize: 12.5 } },
    { text: '• Ngưỡng Phân vị 95th (tau = 0.0455):\nCân bằng giữa Recall (75.2%) và Precision (38.2%).\n\n', options: { color: C.textDark, fontSize: 11.5 } },
    { text: '• Ngưỡng Phân vị 99.9th (tau = 0.7460):\nPrecision tăng vọt lên 91.5% nhưng Recall giảm xuống 25.4%.\n\n', options: { color: C.textDark, fontSize: 11.5 } },
    { text: '• Vai trò Vận hành: Đóng vai trò lớp phòng thủ Zero-day thứ cấp đắc lực trước các hình thức gian lận mới chưa từng xuất hiện nhãn.', options: { color: C.textDark, fontSize: 11.5 } }
  ], {
    x: M + 4.8, y: 1.2, w: 4.1, h: 3.75
  });
}

// =========================================================================
// SLIDE 17: STREAMLIT WEB APP DEMO
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Trình diễn Trực quan: Dashboard Thời gian Thực trên Streamlit', 17);

  addHighlightBlock(s, {
    x: M, y: 1.2, w: 4.3, h: 3.75,
    title: 'Pipeline Suy luận Thời gian Thực',
    bullets: [
      'Giao diện Streamlit tinh gọn với đồng hồ đo xác suất rủi ro trực quan.',
      'Engine trích xuất đặc trưng tức thì (chuyển đổi input người dùng thành vector 14 chiều).',
      'Tải mô hình XGBoost / Random Forest đã đóng gói qua Joblib.',
      'Độ trễ suy luận dưới 1 mili-giây cho từng giao dịch đơn lẻ.'
    ]
  });

  addHighlightBlock(s, {
    x: M + 4.6, y: 1.2, w: 4.3, h: 3.75,
    title: 'Các Kịch bản Mô phỏng Thực nghiệm',
    bullets: [
      'Kịch bản 1 (Giao dịch Chuẩn): Chuyển tiền thông thường với biến động số dư hợp lệ -> Kết quả: AN TOÀN (99.9%).',
      'Kịch bản 2 (Rút cạn Tài khoản): Chuyển tiền giá trị lớn khiến số dư nguồn về 0 -> Kết quả: GIAN LẬN NGUY CƠ CAO (99.8%).',
      'Chế độ Hàng loạt: Tải file CSV để chấm điểm đồng loạt và xuất báo cáo kiểm toán tuân thủ.'
    ]
  });
}

// =========================================================================
// SLIDE 18: SUMMARY OF CONTRIBUTIONS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Tổng kết Đóng góp Cốt lõi của Đề tài', 18);

  const contribs = [
    { title: '1. Quản trị Dữ liệu Chuẩn mực', desc: 'Xây dựng pipeline leak-free toàn diện, giải quyết triệt để mất cân bằng 0.13%.' },
    { title: '2. Khám phá Đặc trưng Tác động Cao', desc: 'Xây dựng phương trình sai lệch số dư đóng góp hơn 97% gain phân loại.' },
    { title: '3. Chỉ số Thực nghiệm Vượt trội', desc: 'Đạt F1-Score > 0.996 và Recall > 0.995, ngăn chặn 99.5% thiệt hại tài chính.' },
    { title: '4. Sẵn sàng Triển khai Vận hành', desc: 'Đóng gói thành dashboard Streamlit hoàn chỉnh cho suy luận real-time.' }
  ];

  const cw = (CW - 0.25) / 2;
  contribs.forEach((c, i) => {
    const rx = i % 2 === 0 ? M : M + cw + 0.25;
    const ry = i < 2 ? 1.2 : 2.65;
    addHighlightBlock(s, {
      x: rx, y: ry, w: cw, h: 1.3,
      title: c.title,
      text: c.desc,
      type: 'blue'
    });
  });

  addHighlightBlock(s, {
    x: M, y: 4.15, w: CW, h: 0.85,
    title: 'Khuyến nghị Lựa chọn Mô hình Chính',
    text: 'XGBoost + SMOTE được lựa chọn làm kiến trúc tối ưu cho môi trường sản xuất nhờ thông lượng suy luận cực cao và dung lượng bộ nhớ nhẹ.',
    type: 'blue'
  });
}

// =========================================================================
// SLIDE 19: LIMITATIONS & FUTURE EXTENSIONS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Hạn chế Nghiên cứu & Định hướng Tương lai', 19);

  addHighlightBlock(s, {
    x: M, y: 1.2, w: 4.3, h: 3.75,
    title: 'Hạn chế Hiện tại',
    bullets: [
      'Khoảng cách Dữ liệu Mô phỏng: PaySim chưa phản ánh hết các thủ thuật lẩn tránh zero-day trong ngân hàng thực tế.',
      'Phạm vi Đặc trưng Tĩnh: Chưa khai thác topo mạng lưới quan hệ giữa các tài khoản chuyển tiền liên thông.',
      'Chi phí Huấn luyện lại: Random Forest tốn nhiều thời gian huấn luyện lại khi luồng dữ liệu biến động liên tục.'
    ],
    type: 'red'
  });

  addHighlightBlock(s, {
    x: M + 4.6, y: 1.2, w: 4.3, h: 3.75,
    title: 'Định hướng Tương lai',
    bullets: [
      'Graph Neural Networks (GNN): Ứng dụng GCN / GraphSAGE để phát hiện các đồ thị con rửa tiền có cấu trúc.',
      'Kiến trúc Xử lý Luồng: Tích hợp Apache Kafka / Apache Flink để xử lý phân tán với độ trễ dưới 1 giây.',
      'Explainable AI (XAI): Tích hợp SHAP / TreeExplainer để giải thích lý do chặn giao dịch phục vụ yêu cầu pháp lý.'
    ],
    type: 'blue'
  });
}

// =========================================================================
// SLIDE 20: Q&A / CONCLUSION (Exact CS115 Style)
// =========================================================================
{
  const s = pptx.addSlide();
  s.background = { color: C.navyBg };

  s.addText('CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE!', {
    x: M, y: 1.3, w: CW, h: 0.6,
    fontSize: 24, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText('CS106 — HỆ THỐNG PHÁT HIỆN GIAN LẬN TÀI CHÍNH (NHÓM 09)', {
    x: M, y: 1.95, w: CW, h: 0.35,
    fontSize: 13, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  s.addShape(pptx.shapes.RECTANGLE, {
    x: M + 1.2, y: 2.6, w: 6.5, h: 2.2,
    fill: { color: '21295C' },
    line: { color: '3B82F6', width: 1 }
  });

  s.addText('PHIÊN HỎI ĐÁP (Q&A)', {
    x: M + 1.2, y: 2.75, w: 6.5, h: 0.35,
    fontSize: 14, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText('• Mã nguồn Dự án: https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection\n• Tài liệu Tham khảo: Lopez-Rojas et al., PaySim Mobile Money Simulator, 2016\n• Thư viện Sử dụng: Scikit-learn, XGBoost, Streamlit, Imbalanced-learn\n\nNhóm 09 rất mong nhận được những câu hỏi và góp ý quý báu từ Hội đồng!', {
    x: M, y: 3.4, w: CW, h: 1.4,
    fontSize: 10.5, fontFace: F.fontBody, color: 'CBD5E1', align: 'center'
  });
}

const outputFile = path.join(__dirname, '[Nhom9]_Slide_FraudDetection_Academic_VN.pptx');
pptx.writeFile({ fileName: outputFile })
  .then(() => {
    console.log('Successfully generated PPTX: ' + outputFile);
  })
  .catch(err => {
    console.error('Error generating PPTX:', err);
    process.exit(1);
  });
