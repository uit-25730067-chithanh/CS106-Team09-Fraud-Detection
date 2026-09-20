const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9'; // 10" x 5.625"

// -------------------------------------------------------------
// CS106 UIT Academic Design System (Refined & Balanced)
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
  tblAltBg: 'F1F5F9',    // Table Row Alt
  pillBlue: '2563EB',    // Section Divider Pill Blue
  videoDarkBg: '0F172A',  // Video Player Dark Box
  videoBorder: '3B82F6'  // Video Player Tech Border
};

const F = {
  fontTitle: 'Segoe UI',
  fontBody: 'Segoe UI',
  fontNumber: 'Cambria',
  fontCode: 'Consolas',
  coverTitle: 32,
  slideTitle: 19,
  subTitle: 14,
  body: 10.5,
  bodyBold: 10.5,
  small: 9.5,
  caption: 8.5
};

const SW = 10.0;
const SH = 5.625;
const M = 0.55;
const CW = SW - 2 * M; // 8.9
const TOTAL_PAGES = 21;

// Slide Header / Footer Helper with comfortable breathing room
function addAcademicHeader(slide, title, pageNum, totalPages = TOTAL_PAGES) {
  slide.background = { color: C.whiteBg };

  // Top University Banner
  slide.addText('TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐHQG-HCM', {
    x: M, y: 0.20, w: CW, h: 0.22,
    fontSize: 8.5, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  // Slide Title (Clean single line, comfortable height)
  slide.addText(title, {
    x: M, y: 0.46, w: CW, h: 0.44,
    fontSize: F.slideTitle, fontFace: F.fontTitle, color: C.navyTitle, bold: true, shrinkText: true
  });

  // Header separator line
  slide.addShape(pptx.shapes.LINE, {
    x: M, y: 0.94, w: CW, h: 0,
    line: { color: 'E2E8F0', width: 1 }
  });

  // Bottom Footer (Clean dash instead of em-dash)
  slide.addText('CS106: Trí tuệ Nhân tạo - Nhóm 09 - Báo cáo Đồ án: Phát hiện Gian lận Tài chính', {
    x: M, y: SH - 0.35, w: 6.8, h: 0.2,
    fontSize: 8.5, fontFace: F.fontBody, color: C.textDim
  });

  // Bottom Page Number
  slide.addText(`${pageNum} / ${totalPages}`, {
    x: SW - M - 1.5, y: SH - 0.35, w: 1.5, h: 0.2,
    fontSize: 8.5, fontFace: F.fontBody, color: C.textDim, align: 'right'
  });
}

// Helper: Section Divider Slide with comfortable spacing
function addSectionDivider(slide, partNumber, partTitle, subBullets) {
  slide.background = { color: C.navyBg };

  // Top Header Banner
  slide.addText('TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐHQG-HCM  •  BÁO CÁO ĐỒ ÁN CS106', {
    x: M, y: 0.50, w: CW, h: 0.25,
    fontSize: 9.5, fontFace: 'Segoe UI', color: '93C5FD', align: 'center', bold: true
  });

  // Section Pill
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: (SW - 1.8) / 2, y: 1.15, w: 1.8, h: 0.42,
    fill: { color: C.pillBlue },
    line: { color: '60A5FA', width: 1 },
    rectRadius: 0.1
  });
  slide.addText(partNumber, {
    x: (SW - 1.8) / 2, y: 1.15, w: 1.8, h: 0.42,
    fontSize: 13, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  // Section Title
  slide.addText(partTitle, {
    x: M, y: 1.75, w: CW, h: 0.75,
    fontSize: 22, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true, shrinkText: true
  });

  // Accent Underline
  slide.addShape(pptx.shapes.LINE, {
    x: (SW - 3.0) / 2, y: 2.65, w: 3.0, h: 0,
    line: { color: 'F59E0B', width: 2.5 }
  });

  // Sub-bullets Box
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: M + 0.85, y: 2.95, w: CW - 1.7, h: 2.05,
    fill: { color: '172048' },
    line: { color: '3B82F6', width: 1 },
    rectRadius: 0.15
  });

  const textArr = subBullets.map((b, idx) => ({
    text: b,
    options: {
      bullet: true,
      breakLine: idx < subBullets.length - 1,
      color: 'E2E8F0',
      fontSize: 11,
      fontFace: F.fontBody,
      lineSpacingMultiple: 1.25,
      paraSpaceAfter: 10
    }
  }));

  slide.addText(textArr, {
    x: M + 1.15, y: 3.15, w: CW - 2.3, h: 1.65,
    margin: [2, 5, 2, 5],
    shrinkText: true
  });
}

// Helper: Variable & Notation Glossary Table (Top-Right / Dedicated Placement)
function addVariableGlossaryTable(slide, x, y, w, rows, title = '📋 Bảng Chú giải Biến & Ký hiệu', colWidths = null) {
  const finalColWidths = colWidths || [w * 0.32, w * 0.28, w * 0.40];

  const tableData = [
    [
      { text: 'Ký hiệu / Biến', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true, fontSize: 8.5 } },
      { text: 'Tên Ý nghĩa', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true, fontSize: 8.5 } },
      { text: 'Mô tả Nghiệp vụ', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true, fontSize: 8.5 } }
    ]
  ];

  rows.forEach(r => {
    tableData.push([
      { text: r[0], options: { bold: true, fontFace: F.fontCode, color: C.navyTitle } },
      { text: r[1], options: { bold: true, color: C.blueAccent } },
      { text: r[2], options: { color: C.textDark } }
    ]);
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: y, w: w, h: 0.26,
    fill: { color: 'E2E8F0' },
    line: { color: 'CBD5E1', width: 1 }
  });
  slide.addText(title, {
    x: x + 0.1, y: y + 0.02, w: w - 0.2, h: 0.22,
    fontSize: 8.5, fontFace: F.fontTitle, bold: true, color: C.navyTitle
  });

  slideTable(slide, tableData, x, y + 0.28, w, finalColWidths, 8.0);
}

// Helper: Highlight block with consistent padding & line spacing
function addHighlightBlock(slide, opts) {
  const { x, y, w, h, title, text, bullets, type = 'blue', fontSize = 9.2 } = opts;
  const isRed = type === 'red';
  const fill = isRed ? C.redBox : C.skyBox;
  const border = isRed ? C.redBorder : C.skyBorder;
  const titleColor = isRed ? C.dangerRed : C.navyTitle;

  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: fill },
    line: { color: border, width: 1 }
  });

  let curY = y + 0.08;
  if (title) {
    slide.addText(title, {
      x: x + 0.15, y: curY, w: w - 0.3, h: 0.24,
      fontSize: fontSize + 0.8, fontFace: F.fontTitle, bold: true, color: titleColor
    });
    curY += 0.24;
  }

  if (text) {
    slide.addText(text, {
      x: x + 0.15, y: curY, w: w - 0.3, h: h - (curY - y) - 0.08,
      fontSize: fontSize, fontFace: F.fontBody, color: C.textDark,
      lineSpacingMultiple: 1.2,
      margin: [2, 4, 2, 4],
      shrinkText: true
    });
  } else if (bullets) {
    const textArr = bullets.map((b, idx) => ({
      text: b,
      options: {
        bullet: true,
        breakLine: idx < bullets.length - 1,
        color: C.textDark,
        fontSize: fontSize,
        fontFace: F.fontBody,
        lineSpacingMultiple: 1.18,
        paraSpaceAfter: 4
      }
    }));

    slide.addText(textArr, {
      x: x + 0.15, y: curY, w: w - 0.3, h: h - (curY - y) - 0.08,
      margin: [2, 4, 2, 4],
      shrinkText: true
    });
  }
}

// Helper: Academic Table Renderer
function slideTable(slide, rows, x, y, w, colWidths, fontSize = 8.5) {
  const formattedRows = rows.map((row, rowIdx) => {
    return row.map((cell) => {
      let cellObj = typeof cell === 'string' ? { text: cell } : cell;
      let opts = cellObj.options || {};

      if (rowIdx === 0) {
        opts.fill = opts.fill || { color: C.tblHdrBg };
        opts.color = opts.color || 'FFFFFF';
        opts.bold = true;
        opts.align = opts.align || 'center';
      } else {
        if (!opts.fill) {
          opts.fill = { color: rowIdx % 2 === 1 ? 'FFFFFF' : C.tblAltBg };
        }
        opts.color = opts.color || C.textDark;
      }

      opts.fontSize = opts.fontSize || fontSize;
      opts.fontFace = opts.fontFace || F.fontBody;
      opts.valign = 'middle';
      opts.margin = opts.margin || [2, 4, 2, 4];

      return { text: cellObj.text, options: opts };
    });
  });

  slide.addTable(formattedRows, {
    x: x, y: y, w: w,
    colW: colWidths,
    border: { type: 'solid', pt: 0.5, color: 'CBD5E1' }
  });
}

// =========================================================================
// SLIDE 1: TITLE (COVER)
// =========================================================================
{
  const s = pptx.addSlide();
  s.background = { color: C.navyBg };

  s.addText('TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐHQG-HCM\nKHOA KHOA HỌC MÁY TÍNH', {
    x: M, y: 0.45, w: CW, h: 0.48,
    fontSize: 9.5, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true, lineSpacingMultiple: 1.2
  });

  s.addText('PHÁT HIỆN GIAN LẬN TÀI CHÍNH', {
    x: M, y: 1.30, w: CW, h: 0.65,
    fontSize: 33, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText('Ứng dụng Machine Learning & Deep Learning trên Tập dữ liệu Mô phỏng PaySim', {
    x: M, y: 2.05, w: CW, h: 0.35,
    fontSize: 14, fontFace: 'Georgia', color: '93C5FD', align: 'center', italic: true
  });

  s.addText('Môn học: CS106 - Trí tuệ Nhân tạo  |  GVHD: PGS.TS. Nguyễn Đình Hiển', {
    x: M, y: 2.75, w: CW, h: 0.3,
    fontSize: 12.5, fontFace: F.fontBody, color: 'FFFFFF', align: 'center'
  });

  s.addShape(pptx.shapes.LINE, {
    x: M + 2.5, y: 3.25, w: 1.3, h: 0,
    line: { color: '93C5FD', width: 2 }
  });
  s.addText('Nhóm 09', {
    x: M + 3.85, y: 3.12, w: 1.2, h: 0.28,
    fontSize: 12.5, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });
  s.addShape(pptx.shapes.LINE, {
    x: M + 5.1, y: 3.25, w: 1.3, h: 0,
    line: { color: '93C5FD', width: 2 }
  });

  s.addText('Trần Hoàng Hôn (26410046)  •  Đặng Chí Thanh (25730067)  •  Nguyễn Duy Khang (26410055)\nHoàng Cao Sơn (25730061)  •  Vũ Văn Duy (26410031)  •  Bùi Thị Mỷ Cẩm (25730013)  •  Phạm Thành Trung (26410141)', {
    x: M, y: 3.65, w: CW, h: 0.55,
    fontSize: 10, fontFace: F.fontBody, color: 'CBD5E1', align: 'center', lineSpacingMultiple: 1.3
  });

  s.addText('TP. Hồ Chí Minh, Tháng 09/2026', {
    x: M, y: 4.85, w: CW, h: 0.25,
    fontSize: 9, fontFace: F.fontBody, color: '94A3B8', align: 'center', italic: true
  });
}

// =========================================================================
// SLIDE 2: AGENDA (Roadmap)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'NỘI DUNG BÁO CÁO & LỘ TRÌNH', 2, TOTAL_PAGES);

  const agenda = [
    { num: '01', title: 'Giới thiệu & Phát biểu Bài toán', desc: 'Bối cảnh tài chính, Extreme Class Imbalance (0.13%) và Cost Asymmetry.', color: '60A5FA' },
    { num: '02', title: 'Phân tích Khám phá Dữ liệu & Kỹ thuật Đặc trưng', desc: 'Khu biệt loại giao dịch, dấu vết rút cạn số dư và 14 engineered features.', color: '3B82F6' },
    { num: '03', title: 'Phương pháp Đề xuất & Kiến trúc Pipeline', desc: 'Quy chuẩn Leak-Free, Random Forest vs. XGBoost và Deep Autoencoder.', color: '2563EB' },
    { num: '04', title: 'Kết quả Thực nghiệm & Đánh giá So sánh', desc: 'Benchmark đa chỉ số, Confusion Matrix, Feature Split Gains và Anomaly Cutoff.', color: '1D4ED8' },
    { num: '05', title: 'Hệ thống Demo & Định hướng Tương lai', desc: 'Dashboard Streamlit thời gian thực, kịch bản kiểm thử và lộ trình mở rộng GNN.', color: '1E3A8A' }
  ];

  const rowH = 0.65;
  agenda.forEach((item, idx) => {
    const cy = 1.12 + idx * (rowH + 0.15);
    s.addShape(pptx.shapes.RECTANGLE, {
      x: M + 0.2, y: cy, w: 0.75, h: rowH,
      fill: { color: item.color },
      line: { type: 'none' }
    });
    s.addText(item.num, {
      x: M + 0.2, y: cy, w: 0.75, h: rowH,
      fontSize: 18, fontFace: F.fontNumber, color: 'FFFFFF', align: 'center', bold: true
    });
    s.addText([
      { text: item.title + '\n', options: { bold: true, fontSize: 12.5, color: C.navyTitle } },
      { text: item.desc, options: { fontSize: 10, color: C.textMuted, lineSpacingMultiple: 1.15 } }
    ], {
      x: M + 1.15, y: cy, w: 7.5, h: rowH,
      margin: [2, 4, 2, 4],
      shrinkText: true
    });
  });
}

// =========================================================================
// SLIDE 3: DIVIDER 01
// =========================================================================
{
  const s = pptx.addSlide();
  addSectionDivider(s, 'PHẦN 01', 'GIỚI THIỆU & PHÁT BIỂU BÀI TOÁN', [
    'Bối cảnh Công nghiệp & Sự bùng nổ Mobile Money',
    'Thách thức Extreme Class Imbalance (~0.13%) & Tổn thất Bất đối xứng (Cost Asymmetry)',
    'Phát biểu Bài toán Hình thức & Mục tiêu Nghiên cứu'
  ]);
}

// =========================================================================
// SLIDE 4: PROBLEM MOTIVATION & TECHNICAL CHALLENGES
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Động lực Nghiên cứu & Thách thức Kỹ thuật', 4, TOTAL_PAGES);

  // Left Content with clear vertical distribution & line spacing
  s.addText([
    { text: '1. Bối cảnh Thực tiễn & Quy mô\n', options: { bold: true, color: C.navyTitle, fontSize: 12 } },
    { text: '• Giao dịch Mobile Money tăng trưởng bùng nổ, kéo theo các thủ đoạn gian lận tinh vi.\n', options: { fontSize: 10.5, color: C.textDark, lineSpacingMultiple: 1.2 } },
    { text: '• Hệ thống phòng thủ đòi hỏi độ trễ suy luận real-time (< 100ms) trước khi tiền bị tẩu tán.\n\n', options: { fontSize: 10.5, color: C.textDark, lineSpacingMultiple: 1.2 } },

    { text: '2. Thách thức Extreme Class Imbalance (~0.13%)\n', options: { bold: true, color: C.navyTitle, fontSize: 12 } },
    { text: '• Gian lận chỉ chiếm ~1 trên 800 giao dịch (8,213 ca trên 6.36M sự kiện trong PaySim).\n', options: { fontSize: 10.5, color: C.textDark, lineSpacingMultiple: 1.2 } },
    { text: '• Cost Asymmetry: Bỏ sót gian lận (FN) gây mất vốn trực tiếp, trong khi Báo động nhầm (FP) chỉ gây gián đoạn trải nghiệm người dùng.\n\n', options: { fontSize: 10.5, color: C.textDark, lineSpacingMultiple: 1.2 } },

    { text: '3. Hành vi Gian lận Phi tĩnh (Non-Stationary)\n', options: { bold: true, color: C.navyTitle, fontSize: 12 } },
    { text: '• Kẻ gian liên tục biến đổi thủ đoạn luân chuyển tiền để lẩn tránh các bộ lọc luật tĩnh.', options: { fontSize: 10.5, color: C.textDark, lineSpacingMultiple: 1.2 } }
  ], {
    x: M, y: 1.08, w: 4.8, h: 4.0,
    margin: [2, 4, 2, 4],
    shrinkText: true
  });

  // Right Side: Notation Table & Goals Box
  addVariableGlossaryTable(s, M + 5.0, 1.08, 3.9, [
    ['Y ∈ {0, 1}', 'Target Label', '1 = Fraud (Gian lận), 0 = Legitimate (Hợp lệ)'],
    ['IR ≈ 0.13%', 'Imbalance Ratio', '8,213 ca gian lận trên 6.36M giao dịch tổng'],
    ['Recall / PR-AUC', 'Primary Metric', 'Tối đa hóa bắt gian lận, Accuracy bị vô hiệu hóa'],
    ['C_FN >> C_FP', 'Cost Asymmetry', 'Phạt bỏ sót gian lận lớn hơn nhiều cảnh báo nhầm']
  ], '📋 Ký hiệu Toán học & Khái niệm Cốt lõi');

  addHighlightBlock(s, {
    x: M + 5.0, y: 2.85, w: 3.9, h: 2.2,
    title: 'Mục tiêu Nghiên cứu Cốt lõi',
    bullets: [
      'Xây dựng end-to-end ML pipeline chuẩn, đảm bảo Leak-Free tuyệt đối.',
      'Thiết kế 14 features bắt trọn sai lệch số dư tài khoản.',
      'So sánh Ensemble Trees với Unsupervised Deep Autoencoder bắt Zero-Day.',
      'Triển khai interactive dashboard phục vụ ra quyết định thời gian thực.'
    ],
    fontSize: 9.5
  });
}

// =========================================================================
// SLIDE 5: DATASET CHARACTERISTICS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Tập Dữ liệu PaySim: Thuộc tính Thống kê', 5, TOTAL_PAGES);

  // 3 Top Stat Cards
  const statCardW = (CW - 0.3) / 3;
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 1.08, w: statCardW, h: 0.82, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addText('Quy mô Mẫu sau Downsample', { x: M + 0.1, y: 1.14, w: statCardW - 0.2, h: 0.20, fontSize: 9.5, bold: true, color: C.navyTitle });
  s.addText('N = 200,000 sự kiện', { x: M + 0.1, y: 1.34, w: statCardW - 0.2, h: 0.32, fontSize: 13.5, bold: true, color: C.blueAccent });
  s.addText('Stratified sample bảo toàn 100% fraud', { x: M + 0.1, y: 1.66, w: statCardW - 0.2, h: 0.18, fontSize: 8.5, color: C.textMuted });

  s.addShape(pptx.shapes.RECTANGLE, { x: M + statCardW + 0.15, y: 1.08, w: statCardW, h: 0.82, fill: { color: C.redBox }, line: { color: C.redBorder } });
  s.addText('Số ca Gian lận (isFraud = 1)', { x: M + statCardW + 0.25, y: 1.14, w: statCardW - 0.2, h: 0.20, fontSize: 9.5, bold: true, color: C.dangerRed });
  s.addText('8,213 ca ground-truth', { x: M + statCardW + 0.25, y: 1.34, w: statCardW - 0.2, h: 0.32, fontSize: 13.5, bold: true, color: C.dangerRed });
  s.addText('Tập trung tuyệt đối ở 2 loại giao dịch', { x: M + statCardW + 0.25, y: 1.66, w: statCardW - 0.2, h: 0.18, fontSize: 8.5, color: C.textMuted });

  s.addShape(pptx.shapes.RECTANGLE, { x: M + (statCardW + 0.15) * 2, y: 1.08, w: statCardW, h: 0.82, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addText('Không gian Đặc trưng Mở rộng', { x: M + (statCardW + 0.15) * 2 + 0.1, y: 1.14, w: statCardW - 0.2, h: 0.20, fontSize: 9.5, bold: true, color: C.navyTitle });
  s.addText('11 → 14 Đặc trưng Miền', { x: M + (statCardW + 0.15) * 2 + 0.1, y: 1.34, w: statCardW - 0.2, h: 0.32, fontSize: 13.5, bold: true, color: C.blueAccent });
  s.addText('Bổ sung các phương trình sai lệch số dư', { x: M + (statCardW + 0.15) * 2 + 0.1, y: 1.66, w: statCardW - 0.2, h: 0.18, fontSize: 8.5, color: C.textMuted });

  // Feature Table
  const tableData = [
    [
      { text: 'Tên Đặc trưng', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true, fontSize: 9.5 } },
      { text: 'Kiểu Dữ liệu', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true, fontSize: 9.5 } },
      { text: 'Ý nghĩa Miền & Nghiệp vụ Giao dịch', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true, fontSize: 9.5 } }
    ],
    [{ text: 'step', options: { bold: true, fontFace: F.fontCode } }, { text: 'Số nguyên (Integer)' }, { text: 'Bước thời gian theo giờ (1..744, tương ứng 30 ngày mô phỏng)' }],
    [{ text: 'type', options: { bold: true, color: C.dangerRed, fontFace: F.fontCode } }, { text: 'Phân loại (Categorical)' }, { text: 'Loại giao dịch: CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT' }],
    [{ text: 'amount', options: { bold: true, fontFace: F.fontCode } }, { text: 'Liên tục (Continuous)' }, { text: 'Số tiền thực hiện giao dịch (đơn vị tiền tệ cục bộ)' }],
    [{ text: 'oldbalanceOrg / newbalanceOrig', options: { bold: true, fontFace: F.fontCode } }, { text: 'Liên tục (Continuous)' }, { text: 'Số dư trước và ngay sau giao dịch của tài khoản nguồn (sender)' }],
    [{ text: 'oldbalanceDest / newbalanceDest', options: { bold: true, fontFace: F.fontCode } }, { text: 'Liên tục (Continuous)' }, { text: 'Số dư trước và ngay sau giao dịch của tài khoản đích (recipient)' }]
  ];

  slideTable(s, tableData, M, 2.02, CW, [CW * 0.32, CW * 0.23, CW * 0.45], 8.8);

  addHighlightBlock(s, {
    x: M, y: 4.08, w: CW, h: 0.98,
    title: 'Insight Quan trọng từ Phân bố Dữ liệu',
    text: '100% tất cả các ca gian lận trong 6.36M giao dịch CHỈ xuất hiện ở 2 loại: TRANSFER và CASH_OUT. Các loại PAYMENT, CASH_IN và DEBIT hoàn toàn an toàn (0% gian lận). Do đó, bước tiền xử lý lọc chỉ giữ lại TRANSFER & CASH_OUT giúp triệt tiêu 70% dữ liệu nhiễu.',
    type: 'blue',
    fontSize: 9.3
  });
}

// =========================================================================
// SLIDE 6: DIVIDER 02
// =========================================================================
{
  const s = pptx.addSlide();
  addSectionDivider(s, 'PHẦN 02', 'PHÂN TÍCH KHÁM PHÁ DỮ LIỆU & KỸ THUẬT ĐẶC TRƯNG', [
    'Phân tích Dấu vết Hành vi Thực nghiệm (Behavioral Signatures)',
    'Công thức Toán học của 14 Engineered Domain Features',
    'Xử lý Mất cân bằng Lớp: SMOTE vs. ADASYN Formulation'
  ]);
}

// =========================================================================
// SLIDE 7: EDA BEHAVIORAL SIGNATURES
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Phân tích Khám phá Dữ liệu: Dấu vết Hành vi Cốt lõi', 7, TOTAL_PAGES);

  const cardW = (CW - 0.3) / 3;
  const cardH = 3.92;

  // Card 1: Category Confinement
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 1.10, w: cardW, h: cardH, fill: { color: C.skyBox }, line: { color: C.skyBorder, width: 1.5 } });
  s.addShape(pptx.shapes.RECTANGLE, { x: M + 0.15, y: 1.25, w: cardW - 0.3, h: 0.35, fill: { color: C.pillBlue } });
  s.addText('100% GIAN LẬN KHU BIỆT', { x: M + 0.15, y: 1.25, w: cardW - 0.3, h: 0.35, fontSize: 10.5, bold: true, color: 'FFFFFF', align: 'center' });
  s.addText('Phát hiện 1: Khoanh vùng Loại Giao dịch', { x: M + 0.15, y: 1.70, w: cardW - 0.3, h: 0.3, fontSize: 11, bold: true, color: C.navyTitle });
  s.addText([
    { text: '• 100% gian lận xảy ra duy nhất ở 2 loại giao dịch: ', options: { color: C.textDark } },
    { text: 'TRANSFER và CASH_OUT.\n', options: { bold: true, color: C.dangerRed } },
    { text: '• Các loại PAYMENT, CASH_IN, DEBIT hoàn toàn không có gian lận (0%).\n\n', options: { color: C.textDark } },
    { text: '• Hành động Pipeline: ', options: { bold: true, color: C.blueAccent } },
    { text: 'Lọc tập dữ liệu chỉ giữ lại TRANSFER & CASH_OUT, triệt tiêu ngay 70% dữ liệu nhiễu vô ích.', options: { color: C.textDark } }
  ], { x: M + 0.15, y: 2.05, w: cardW - 0.3, h: cardH - 1.15, fontSize: 9.8, lineSpacingMultiple: 1.22, shrinkText: true, margin: [2, 4, 2, 4] });

  // Card 2: Total Account Drain
  s.addShape(pptx.shapes.RECTANGLE, { x: M + cardW + 0.15, y: 1.10, w: cardW, h: cardH, fill: { color: C.redBox }, line: { color: C.redBorder, width: 1.5 } });
  s.addShape(pptx.shapes.RECTANGLE, { x: M + cardW + 0.3, y: 1.25, w: cardW - 0.3, h: 0.35, fill: { color: C.dangerRed } });
  s.addText('97.55% TỔNG SỐ CA GIAN LẬN', { x: M + cardW + 0.3, y: 1.25, w: cardW - 0.3, h: 0.35, fontSize: 10.5, bold: true, color: 'FFFFFF', align: 'center' });
  s.addText('Phát hiện 2: Vét Sạch Số Dư Nguồn', { x: M + cardW + 0.3, y: 1.70, w: cardW - 0.3, h: 0.3, fontSize: 11, bold: true, color: C.dangerRed });
  s.addText([
    { text: '• Trong 97.55% giao dịch gian lận, tài khoản nạn nhân bị rút cạn sạch về 0: ', options: { color: C.textDark } },
    { text: 'newbalanceOrig == 0.\n', options: { bold: true, color: C.navyTitle } },
    { text: '• Kẻ gian tối đa hóa số tiền lấy cắp trong 1 lần duy nhất trước khi bị khóa thẻ.\n\n', options: { color: C.textDark } },
    { text: '• Tín hiệu Cốt lõi: ', options: { bold: true, color: C.dangerRed } },
    { text: '97.55% ca gian lận rút cạn tài khoản nguồn; kết hợp sai lệch errorBalanceOrig mới tạo phân loại mạnh.', options: { color: C.textDark } }
  ], { x: M + cardW + 0.3, y: 2.05, w: cardW - 0.3, h: cardH - 1.15, fontSize: 9.8, lineSpacingMultiple: 1.22, shrinkText: true, margin: [2, 4, 2, 4] });

  // Card 3: Destination Ledger Mismatch
  s.addShape(pptx.shapes.RECTANGLE, { x: M + (cardW + 0.15) * 2, y: 1.10, w: cardW, h: cardH, fill: { color: C.skyBox }, line: { color: C.skyBorder, width: 1.5 } });
  s.addShape(pptx.shapes.RECTANGLE, { x: M + (cardW + 0.15) * 2 + 0.15, y: 1.25, w: cardW - 0.3, h: 0.35, fill: { color: '1D4ED8' } });
  s.addText('BẤT THƯỜNG BIẾN ĐỘNG SỐ DƯ', { x: M + (cardW + 0.15) * 2 + 0.15, y: 1.25, w: cardW - 0.3, h: 0.35, fontSize: 10.5, bold: true, color: 'FFFFFF', align: 'center' });
  s.addText('Phát hiện 3: Sai Lệch số dư đích', { x: M + (cardW + 0.15) * 2 + 0.15, y: 1.70, w: cardW - 0.3, h: 0.3, fontSize: 11, bold: true, color: C.navyTitle });
  s.addText([
    { text: '• Tỷ lệ lớn giao dịch gian lận không làm tăng số dư tài khoản đích theo sổ sách: ', options: { color: C.textDark } },
    { text: 'newbalanceDest ≈ 0.\n', options: { bold: true, color: C.navyTitle } },
    { text: '• Phản ánh tài khoản rác (mule account) hoặc luân chuyển rửa tiền đa tầng tức thì.\n\n', options: { color: C.textDark } },
    { text: '• Tín hiệu Cốt lõi: ', options: { bold: true, color: C.blueAccent } },
    { text: 'Sai lệch số dư đích vạch trần hành vi rút tiền bất hợp pháp.', options: { color: C.textDark } }
  ], { x: M + (cardW + 0.15) * 2 + 0.15, y: 2.05, w: cardW - 0.3, h: cardH - 1.15, fontSize: 9.8, lineSpacingMultiple: 1.22, shrinkText: true, margin: [2, 4, 2, 4] });
}

// =========================================================================
// SLIDE 8: FEATURE ENGINEERING & CODE VARIABLES
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kỹ thuật Đặc trưng: 14 Thuộc tính Miền Cốt lõi', 8, TOTAL_PAGES);

  // Left: 3 Math Cards
  const leftW = 4.65;
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 1.08, w: leftW, h: 1.18, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addText('1. Sai lệch Số dư Nguồn (Delta Orig)', { x: M + 0.15, y: 1.14, w: leftW - 0.3, h: 0.22, fontSize: 10, bold: true, color: C.navyTitle });
  s.addText('errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig', { x: M + 0.15, y: 1.38, w: leftW - 0.3, h: 0.28, fontSize: 8.8, fontFace: F.fontCode, bold: true, color: C.blueAccent });
  s.addText('Đo lường sai lệch giữa số dư kỳ vọng và số dư thực tế tài khoản nguồn.', { x: M + 0.15, y: 1.68, w: leftW - 0.3, h: 0.50, fontSize: 8.8, color: C.textDark, lineSpacingMultiple: 1.2 });

  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 2.36, w: leftW, h: 1.18, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addText('2. Sai lệch Số dư Đích (Delta Dest)', { x: M + 0.15, y: 2.42, w: leftW - 0.3, h: 0.22, fontSize: 10, bold: true, color: C.navyTitle });
  s.addText('errorBalanceDest = oldbalanceDest + amount - newbalanceDest', { x: M + 0.15, y: 2.66, w: leftW - 0.3, h: 0.28, fontSize: 8.8, fontFace: F.fontCode, bold: true, color: C.blueAccent });
  s.addText('Ghi nhận bất thường không ghi có hoặc luân chuyển tiền đa tầng tức thì.', { x: M + 0.15, y: 2.96, w: leftW - 0.3, h: 0.50, fontSize: 8.8, color: C.textDark, lineSpacingMultiple: 1.2 });

  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 3.64, w: leftW, h: 1.36, fill: { color: C.redBox }, line: { color: C.redBorder } });
  s.addText('3. Cờ Vét sạch Tài khoản & Chu kỳ Giờ', { x: M + 0.15, y: 3.70, w: leftW - 0.3, h: 0.22, fontSize: 10, bold: true, color: C.dangerRed });
  s.addText('drain_flag = (oldbalanceOrg > 0) & (newbalanceOrig == 0)\nhour = step % 24   |   is_overnight = 1 if hour ∈ [0..5] else 0', { x: M + 0.15, y: 3.94, w: leftW - 0.3, h: 0.44, fontSize: 8.5, fontFace: F.fontCode, bold: true, color: C.navyTitle });
  s.addText('Bắt trọn hành vi vét sạch tài khoản trong 1 bước và tấn công tự động ban đêm.', { x: M + 0.15, y: 4.42, w: leftW - 0.3, h: 0.50, fontSize: 8.8, color: C.textDark, lineSpacingMultiple: 1.2 });

  // Right Side: Glossary Table & Key Insights
  const rightW = CW - leftW - 0.25;
  const rightX = M + leftW + 0.25;

  addVariableGlossaryTable(s, rightX, 1.08, rightW, [
    ['errorBalanceOrig', 'Sai lệch Nguồn', 'Độ chênh lệch giữa số dư tính toán và thực tế nguồn'],
    ['errorBalanceDest', 'Sai lệch Đích', 'Độ lệch ghi có tại tài khoản nhận tiền'],
    ['drain_flag', 'Cờ Vét sạch', '1 nếu số dư nguồn bị rút sạch về 0, ngược lại 0'],
    ['hour / overnight', 'Chu kỳ Giờ', 'Giờ trong ngày (0..23); 1 nếu giao dịch từ 0h - 5h sáng']
  ], '📋 Bảng chú giải biến & ký hiệu', [rightW * 0.42, rightW * 0.25, rightW * 0.33]);

  addHighlightBlock(s, {
    x: rightX, y: 2.95, w: rightW, h: 2.05,
    title: 'Đúc kết Feature Importance',
    bullets: [
      'Hai biến errorBalanceOrig (49.9%) và newbalanceOrig (47.2%) chiếm 97.1% tổng Feature Split Gains (XGBoost).',
      'XGBoost dựa gần như hoàn toàn vào nhóm số dư (98.5%); nhóm ghi nhận rủi ro simulator artifact (Mục 3.6.2).',
      'Nguyên tắc Chống Rò rỉ: Toàn bộ 14 đặc trưng (7 dẫn xuất) được chuẩn hóa StandardScaler CHỈ trên tập Train.'
    ],
    type: 'blue',
    fontSize: 9.0
  });
}

// =========================================================================
// SLIDE 9: CLASS IMBALANCE MITIGATION (SMOTE vs ADASYN)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Xử lý Mất cân bằng Lớp: SMOTE vs. ADASYN', 9, TOTAL_PAGES);

  // Top Banner: Accuracy Paradox
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 1.08, w: CW, h: 0.72, fill: { color: C.redBox }, line: { color: C.redBorder } });
  s.addText('Accuracy Paradox trong Bài toán Phân lớp Mất cân bằng Cực đoan', { x: M + 0.15, y: 1.12, w: CW - 0.3, h: 0.20, fontSize: 10.5, bold: true, color: C.dangerRed });
  s.addText('Một mô hình ngây thơ luôn dự đoán 100% là "Hợp lệ" vẫn đạt Accuracy 99.87% nhưng bỏ sót 100% gian lận! Do đó, đánh giá mô hình phải dẫn dắt bởi Precision, Recall, F1-Score và PR-AUC (Precision-Recall AUC).', {
    x: M + 0.15, y: 1.34, w: CW - 0.3, h: 0.42, fontSize: 9.3, color: C.textDark, lineSpacingMultiple: 1.2
  });

  const colW = (CW - 0.25) / 2;

  // Left: SMOTE Box
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 1.90, w: colW, h: 3.10, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addText('Kỹ thuật Nội suy Mẫu SMOTE', { x: M + 0.15, y: 1.98, w: colW - 0.3, h: 0.24, fontSize: 11.5, bold: true, color: C.navyTitle });

  // Math Card inside SMOTE
  s.addShape(pptx.shapes.RECTANGLE, { x: M + 0.15, y: 2.26, w: colW - 0.3, h: 0.36, fill: { color: 'FFFFFF' }, line: { color: C.skyBorder } });
  s.addText('x_new = x_i + λ · (x_zi - x_i),    với  λ ∈ [0, 1]', { x: M + 0.2, y: 2.29, w: colW - 0.4, h: 0.30, fontSize: 9.2, fontFace: F.fontCode, bold: true, color: C.blueAccent });

  s.addText([
    { text: '• Cơ chế: ', options: { bold: true, color: C.navyTitle } },
    { text: 'Nội suy mẫu nhân tạo thiểu số dọc theo đoạn thẳng nối các láng giềng k-NN trong Latent Space.\n\n', options: { color: C.textDark } },
    { text: '• Ưu điểm: ', options: { bold: true, color: C.blueAccent } },
    { text: 'Tạo Decision Boundary rõ nét, phân tách tốt giữa Fraud và Legitimate.\n\n', options: { color: C.textDark } },
    { text: '• Kết quả Thực nghiệm: ', options: { bold: true, color: C.navyTitle } },
    { text: 'Đạt F1-Score cao nhất (99.73%), chỉ tạo đúng 1 False Positive trên 38,357 mẫu test.', options: { color: C.textDark } }
  ], { x: M + 0.15, y: 2.70, w: colW - 0.3, h: 2.22, fontSize: 9.2, lineSpacingMultiple: 1.2, shrinkText: true, margin: [2, 4, 2, 4] });

  // Right Top: Glossary Table
  addVariableGlossaryTable(s, M + colW + 0.25, 1.90, colW, [
    ['x_i', 'Mẫu Thiểu số', 'Vector đặc trưng giao dịch gian lận gốc'],
    ['x_zi', 'Láng giềng k-NN', 'Mẫu gian lận lân cận gần nhất được chọn'],
    ['λ ∈ [0, 1]', 'Hệ số Nội suy', 'Số thực ngẫu nhiên xác định vị trí sinh mẫu'],
    ['Γ_i = r_i / ∑ r_i', 'Trọng số ADASYN', 'Tỷ lệ sinh mẫu thích ứng theo mật độ vùng biên']
  ], '📋 Bảng chú giải biến & ký hiệu', [colW * 0.36, colW * 0.28, colW * 0.36]);

  // Right Bottom: ADASYN Mechanism Box
  s.addShape(pptx.shapes.RECTANGLE, { x: M + colW + 0.25, y: 3.65, w: colW, h: 1.35, fill: { color: C.lightGrayBg }, line: { color: 'CBD5E1' } });
  s.addText('Tái lấy mẫu Mật độ ADASYN vs. Đúc kết', { x: M + colW + 0.35, y: 3.70, w: colW - 0.2, h: 0.22, fontSize: 10, bold: true, color: C.navyTitle });
  s.addText([
    { text: '• ADASYN sinh mẫu tỷ lệ thuận theo mật độ vùng biên khó, tuy nhiên dễ over-synthesize ở vùng chồng lấn nhiễu gây tăng nhẹ False Alarm.\n', options: { color: C.textDark } },
    { text: '• Đúc kết: SMOTE ổn định và vượt trội hơn ADASYN trên cả Random Forest và XGBoost.', options: { bold: true, color: C.blueAccent } }
  ], { x: M + colW + 0.35, y: 3.94, w: colW - 0.2, h: 1.00, fontSize: 8.8, lineSpacingMultiple: 1.18, shrinkText: true, margin: [2, 4, 2, 4] });
}

// =========================================================================
// SLIDE 10: DIVIDER 03
// =========================================================================
{
  const s = pptx.addSlide();
  addSectionDivider(s, 'PHẦN 03', 'PHƯƠNG PHÁP ĐỀ XUẤT & KIẾN TRÚC PIPELINE', [
    'Kiến trúc Pipeline Toàn diện Chuẩn Leak-Free',
    'Mô hình Giám sát: Random Forest vs. XGBoost Classifier',
    'Mô hình Không giám sát: Deep Autoencoder (Manifold Reconstruction)'
  ]);
}

// =========================================================================
// SLIDE 11: END-TO-END PIPELINE ARCHITECTURE
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kiến trúc Pipeline Machine Learning Chuẩn Leak-Free', 11, TOTAL_PAGES);

  // 6 Pipeline Steps spanning the full 8.9" width
  const steps = [
    { num: '1', name: 'Filtering', desc: 'Lọc giữ lại\nTRANSFER &\nCASH_OUT', color: '60A5FA' },
    { num: '2', name: 'Feature Eng.', desc: 'Tính toán 14\nengineered\ndomain features', color: '3B82F6' },
    { num: '3', name: 'Stratified Split', desc: 'Phân chia chuẩn\n80% Train /\n20% Test', color: '2563EB' },
    { num: '4', name: 'Resampling', desc: 'SMOTE / ADASYN\nCHỈ áp dụng\ntrên tập Train', color: '1D4ED8' },
    { num: '5', name: 'Model Training', desc: 'Huấn luyện RF,\nXGB & Deep\nAutoencoder', color: '1E3A8A' },
    { num: '6', name: 'Evaluation', desc: 'Đánh giá độc lập\ntrên Test set\n(N=40,000)', color: '0F172A' }
  ];

  const cardW = 1.25;
  const gapW = (CW - 6 * cardW) / 5;
  const stepH = 1.70;

  steps.forEach((st, idx) => {
    const sx = M + idx * (cardW + gapW);

    // Card Container
    s.addShape(pptx.shapes.RECTANGLE, { x: sx, y: 1.08, w: cardW, h: stepH, fill: { color: C.skyBox }, line: { color: C.skyBorder } });

    // Top Step Badge
    s.addShape(pptx.shapes.RECTANGLE, { x: sx, y: 1.08, w: cardW, h: 0.34, fill: { color: st.color } });
    s.addText(`B.${st.num}: ${st.name}`, { x: sx, y: 1.08, w: cardW, h: 0.34, fontSize: 8.5, bold: true, color: 'FFFFFF', align: 'center' });

    // Step Body Text
    s.addText(st.desc, { x: sx + 0.04, y: 1.46, w: cardW - 0.08, h: stepH - 0.42, fontSize: 8.8, align: 'center', color: C.textDark, lineSpacingMultiple: 1.15, shrinkText: true });

    // Distinct Arrow Connector
    if (idx < 5) {
      const arrowX = sx + cardW;
      s.addText('➔', { x: arrowX, y: 1.62, w: gapW, h: 0.40, fontSize: 13, bold: true, color: C.blueAccent, align: 'center' });
    }
  });

  // Bottom Rules Box
  addHighlightBlock(s, {
    x: M, y: 2.98, w: CW, h: 2.02,
    title: 'Nguyên tắc Chống Rò rỉ Dữ liệu (Data Leakage)',
    bullets: [
      'Phân tách Tập Dữ liệu Tuyệt đối: Phân chia Stratified Train/Test (80/20) được thực hiện TRƯỚC BẤT KỲ bước resampling hay chuẩn hóa nào.',
      'Resampling Phân lập: SMOTE / ADASYN tuyệt đối CHỈ áp dụng trên tập huấn luyện (Train fold). Tập Test hoàn toàn giữ nguyên phân bố tự nhiên (0.13% fraud).',
      'Chuẩn hóa StandardScaler: Bộ biến đổi tỷ lệ chỉ được fit trên tập Train và transform mù trên tập Test, không rò rỉ bất kỳ thông tin trung bình/độ lệch chuẩn nào.',
      'Không tối ưu Hyperparameter trên Test Set: Toàn bộ quá trình chọn ngưỡng và tune tham số đều tuân thủ Cross-Validation nội bộ trên tập Train.'
    ],
    type: 'blue',
    fontSize: 9.3
  });
}

// =========================================================================
// SLIDE 12: SUPERVISED ARCHITECTURES (RF & XGBOOST)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Mô hình Giám sát: Random Forest vs. XGBoost Classifier', 12, TOTAL_PAGES);

  const colW = (CW - 0.25) / 2;

  // Left: Random Forest
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 1.08, w: colW, h: 3.92, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addShape(pptx.shapes.RECTANGLE, { x: M + 0.15, y: 1.18, w: colW - 0.3, h: 0.32, fill: { color: C.navyTitle } });
  s.addText('Mô hình 1: Random Forest Ensemble', { x: M + 0.15, y: 1.18, w: colW - 0.3, h: 0.32, fontSize: 10.5, bold: true, color: 'FFFFFF', align: 'center' });

  // Math Card RF
  s.addShape(pptx.shapes.RECTANGLE, { x: M + 0.15, y: 1.58, w: colW - 0.3, h: 0.36, fill: { color: 'FFFFFF' }, line: { color: C.skyBorder } });
  s.addText('Gini(D) = 1 - ∑ (p_i)²', { x: M + 0.2, y: 1.60, w: colW - 0.4, h: 0.30, fontSize: 9.5, fontFace: F.fontCode, bold: true, color: C.blueAccent });

  // Code Variable & Hyperparameter Badge
  s.addShape(pptx.shapes.RECTANGLE, { x: M + 0.15, y: 2.00, w: colW - 0.3, h: 0.42, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 0.5 } });
  s.addText('📋 Tham số: n_estimators = 200, max_depth = 20\n📋 Chú giải biến: p_i = Xác suất mẫu thuộc lớp i tại node D', {
    x: M + 0.2, y: 2.03, w: colW - 0.4, h: 0.36, fontSize: 8.2, fontFace: F.fontBody, color: C.navyTitle, lineSpacingMultiple: 1.15
  });

  s.addText([
    { text: '• Cơ chế: ', options: { bold: true, color: C.navyTitle } },
    { text: 'Tập hợp 200 cây quyết định độc lập (Bagging) với kỹ thuật lấy mẫu ngẫu nhiên không gian con đặc trưng (Random Subspace).\n\n', options: { color: C.textDark } },
    { text: '• Peak Precision: ', options: { bold: true, color: C.blueAccent } },
    { text: 'Chỉ sinh duy nhất 1 False Positive trên 38,357 giao dịch hợp lệ (Precision = 99.94%).\n\n', options: { color: C.textDark } },
    { text: '• Hạn chế: ', options: { bold: true, color: C.dangerRed } },
    { text: 'Thời gian huấn luyện lâu (~20 phút), chi phí tính toán cao khi dữ liệu phình to.', options: { color: C.textDark } }
  ], { x: M + 0.15, y: 2.50, w: colW - 0.3, h: 2.40, fontSize: 9.0, lineSpacingMultiple: 1.2, shrinkText: true, margin: [2, 4, 2, 4] });

  // Right: XGBoost
  s.addShape(pptx.shapes.RECTANGLE, { x: M + colW + 0.25, y: 1.08, w: colW, h: 3.92, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addShape(pptx.shapes.RECTANGLE, { x: M + colW + 0.4, y: 1.18, w: colW - 0.3, h: 0.32, fill: { color: '1D4ED8' } });
  s.addText('Mô hình 2: XGBoost Classifier (GBDT)', { x: M + colW + 0.4, y: 1.18, w: colW - 0.3, h: 0.32, fontSize: 10.5, bold: true, color: 'FFFFFF', align: 'center' });

  // Math Card XGBoost
  s.addShape(pptx.shapes.RECTANGLE, { x: M + colW + 0.4, y: 1.58, w: colW - 0.3, h: 0.36, fill: { color: 'FFFFFF' }, line: { color: C.skyBorder } });
  s.addText('Obj^(t) ≈ ∑ [ g_i · f_t + ½ h_i · f_t² ] + Ω(f_t)', { x: M + colW + 0.45, y: 1.60, w: colW - 0.4, h: 0.30, fontSize: 9.0, fontFace: F.fontCode, bold: true, color: C.blueAccent });

  // Code Variable & Regularization Badge
  s.addShape(pptx.shapes.RECTANGLE, { x: M + colW + 0.4, y: 2.00, w: colW - 0.3, h: 0.42, fill: { color: 'F1F5F9' }, line: { color: 'CBD5E1', width: 0.5 } });
  s.addText('📋 Phạt phức tạp: Ω(f_t) = γ · T + ½ λ · ∑ w_j²\n📋 Chú giải biến: g_i, h_i = Gradient & Hessian bậc 1, 2; T = Số node lá', {
    x: M + colW + 0.45, y: 2.03, w: colW - 0.4, h: 0.36, fontSize: 8.0, fontFace: F.fontBody, color: C.navyTitle, lineSpacingMultiple: 1.15
  });

  s.addText([
    { text: '• Cơ chế: ', options: { bold: true, color: C.navyTitle } },
    { text: 'Gradient Boosting cải tiến với gradient bậc 1 (g_i) và Hessian bậc 2 (h_i), bổ sung L2 regularization chống Overfitting.\n\n', options: { color: C.textDark } },
    { text: '• Ưu thế Vượt trội: ', options: { bold: true, color: C.blueAccent } },
    { text: 'F1-Score đạt 99.63% tương đương RF, nhưng tốc độ huấn luyện nhanh gấp khoảng 28 lần (~42s).\n\n', options: { color: C.textDark } },
    { text: '• Production Ready: ', options: { bold: true, color: C.navyTitle } },
    { text: 'Độ trễ suy luận < 0.5ms, lý tưởng cho cổng thanh toán real-time.', options: { color: C.textDark } }
  ], { x: M + colW + 0.4, y: 2.50, w: colW - 0.3, h: 2.40, fontSize: 9.0, lineSpacingMultiple: 1.2, shrinkText: true, margin: [2, 4, 2, 4] });
}

// =========================================================================
// SLIDE 13: UNSUPERVISED ARCHITECTURE (DEEP AUTOENCODER)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Mô hình Không giám sát: Deep Autoencoder', 13, TOTAL_PAGES);

  const leftW = 4.8;
  // Left: 3-Phase Presentation Story
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: 1.08, w: leftW, h: 3.92, fill: { color: C.lightGrayBg }, line: { color: 'CBD5E1' } });
  s.addText('Cấu trúc & Nguyên lý Phát hiện Bất thường (3 Giai đoạn)', { x: M + 0.15, y: 1.15, w: leftW - 0.3, h: 0.24, fontSize: 10.5, bold: true, color: C.navyTitle });

  // Architecture Card
  s.addShape(pptx.shapes.RECTANGLE, { x: M + 0.15, y: 1.42, w: leftW - 0.3, h: 0.32, fill: { color: 'FFFFFF' }, line: { color: 'CBD5E1' } });
  s.addText('14(Input) → 16(Dense) → 8(Dense) → 4(Bottleneck) → 8(Dense) → 16(Dense) → 14(Output)', {
    x: M + 0.2, y: 1.45, w: leftW - 0.4, h: 0.26, fontSize: 8.5, fontFace: F.fontCode, bold: true, color: C.blueAccent
  });

  // Formula Card
  s.addShape(pptx.shapes.RECTANGLE, { x: M + 0.15, y: 1.80, w: leftW - 0.3, h: 0.34, fill: { color: 'FFFFFF' }, line: { color: C.redBorder } });
  s.addText('L_rec(x, x_recon) = (1 / d) · ∑ (x_j - x_recon_j)²', { x: M + 0.2, y: 1.83, w: leftW - 0.4, h: 0.28, fontSize: 9.0, fontFace: F.fontCode, bold: true, color: C.dangerRed });

  s.addText([
    { text: '1. Giai đoạn Học Chuẩn (Normal Manifold):\n', options: { bold: true, color: C.navyTitle } },
    { text: '• Mạng chỉ huấn luyện trên giao dịch HỢP LỆ, học cách nén và tái tạo cấu trúc luồng tiền bình thường.\n\n', options: { color: C.textDark } },
    { text: '2. Giai đoạn Bắt Lỗi (Anomaly Spike):\n', options: { bold: true, color: C.dangerRed } },
    { text: '• Khi gặp giao dịch gian lận bất thường, mạng không thể tái tạo chính xác → Sai số MSE tăng vọt.\n\n', options: { color: C.textDark } },
    { text: '3. Giai đoạn Ra Quyết định (Thresholding):\n', options: { bold: true, color: C.blueAccent } },
    { text: '• Gán cờ Gian lận nếu L_rec(x, x_recon) > τ (ngưỡng phân vị 95th: τ = 0.0455).', options: { color: C.textDark } }
  ], { x: M + 0.15, y: 2.22, w: leftW - 0.3, h: 2.70, fontSize: 9.0, lineSpacingMultiple: 1.18, shrinkText: true, margin: [2, 4, 2, 4] });

  // Right Side: Unified Notation Glossary & Zero-Day Role
  const rightW = CW - leftW - 0.25;
  const rightX = M + leftW + 0.25;

  addVariableGlossaryTable(s, rightX, 1.08, rightW, [
    ['x', 'Vector Đầu vào', 'Vector đặc trưng giao dịch gốc (14 chiều)'],
    ['x_recon', 'Vector Tái tạo', 'Vector đầu ra tái tạo từ tầng giải mã'],
    ['d = 14', 'Số chiều Đặc trưng', 'Tổng số lượng thuộc tính đầu vào của mạng'],
    ['L_rec(x, x_recon)', 'Sai số Tái tạo', 'Hàm mất mát MSE đo mức độ dị biệt giao dịch'],
    ['τ = 0.0455', 'Ngưỡng Cutoff', 'Điểm cắt phân vị 95th để kích hoạt cảnh báo']
  ], '📋 Bảng chú giải biến & ký hiệu đồng nhất', [rightW * 0.35, rightW * 0.30, rightW * 0.35]);

  addHighlightBlock(s, {
    x: rightX, y: 3.08, w: rightW, h: 1.92,
    title: 'Phát hiện Bất thường Không giám sát (Unsupervised)',
    bullets: [
      'Autoencoder đạt 75.23% Recall trên Test dù không dùng nhãn gian lận khi huấn luyện mạng.',
      'Không phụ thuộc nhãn: Phát hiện bất thường theo nguyên lý sai số tái tạo (Reconstruction MSE).',
      'Lớp Phòng thủ Thứ cấp (Defense-in-Depth): Đóng vai trò lưới lọc an toàn chuyển giao dịch nghi vấn sang kiểm tra chuyên sâu.'
    ],
    type: 'blue',
    fontSize: 8.8
  });
}

// =========================================================================
// SLIDE 14: DIVIDER 04
// =========================================================================
{
  const s = pptx.addSlide();
  addSectionDivider(s, 'PHẦN 04', 'KẾT QUẢ THỰC NGHIỆM & ĐÁNH GIÁ SO SÁNH', [
    'Benchmark Hiệu năng Toàn diện & Bảng so sánh đa chỉ số (Precision, Recall, F1, PR-AUC)',
    'Phân tích Ma trận Nhầm lẫn (Confusion Matrix) & Đánh đổi False Alarm vs. Missed Fraud',
    'Feature Importance Attribution & Phân tích Đóng góp Nhóm Đặc trưng Số dư',
    'Phân bố Sai số Tái tạo & Ngưỡng Anomaly Thresholding (Deep Autoencoder)'
  ]);
}

// =========================================================================
// SLIDE 15: EXPERIMENTAL BENCHMARK & METRICS COMPARISON CHART
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Kết quả Thực nghiệm: So sánh đa chỉ số', 15, TOTAL_PAGES);

  const leftW = 4.45;
  const rightX = M + leftW + 0.20;
  const rightW = CW - leftW - 0.20;

  // Left Side: Benchmark Table
  const benchTable = [
    [
      { text: 'Mô hình', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Resampling', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Prec.', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Recall', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'F1', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Time', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } }
    ],
    [{ text: 'Random Forest', options: { bold: true } }, { text: 'SMOTE' }, { text: '99.94%', options: { bold: true, color: C.blueAccent } }, { text: '99.51%', options: { bold: true, color: C.blueAccent } }, { text: '99.73%', options: { bold: true, color: C.blueAccent } }, { text: '1187s' }],
    [{ text: 'Random Forest', options: { bold: true } }, { text: 'ADASYN' }, { text: '99.82%' }, { text: '99.51%' }, { text: '99.66%' }, { text: '1168s' }],
    [{ text: 'XGBoost', options: { bold: true, color: C.navyTitle } }, { text: 'SMOTE' }, { text: '99.76%' }, { text: '99.51%' }, { text: '99.63%', options: { bold: true } }, { text: '41.7s', options: { bold: true, color: C.blueAccent } }],
    [{ text: 'XGBoost', options: { bold: true } }, { text: 'ADASYN' }, { text: '99.57%' }, { text: '99.51%' }, { text: '99.54%' }, { text: '43.2s' }],
    [{ text: 'Autoencoder (Zero-Day)', options: { bold: true, color: C.dangerRed } }, { text: 'None (Unsup.)' }, { text: '38.22%' }, { text: '75.23%', options: { bold: true, color: C.dangerRed } }, { text: '50.69%' }, { text: '68.4s' }]
  ];

  slideTable(s, benchTable, M, 1.08, leftW, [leftW * 0.32, leftW * 0.20, leftW * 0.12, leftW * 0.12, leftW * 0.12, leftW * 0.12], 8.2);

  // Left Bottom: Quantitative Findings Box
  addHighlightBlock(s, {
    x: M, y: 3.12, w: leftW, h: 1.88,
    title: 'Đúc kết bảng so sánh',
    bullets: [
      'Random Forest + SMOTE đạt F1-Score đỉnh cao 99.73% nhờ cơ chế Bagging triệt tiêu phương sai.',
      'XGBoost + SMOTE đạt hiệu năng tương đương (F1 = 99.63%) nhưng tốc độ huấn luyện nhanh gấp 28.5 lần.',
      'Autoencoder bắt được 75.23% gian lận hoàn toàn không cần nhãn giám sát, tạo lớp phòng thủ Zero-Day vững chắc.'
    ],
    type: 'blue',
    fontSize: 8.6
  });

  // Right Side: Metrics Comparison Chart
  const chartImgPath = path.join(__dirname, 'slide_assets', 'academic_metrics_comparison.png');
  const chartH = rightW / 2.118; // Natural aspect ratio 2220x1048
  if (fs.existsSync(chartImgPath)) {
    s.addImage({
      path: chartImgPath,
      x: rightX, y: 1.08, w: rightW, h: chartH
    });
  }

  // Right Bottom: Comparison Insights
  addHighlightBlock(s, {
    x: rightX, y: 1.08 + chartH + 0.10, w: rightW, h: 3.92 - chartH - 0.10,
    title: 'Phân tích Biểu đồ',
    bullets: [
      'Cột Precision & Recall của RF và XGBoost vượt trội trên 99.5%, khẳng định tính khả thi triển khai thực tế.',
      'Autoencoder hy sinh Precision (38.2%) để duy trì Recall cao (75.2%) nhằm phòng ngừa triệt để tổn thất tài chính.'
    ],
    type: 'blue',
    fontSize: 8.4
  });
}

// =========================================================================
// SLIDE 16: CONFUSION MATRICES & ERROR TRADE-OFFS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Phân tích Ma trận Nhầm lẫn & Đánh đổi Sai số', 16, TOTAL_PAGES);

  // Top: Wide Confusion Matrices Chart
  const cmImgPath = path.join(__dirname, 'slide_assets', 'academic_confusion_matrices.png');
  const imgW = CW;
  const imgH = imgW / 3.457; // Natural aspect ratio 3419x989 (~2.57")
  const actualImgH = 2.40;
  const actualImgW = actualImgH * 3.457;
  const imgX = M + (CW - actualImgW) / 2;

  if (fs.existsSync(cmImgPath)) {
    s.addImage({
      path: cmImgPath,
      x: imgX, y: 1.06, w: actualImgW, h: actualImgH
    });
  }

  // Bottom: 3 Detailed Insight Cards (RF, XGBoost, Autoencoder)
  const cardW = (CW - 0.3) / 3;
  const cardY = 1.06 + actualImgH + 0.12; // 3.58
  const cardH = SH - cardY - 0.45; // ~1.595"

  // Card 1: Random Forest
  s.addShape(pptx.shapes.RECTANGLE, { x: M, y: cardY, w: cardW, h: cardH, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addText('Random Forest + SMOTE', { x: M + 0.1, y: cardY + 0.08, w: cardW - 0.2, h: 0.20, fontSize: 9.5, bold: true, color: C.navyTitle });
  s.addText('TP: 1,635  •  FP: 1\nFN: 8  •  TN: 38,356', { x: M + 0.1, y: cardY + 0.28, w: cardW - 0.2, h: 0.38, fontSize: 8.5, fontFace: F.fontCode, bold: true, color: C.blueAccent });
  s.addText('• Tỷ lệ False Alarm thấp kỷ lục (chỉ 1 ca trên 38,357 mẫu test).\n• Precision đạt 99.94%, gần như triệt tiêu hoàn toàn báo động giả.', {
    x: M + 0.1, y: cardY + 0.68, w: cardW - 0.2, h: cardH - 0.72, fontSize: 8.2, color: C.textDark, lineSpacingMultiple: 1.15, shrinkText: true, margin: [2, 4, 2, 4]
  });

  // Card 2: XGBoost
  s.addShape(pptx.shapes.RECTANGLE, { x: M + cardW + 0.15, y: cardY, w: cardW, h: cardH, fill: { color: C.skyBox }, line: { color: C.skyBorder } });
  s.addText('XGBoost + SMOTE (Sản xuất)', { x: M + cardW + 0.25, y: cardY + 0.08, w: cardW - 0.2, h: 0.20, fontSize: 9.5, bold: true, color: C.navyTitle });
  s.addText('TP: 1,635  •  FP: 4\nFN: 8  •  TN: 38,353', { x: M + cardW + 0.25, y: cardY + 0.28, w: cardW - 0.2, h: 0.38, fontSize: 8.5, fontFace: F.fontCode, bold: true, color: C.blueAccent });
  s.addText('• Chỉ 4 ca cảnh báo nhầm, đồng thời bắt trúng 1,635 ca gian lận.\n• Độ trễ suy luận < 0.5ms — cấu hình tối ưu nhất cho môi trường thực tế.', {
    x: M + cardW + 0.25, y: cardY + 0.68, w: cardW - 0.2, h: cardH - 0.72, fontSize: 8.2, color: C.textDark, lineSpacingMultiple: 1.15, shrinkText: true, margin: [2, 4, 2, 4]
  });

  // Card 3: Deep Autoencoder
  s.addShape(pptx.shapes.RECTANGLE, { x: M + (cardW + 0.15) * 2, y: cardY, w: cardW, h: cardH, fill: { color: C.redBox }, line: { color: C.redBorder } });
  s.addText('Deep Autoencoder (Zero-Day)', { x: M + (cardW + 0.15) * 2 + 0.1, y: cardY + 0.08, w: cardW - 0.2, h: 0.20, fontSize: 9.5, bold: true, color: C.dangerRed });
  s.addText('TP: 1,236  •  FP: 1,998\nFN: 407  •  TN: 36,359', { x: M + (cardW + 0.15) * 2 + 0.1, y: cardY + 0.28, w: cardW - 0.2, h: 0.38, fontSize: 8.5, fontFace: F.fontCode, bold: true, color: C.dangerRed });
  s.addText('• Bắt 1,236 ca gian lận trong điều kiện học không giám sát.\n• Đóng vai trò màng lọc an toàn thứ cấp cho các mẫu tấn công phi quy ước.', {
    x: M + (cardW + 0.15) * 2 + 0.1, y: cardY + 0.68, w: cardW - 0.2, h: cardH - 0.72, fontSize: 8.2, color: C.textDark, lineSpacingMultiple: 1.15, shrinkText: true, margin: [2, 4, 2, 4]
  });
}

// =========================================================================
// SLIDE 17: FEATURE IMPORTANCE & DOMAIN GAINS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Phân tích Đóng góp Đặc trưng (Feature Importance)', 17, TOTAL_PAGES);

  const leftW = 4.45;
  const rightX = M + leftW + 0.20;
  const rightW = CW - leftW - 0.20;

  // Left Side: Feature Importance Chart
  const fiImgPath = path.join(__dirname, 'slide_assets', 'academic_feature_importance.png');
  const chartH = leftW / 1.838; // 1926x1048 -> ~2.42"
  if (fs.existsSync(fiImgPath)) {
    s.addImage({
      path: fiImgPath,
      x: M, y: 1.08, w: leftW, h: chartH
    });
  }

  // Left Bottom: Engineering Insight Box
  addHighlightBlock(s, {
    x: M, y: 1.08 + chartH + 0.10, w: leftW, h: 3.92 - chartH - 0.10,
    title: 'Ý nghĩa Kỹ thuật Đặc trưng (Feature Engineering)',
    bullets: [
      'Top 2 đặc trưng (errorBalanceOrig dẫn xuất & newbalanceOrig gốc nguồn) chiếm 97.1% Split Gains.',
      'Mô hình cây dựa chủ yếu vào sai lệch cân bằng kế toán để phân định gian lận thay vì chỉ học giá trị số tiền gốc.'
    ],
    type: 'blue',
    fontSize: 8.4
  });

  // Right Side: Split Gain Table
  const fiTable = [
    [
      { text: 'Đặc trưng', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Split Gain', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Ý nghĩa Phân loại Nghiệp vụ', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } }
    ],
    [{ text: 'errorBalanceOrig', options: { bold: true, fontFace: F.fontCode } }, { text: '49.9%', options: { bold: true, color: C.blueAccent } }, { text: 'Sai lệch số dư tài khoản nguồn' }],
    [{ text: 'newbalanceOrig', options: { bold: true, fontFace: F.fontCode } }, { text: '47.2%', options: { bold: true, color: C.blueAccent } }, { text: 'Số dư nguồn về 0 (rút cạn tài khoản)' }],
    [{ text: 'amount', options: { bold: true, fontFace: F.fontCode } }, { text: '0.5%' }, { text: 'Giá trị giao dịch bất thường' }],
    [{ text: 'hour / overnight', options: { bold: true, fontFace: F.fontCode } }, { text: '0.03%' }, { text: 'Khung giờ tấn công đêm (0h - 5h)' }],
    [{ text: '9 features còn lại', options: { bold: true } }, { text: '2.4%' }, { text: 'Các thuộc tính phụ trợ' }]
  ];
  slideTable(s, fiTable, rightX, 1.08, rightW, [rightW * 0.38, rightW * 0.22, rightW * 0.40], 8.2);

  // Right Bottom: Deep Dive Highlight
  addHighlightBlock(s, {
    x: rightX, y: 3.05, w: rightW, h: 1.95,
    title: 'Đúc kết Bản chất Bài toán Gian lận',
    bullets: [
      'errorBalanceOrig = 49.9%: Khi kẻ gian thực hiện lệnh chuyển/rút tiền, số dư sổ cái bị trừ vượt mức số tiền thực tế có trong tài khoản.',
      'newbalanceOrig = 47.2%: 97.55% các ca gian lận rút cạn số dư nguồn về 0 nhằm tẩu tán tối đa tài sản.',
      'Đặc trưng số dư: Nhóm số dư chiếm 98.5% Split Gains; nhóm ghi nhận đây là thế mạnh trên PaySim nhưng cũng là nguy cơ rủi ro dữ liệu mô phỏng (Mục 3.6.2).'
    ],
    type: 'blue',
    fontSize: 8.3
  });
}

// =========================================================================
// SLIDE 18: AUTOENCODER ANOMALY DISTRIBUTION & THRESHOLDING
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Phân bố Sai số Tái tạo & Ngưỡng Anomaly', 18, TOTAL_PAGES);

  const leftW = 4.45;
  const rightX = M + leftW + 0.20;
  const rightW = CW - leftW - 0.20;

  // Left Side: Reconstruction Error Distribution Chart
  const aeImgPath = path.join(__dirname, 'slide_assets', 'academic_autoencoder_dist.png');
  const chartH = leftW / 1.918; // 2010x1048 -> ~2.32"
  if (fs.existsSync(aeImgPath)) {
    s.addImage({
      path: aeImgPath,
      x: M, y: 1.08, w: leftW, h: chartH
    });
  }

  // Left Bottom: Threshold Theory Box
  addHighlightBlock(s, {
    x: M, y: 1.08 + chartH + 0.10, w: leftW, h: 3.92 - chartH - 0.10,
    title: 'Nguyên lý Phân tách Phân bố Sai số',
    bullets: [
      'Giao dịch hợp lệ (Xanh) tập trung ở vùng sai số MSE cực thấp (< 0.02).',
      'Giao dịch gian lận (Đỏ) có sai số tái tạo trải dài sang phải do cấu trúc dòng tiền dị biệt không thể nén qua bottleneck.'
    ],
    type: 'blue',
    fontSize: 8.3
  });

  // Right Side: Threshold Sweep Table
  const thTable = [
    [
      { text: 'Phân vị', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Ngưỡng τ', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Recall', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Precision', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } }
    ],
    [{ text: '90.0th %ile', options: { bold: true } }, { text: '0.0134' }, { text: '84.8%' }, { text: '26.6%' }],
    [{ text: '95.0th %ile (Chọn)', options: { bold: true, color: C.dangerRed } }, { text: '0.0455', options: { bold: true } }, { text: '73.5%', options: { bold: true, color: C.dangerRed } }, { text: '38.6%', options: { bold: true } }],
    [{ text: '99.0th %ile', options: { bold: true } }, { text: '0.1240' }, { text: '47.0%' }, { text: '66.8%' }],
    [{ text: '99.9th %ile', options: { bold: true } }, { text: '0.7460' }, { text: '25.4%' }, { text: '91.5%' }]
  ];
  slideTable(s, thTable, rightX, 1.08, rightW, [rightW * 0.28, rightW * 0.24, rightW * 0.24, rightW * 0.24], 8.2);

  // Right Bottom: Strategic Decision Highlight
  addHighlightBlock(s, {
    x: rightX, y: 2.85, w: rightW, h: 2.15,
    title: 'Quét ngưỡng trên Validation & Điểm cắt Chọn (τ = 0.0455)',
    bullets: [
      'Điểm cắt 95th (τ = 0.0455) đạt F1 cao nhất (0.5064) trong các ngưỡng thỏa Recall ≥ 60%. Trên Test độc lập đạt Recall 75.2%, Precision 38.2%.',
      'Chiến lược Defense-in-Depth: Đóng vai trò lớp phòng thủ thứ cấp phát hiện giao dịch dị biệt chuyển sang thẩm định chuyên sâu.',
      'Không cần nhãn gian lận: Mạng nơ-ron huấn luyện hoàn toàn trên luồng tiền hợp lệ (nhãn chỉ dùng ở bước quét ngưỡng).'
    ],
    type: 'blue',
    fontSize: 8.3
  });
}

// =========================================================================
// SLIDE 19: DIVIDER 05
// =========================================================================
{
  const s = pptx.addSlide();
  addSectionDivider(s, 'PHẦN 05', 'HỆ THỐNG DEMO & ĐỊNH HƯỚNG TƯƠNG LAI', [
    'Kiến trúc Dashboard Streamlit Real-Time Inference & Batch CSV Scoring',
    'Tổng kết Đóng góp Học thuật & Quy chuẩn Kỹ thuật Cốt lõi',
    'Hạn chế Nghiên cứu & Lộ trình Mở rộng Graph Neural Networks (GNN)'
  ]);
}

// =========================================================================
// SLIDE 20: TRUE 16:9 VIDEO DEMO & EXPANDED DASHBOARD SHOWCASE
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Hệ thống Demo Streamlit & Hướng phát triển', 20, TOTAL_PAGES);

  // Left: Outer Video Player Device Frame
  const leftW = 5.50;
  const leftH = 3.92;

  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: M, y: 1.08, w: leftW, h: leftH,
    fill: { color: C.videoDarkBg },
    line: { color: C.videoBorder, width: 1.5 },
    rectRadius: 0.12
  });

  // Top Status Bar of Player
  s.addShape(pptx.shapes.RECTANGLE, {
    x: M, y: 1.08, w: leftW, h: 0.30,
    fill: { color: '1E293B' },
    line: { type: 'none' }
  });
  s.addText('🔴 LIVE DEMO  •  Streamlit Real-Time Fraud Shield  |  XGBoost-SMOTE & Autoencoder', {
    x: M + 0.15, y: 1.08, w: leftW - 0.3, h: 0.30,
    fontSize: 8.8, fontFace: F.fontCode, color: '60A5FA', bold: true
  });

  // TRUE 16:9 SCREEN BOX (Width: 5.12", Height: 2.88" -> Exact 16:9 Ratio!)
  const screenW = 5.12;
  const screenH = 2.88; // 5.12 * 9 / 16 = 2.88
  const screenX = M + (leftW - screenW) / 2;
  const screenY = 1.45;

  s.addShape(pptx.shapes.RECTANGLE, {
    x: screenX, y: screenY, w: screenW, h: screenH,
    fill: { color: '0B1120' },
    line: { color: '38BDF8', width: 1.5 }
  });

  // Center Play Icon & 16:9 Watermark inside Video Screen
  s.addText('▶', {
    x: screenX, y: screenY + 0.35, w: screenW, h: 0.65,
    fontSize: 36, color: '38BDF8', align: 'center', bold: true
  });
  s.addText('[ KHUNG CHÈN VIDEO DEMO STREAMLIT ]\n(Tỷ lệ Chuẩn 16:9 — 1920×1080 / 1280×720 MP4/GIF)', {
    x: screenX + 0.15, y: screenY + 1.05, w: screenW - 0.3, h: 0.55,
    fontSize: 10, fontFace: 'Segoe UI', color: 'E2E8F0', align: 'center', bold: true, lineSpacingMultiple: 1.2
  });
  s.addText('Giao diện phân tích rủi ro thời gian thực & Chấm điểm Batch CSV', {
    x: screenX + 0.15, y: screenY + 1.68, w: screenW - 0.3, h: 0.25,
    fontSize: 8.5, fontFace: 'Segoe UI', color: '94A3B8', align: 'center', italic: true
  });

  // Bottom 16:9 Aspect Ratio Pill Badge
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: screenX + (screenW - 2.2) / 2, y: screenY + 2.15, w: 2.2, h: 0.32,
    fill: { color: '1E293B' },
    line: { color: '64748B', width: 0.8 },
    rectRadius: 0.08
  });
  s.addText('HD 1080p  •  TỶ LỆ 16:9', {
    x: screenX + (screenW - 2.2) / 2, y: screenY + 2.15, w: 2.2, h: 0.32,
    fontSize: 8.2, fontFace: F.fontCode, color: '38BDF8', align: 'center', bold: true
  });

  // Bottom Ticker Bar inside Video Frame
  s.addShape(pptx.shapes.RECTANGLE, {
    x: M + 0.15, y: 4.40, w: leftW - 0.3, h: 0.50,
    fill: { color: '131C31' },
    line: { color: '1E293B', width: 1 }
  });
  s.addText('3 Kịch bản: 1. Hợp lệ (< 0.1%)  |  2. Vét cạn số dư (88.36%)  |  3. Cận biên ban đêm (~32%)', {
    x: M + 0.20, y: 4.40, w: leftW - 0.4, h: 0.50,
    fontSize: 7.8, fontFace: F.fontCode, color: 'CBD5E1', align: 'center'
  });

  // Right Side: Contributions & Roadmap
  const rightW = CW - leftW - 0.25;
  const rightX = M + leftW + 0.25;

  addHighlightBlock(s, {
    x: rightX, y: 1.08, w: rightW, h: 1.90,
    title: 'Tổng kết Đóng góp Cốt lõi',
    bullets: [
      'Quy chuẩn Leak-Free: 80/20 Stratified Split chống rò rỉ dữ liệu.',
      'Đặc trưng Số dư: Nhóm số dư chiếm > 97% split gains (ghi nhận rủi ro simulator artifact).',
      'Benchmark: F1 = 99.73%, Recall = 99.51% (Random Forest SMOTENC, 8 ca bỏ sót).',
      'Phòng thủ Đa tầng: Phối hợp XGBoost phát hiện nhanh và Autoencoder bắt bất thường.'
    ],
    type: 'blue',
    fontSize: 8.4
  });

  addHighlightBlock(s, {
    x: rightX, y: 3.10, w: rightW, h: 1.90,
    title: 'Hướng phát triển',
    bullets: [
      'Graph Neural Networks (GNN): GraphSAGE phát hiện rửa tiền đa tầng.',
      'Xử lý Phân tán (Kafka/Flink): Streaming hàng triệu sự kiện/giây.',
      'Explainable AI (XAI): SHAP giải thích quyết định chặn giao dịch.'
    ],
    type: 'blue',
    fontSize: 8.4
  });
}

// =========================================================================
// SLIDE 21: CONCLUSION & REFERENCES (Q&A)
// =========================================================================
{
  const s = pptx.addSlide();
  s.background = { color: C.navyBg };

  s.addText('CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN\nĐÃ LẮNG NGHE BÁO CÁO!', {
    x: M, y: 0.70, w: CW, h: 0.68,
    fontSize: 22, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true, lineSpacingMultiple: 1.25
  });

  s.addText('CS106: TRÍ TUỆ NHÂN TẠO  •  BÁO CÁO BẢO VỆ ĐỒ ÁN  •  NHÓM 09', {
    x: M, y: 1.45, w: CW, h: 0.28,
    fontSize: 11.5, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  // Center Content Box
  s.addShape(pptx.shapes.RECTANGLE, {
    x: M + 0.5, y: 1.88, w: CW - 1.0, h: 2.92,
    fill: { color: '172048' },
    line: { color: '3B82F6', width: 1.5 }
  });

  s.addText('TÀI LIỆU THAM KHẢO HỌC THUẬT & REPOSITORY DỰ ÁN', {
    x: M + 0.5, y: 2.00, w: CW - 1.0, h: 0.28,
    fontSize: 12, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText([
    { text: '• Mã nguồn Dự án (Gói nộp bài & GitHub Repo): ', options: { bold: true, color: '60A5FA' } },
    { text: 'https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection\n', options: { color: '38BDF8', bold: true } },
    { text: '• PaySim Simulator: ', options: { bold: true, color: '60A5FA' } },
    { text: 'E. A. Lopez-Rojas, A. Elmir, and S. Axelsson, "PaySim: A financial mobile money simulator for fraud detection," in Proc. 28th Eur. Model. Simul. Symp., 2016, pp. 249-255.\n', options: { color: 'E2E8F0' } },
    { text: '• XGBoost GBDT: ', options: { bold: true, color: '60A5FA' } },
    { text: 'T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in Proc. 22nd ACM SIGKDD, 2016, pp. 785-794.\n', options: { color: 'E2E8F0' } },
    { text: '• SMOTE Resampling: ', options: { bold: true, color: '60A5FA' } },
    { text: 'N. V. Chawla et al., "SMOTE: Synthetic minority over-sampling technique," J. Artif. Intell. Res., vol. 16, pp. 321-357, 2002.\n\n', options: { color: 'E2E8F0' } },
    { text: 'Nhóm 09 rất mong nhận được những câu hỏi và góp ý quý báu từ Thầy và các bạn!', options: { italic: true, color: 'FCD34D' } }
  ], {
    x: M + 0.75, y: 2.36, w: CW - 1.5, h: 2.35,
    fontSize: 9.3, fontFace: F.fontBody, align: 'left', lineSpacingMultiple: 1.25, shrinkText: true, margin: [2, 4, 2, 4]
  });
}

// -------------------------------------------------------------
// Write Presentation File
// -------------------------------------------------------------
const outputFile = path.join(__dirname, '[Nhom9]_Slide_FraudDetection_Academic_VN.pptx');
pptx.writeFile({ fileName: outputFile })
  .then(() => {
    console.log(`Successfully generated ${TOTAL_PAGES}-slide PPTX: ` + outputFile);
  })
  .catch(err => {
    console.error('Error generating PPTX:', err);
    process.exit(1);
  });
