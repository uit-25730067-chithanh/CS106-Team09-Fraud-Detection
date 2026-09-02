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
  slideTitle: 22,
  subTitle: 15,
  body: 12.5,
  bodyBold: 12.5,
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
  slide.addText('UNIVERSITY OF INFORMATION TECHNOLOGY, VNUHCM', {
    x: M, y: 0.22, w: CW, h: 0.22,
    fontSize: 8.5, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  // Slide Title (Left Aligned, Montserrat, Navy)
  slide.addText(title, {
    x: M, y: 0.55, w: CW, h: 0.45,
    fontSize: F.slideTitle, fontFace: F.fontTitle, color: C.navyTitle, bold: true
  });

  // Bottom Footer
  slide.addText('CS106 — Team 09 — Financial Fraud Detection on PaySim', {
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

  let curY = y + 0.12;
  if (title) {
    slide.addText(title, {
      x: x + 0.2, y: curY, w: w - 0.4, h: 0.28,
      fontSize: 12, fontFace: F.fontTitle, color: isBlue ? C.navyTitle : C.dangerRed, bold: true
    });
    curY += 0.3;
  }

  if (text) {
    slide.addText(text, {
      x: x + 0.2, y: curY, w: w - 0.4, h: h - (curY - y) - 0.1,
      fontSize: F.body, fontFace: F.fontBody, color: C.textDark, shrinkText: true
    });
  } else if (bullets && bullets.length > 0) {
    const textArr = bullets.map((b, idx) => ({
      text: b,
      options: { bullet: true, breakLine: idx < bullets.length - 1, color: C.textDark, fontSize: F.body }
    }));
    slide.addText(textArr, {
      x: x + 0.2, y: curY, w: w - 0.4, h: h - (curY - y) - 0.1,
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

  s.addText('UNIVERSITY OF INFORMATION TECHNOLOGY, VNUHCM\nFACULTY OF COMPUTER SCIENCE', {
    x: M, y: 0.5, w: CW, h: 0.5,
    fontSize: 9.5, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  s.addText('FINANCIAL FRAUD DETECTION', {
    x: M, y: 1.45, w: CW, h: 0.75,
    fontSize: 34, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText('Applied Machine Learning & Deep Learning on PaySim Synthetic Dataset', {
    x: M, y: 2.25, w: CW, h: 0.4,
    fontSize: 15, fontFace: 'Georgia', color: '93C5FD', align: 'center', italic: true
  });

  s.addText('Instructor: Assoc. Prof. Nguyen Dinh Hien', {
    x: M, y: 3.0, w: CW, h: 0.35,
    fontSize: 13, fontFace: F.fontBody, color: 'FFFFFF', align: 'center'
  });

  s.addShape(pptx.shapes.LINE, {
    x: M + 2.8, y: 3.48, w: 1.2, h: 0,
    line: { color: '93C5FD', width: 2 }
  });
  s.addText('Team 09', {
    x: M + 4.1, y: 3.38, w: 0.9, h: 0.25,
    fontSize: 12.5, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });
  s.addShape(pptx.shapes.LINE, {
    x: M + 5.1, y: 3.48, w: 1.2, h: 0,
    line: { color: '93C5FD', width: 2 }
  });

  s.addText('Tran Hoang Hon  ·  Dang Chi Thanh  ·  Nguyen Duy Khang  ·  Hoang Cao Son  ·  Vu Van Duy  ·  Bui Thi My Cam  ·  Pham Thanh Trung', {
    x: M, y: 3.85, w: CW, h: 0.35,
    fontSize: 10, fontFace: F.fontBody, color: 'CBD5E1', align: 'center'
  });
}

// =========================================================================
// SLIDE 2: AGENDA (CS115 Minimalist Number Grid)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'AGENDA', 2);

  const agenda = [
    { num: '01', title: 'Introduction & Problem Formulation', color: '60A5FA' },
    { num: '02', title: 'Exploratory Data Analysis & Feature Engineering', color: '3B82F6' },
    { num: '03', title: 'Proposed Methodologies & Pipeline', color: '2563EB' },
    { num: '04', title: 'Experiments, Results & Error Analysis', color: '1D4ED8' },
    { num: '05', title: 'Interactive Demo & Future Directions', color: '1E3A8A' }
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
      fontSize: 16, fontFace: F.fontTitle, color: C.navyTitle, bold: true
    });
  });
}

// =========================================================================
// SLIDE 3: PROBLEM MOTIVATION & TECHNICAL CHALLENGES
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Problem Motivation & Challenges', 3);

  // Left Content
  s.addText([
    { text: '1. Industrial Context\n', options: { bold: true, color: C.navyTitle, fontSize: 13.5 } },
    { text: '• Mobile money transactions have surged globally, introducing complex financial fraud vectors.\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Real-time defense mechanisms require low-latency response (< 100ms) before fund extraction.\n\n', options: { fontSize: 12, color: C.textDark } },
    
    { text: '2. Extreme Class Imbalance (~0.13%)\n', options: { bold: true, color: C.navyTitle, fontSize: 13.5 } },
    { text: '• Fraud accounts for only ~1 out of 800 transactions, causing standard classifiers to collapse.\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Cost Asymmetry: False Negatives (missed fraud) carry severe financial penalties vs False Positives.\n', options: { fontSize: 12, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 4.8, h: 3.8
  });

  // Right Notation Box
  addNotationTable(s, M + 5.1, 1.2, 3.8, [
    ['Class Target', 'Y', '1 = Fraudulent, 0 = Legitimate'],
    ['Imbalance', 'IR', '0.13% minority positive class'],
    ['Metric', 'Recall', 'Maximize coverage on true fraud'],
    ['Cost Ratio', 'C_FN / C_FP', 'Asymmetric loss penalty (>> 1)']
  ]);

  addHighlightBlock(s, {
    x: M + 5.1, y: 3.1, w: 3.8, h: 1.85,
    title: 'Research Objective',
    bullets: [
      'Construct an end-to-end leak-free pipeline.',
      'Optimize PR-AUC & Recall on rare fraud cases.',
      'Benchmark ensemble learning against deep unsupervised anomaly detection.'
    ]
  });
}

// =========================================================================
// SLIDE 4: PAYSIM SYNTHETIC DATASET OVERVIEW
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'PaySim Dataset: Statistical Characteristics', 4);

  // Top Stat Cards
  const stats = [
    { num: '6.36M -> 200K', label: 'Downsampled Size', desc: 'Preserves 100% fraud cases' },
    { num: '8,213', label: 'Positive Instances (isFraud = 1)', desc: 'Rare ground-truth labels' },
    { num: '11', label: 'Original Attributes', desc: 'Temporal, categorical & balance fields' }
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
      fontSize: 10, fontFace: F.fontBody, color: C.textMuted, align: 'center'
    });
  });

  // Table of fields
  const tableData = [
    [
      { text: 'Feature Name', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Type', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
      { text: 'Domain & Description', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } }
    ],
    [{ text: 'step', options: { bold: true } }, { text: 'Integer' }, { text: 'Time step in hours (1..744, representing 30 simulation days)' }],
    [{ text: 'type', options: { bold: true } }, { text: 'Categorical' }, { text: 'Transaction category: CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT' }],
    [{ text: 'amount', options: { bold: true } }, { text: 'Continuous' }, { text: 'Amount transacted in local currency units' }],
    [{ text: 'oldbalanceOrg / newbalanceOrig', options: { bold: true } }, { text: 'Continuous' }, { text: 'Originator account balance before and immediately after transaction' }],
    [{ text: 'oldbalanceDest / newbalanceDest', options: { bold: true } }, { text: 'Continuous' }, { text: 'Destination account balance before and immediately after transaction' }]
  ];

  s.addTable(tableData, {
    x: M, y: 2.45, w: CW, h: 2.5,
    border: { pt: 0.5, color: 'CBD5E1' },
    margin: [3, 4, 3, 4],
    fontSize: 10
  });
}

// =========================================================================
// SLIDE 5: EXPLORATORY DATA ANALYSIS (EDA)
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Exploratory Data Analysis: Key Behavioral Signatures', 5);

  const findings = [
    {
      title: 'Finding 1: Category Confinement',
      desc: '100% of fraud instances occur exclusively in TRANSFER and CASH_OUT.\nAll PAYMENT, CASH_IN, and DEBIT instances have exactly 0% fraud.\n-> Action: Filter dataset to only TRANSFER & CASH_OUT to reduce noise.'
    },
    {
      title: 'Finding 2: Account Drain Anomaly',
      desc: '97.56% of fraudulent transfers result in newbalanceOrig == 0.\nPerpetrators attempt to exhaust the complete victim balance in a single execution step.'
    },
    {
      title: 'Finding 3: Zero Balance Inconsistency',
      desc: 'Significant proportion of fraud transactions show zero balance delta at destination.\nDestinations receive massive funds without corresponding updates in logged destination balance.'
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
  addAcademicHeader(s, 'Feature Engineering: 14 Synthesized Predictors', 6);

  s.addText([
    { text: 'Mathematical Formulation of Domain Features:\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '1. Origin Balance Discrepancy:\n   errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '2. Destination Balance Discrepancy:\n   errorBalanceDest = oldbalanceDest + amount - newbalanceDest\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '3. Full Drain Indicator Flag:\n   is_drain_account = 1 if (oldbalanceOrg > 0 and newbalanceOrig == 0) else 0\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '4. Ratio & Temporal Dynamics:\n   amount_ratio = amount / (oldbalanceOrg + 1), hour = step % 24\n', options: { fontSize: 11.5, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.2, h: 3.8
  });

  addNotationTable(s, M + 5.4, 1.2, 3.5, [
    ['Feature Count', 'd = 14', 'Total engineered feature space'],
    ['Origin Error', 'Err_org', 'Captures ledger imbalance'],
    ['Dest Error', 'Err_dst', 'Tracks routing discrepancies'],
    ['Drain Flag', 'I_drain', 'Binary signature of account wipeout'],
    ['Night Flag', 'I_night', 'Hour in [0..5] (overnight flag)']
  ]);
}

// =========================================================================
// SLIDE 7: IMBALANCE MITIGATION STRATEGY
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Class Imbalance Mitigation: SMOTE vs ADASYN', 7);

  addHighlightBlock(s, {
    x: M, y: 1.2, w: 4.3, h: 3.75,
    title: 'The Accuracy Paradox',
    text: '• A trivial "All Normal" classifier achieves 99.87% Accuracy yet misses 100% of fraud attacks.\n\n• Evaluation mandate: Model selection must be strictly governed by Precision, Recall, F1-Score, and PR-AUC.',
    type: 'red'
  });

  s.addText([
    { text: 'Synthetic Resampling Strategies:\n\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '1. SMOTE (Synthetic Minority Over-sampling Technique):\n', options: { bold: true, color: C.blueAccent } },
    { text: 'Generates synthetic minority samples along line segments connecting k-NN neighbors in feature space.\n\n', options: { color: C.textDark } },
    { text: '2. ADASYN (Adaptive Synthetic Sampling):\n', options: { bold: true, color: C.blueAccent } },
    { text: 'Adaptively weights minority instances based on difficulty, generating more samples near decision boundaries.', options: { color: C.textDark } }
  ], {
    x: M + 4.6, y: 1.2, w: 4.3, h: 3.75
  });
}

// =========================================================================
// SLIDE 8: END-TO-END SYSTEM PIPELINE
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'End-to-End Leak-Free Machine Learning Pipeline', 8);

  const steps = [
    { n: '1', t: 'Filtering', d: 'Retain TRANSFER & CASH_OUT' },
    { n: '2', t: 'Feature Eng.', d: 'Compute 14 mathematical features' },
    { n: '3', t: 'Stratified Split', d: '80/20 Train/Test separation' },
    { n: '4', t: 'Resampling', d: 'SMOTE / ADASYN on Train only' },
    { n: '5', t: 'Training', d: 'Fit RF, XGBoost & Autoencoder' },
    { n: '6', t: 'Evaluation', d: 'Test set inference (N=40,000)' }
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
      fontSize: 11, fontFace: F.fontTitle, color: C.navyTitle, align: 'center', bold: true
    });
    s.addText(st.d, {
      x: cx + 0.05, y: 2.0, w: colW - 0.1, h: 1.3,
      fontSize: 9.5, fontFace: F.fontBody, color: C.textMuted, align: 'center'
    });
  });

  addHighlightBlock(s, {
    x: M, y: 3.65, w: CW, h: 1.3,
    title: 'Strict Protocol Against Data Leakage',
    text: '• Oversampling (SMOTE/ADASYN) is strictly executed AFTER data partitioning.\n• StandardScaler is fitted on the training split only and applied blindly to the test split.',
    type: 'blue'
  });
}

// =========================================================================
// SLIDE 9: RANDOM FOREST CLASSIFIER
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Supervised Architecture 1: Random Forest Ensemble', 9);

  s.addText([
    { text: 'Ensemble Bagging Architecture:\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• Constructs an ensemble of decorrelated Decision Trees trained on bootstrap sub-samples.\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Reduces variance without inflating bias, highly robust against feature co-linearity.\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Provides Gini Impurity-based Mean Decrease in Impurity (MDI) feature importance rankings.\n\n', options: { fontSize: 12, color: C.textDark } },
    { text: 'Optimal Hyperparameters:\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• n_estimators: 200 (SMOTE) / 500 (ADASYN)\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• max_depth: 20 | min_samples_split: 2 | max_features: sqrt', options: { fontSize: 11.5, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.0, h: 3.8
  });

  addNotationTable(s, M + 5.3, 1.2, 3.6, [
    ['Ensemble Size', 'B = 200/500', 'Number of bagged trees'],
    ['Depth Limit', 'd_max = 20', 'Prevents individual tree overfitting'],
    ['Split Criterion', 'Gini', 'Information impurity metric'],
    ['Class Weight', 'balanced', 'Inverse frequency compensation']
  ]);
}

// =========================================================================
// SLIDE 10: XGBOOST CLASSIFIER
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Supervised Architecture 2: Extreme Gradient Boosting', 10);

  s.addText([
    { text: 'Gradient Boosted Decision Trees (GBDT):\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• Optimizes second-order Taylor expansion of arbitrary differentiable loss functions.\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Incorporates explicit L1/L2 regularization to constrain model leaf complexity.\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Computational efficiency: Trains in ~41s (28x faster than Random Forest ~1180s).\n\n', options: { fontSize: 12, color: C.textDark } },
    { text: 'Tuned Hyperparameter Setup:\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• learning_rate (eta): 0.2 | n_estimators: 300\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• max_depth: 8 | subsample: 0.85 | colsample_bytree: 1.0', options: { fontSize: 11.5, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.0, h: 3.8
  });

  addNotationTable(s, M + 5.3, 1.2, 3.6, [
    ['Objective', 'Loss + Omega', 'Regularized objective function'],
    ['Learning Rate', 'eta = 0.2', 'Shrinkage step size'],
    ['Tree Depth', 'max_depth = 8', 'Max level per boosting round'],
    ['Subsample', 'rho = 0.85', 'Stochastic row sampling ratio']
  ]);
}

// =========================================================================
// SLIDE 11: DEEP AUTOENCODER ANOMALY DETECTION
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Unsupervised Architecture 3: Deep Autoencoder', 11);

  s.addText([
    { text: 'One-Class Semi-Supervised Anomaly Detection:\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• Network is trained EXCLUSIVELY on legitimate transactions (N = 122,744 normal samples).\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Learns low-dimensional manifold encoding normal transaction dynamics.\n', options: { fontSize: 12, color: C.textDark } },
    { text: '• Anomaly Scoring: Fraudulent instances fail reconstruction -> Large Reconstruction Error (MSE).\n\n', options: { fontSize: 12, color: C.textDark } },
    { text: 'Architectural Specifications:\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• Symmetric Topology: 16 -> 8 -> 4 (Bottleneck) -> 8 -> 16\n', options: { fontSize: 11.5, color: C.textDark } },
    { text: '• Decision Threshold: tau = 0.045456 (95th percentile validation error)', options: { fontSize: 11.5, color: C.textDark } }
  ], {
    x: M, y: 1.15, w: 5.0, h: 3.8
  });

  addNotationTable(s, M + 5.3, 1.2, 3.6, [
    ['Bottleneck', 'z in R^4', 'Latent embedding representation'],
    ['Loss Function', 'MSE(x, x_hat)', 'Mean Squared Reconstruction Loss'],
    ['Activation', 'ReLU', 'Non-linear hidden activations'],
    ['Threshold', 'tau = 0.0455', '95th Percentile decision cutoff']
  ]);
}

// =========================================================================
// SLIDE 12: COMPREHENSIVE EXPERIMENTAL BENCHMARK
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Experimental Results: Benchmark Comparison (N = 40,000)', 12);

  const headers = [
    { text: 'Model Architecture', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Resampling', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Precision', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Recall', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'F1-Score', options: { fill: { color: C.tblHdrBg }, color: 'FDE047', bold: true } },
    { text: 'ROC-AUC', options: { fill: { color: C.tblHdrBg }, color: 'FFFFFF', bold: true } },
    { text: 'Training Time', options: { fill: { color: C.tblHdrBg }, color: 'CBD5E1', bold: true } }
  ];

  const rows = [
    ['Random Forest', 'SMOTE', '0.9994', '0.9951', '0.9973 (Best)', '0.9994', '1187.7s'],
    ['Random Forest', 'ADASYN', '0.9982', '0.9951', '0.9966', '0.9992', '1167.5s'],
    ['XGBoost', 'SMOTE', '0.9976', '0.9951', '0.9963', '0.9993', '41.6s'],
    ['XGBoost', 'ADASYN', '0.9957', '0.9951', '0.9954', '0.9994', '41.5s'],
    ['Autoencoder', 'None (One-Class)', '0.3822', '0.7523', '0.5069', '0.9318', '215.3s']
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
    title: 'Key Empirical Deductions',
    bullets: [
      'RF + SMOTE yields peak F1 (99.73%) with only 1 False Positive across 38,357 legitimate test samples.',
      'XGBoost achieves near-identical classification power (F1 99.63%) with 28.5x computational acceleration.',
      'Autoencoder obtains 75.23% Recall without any fraud supervision during training.'
    ]
  });
}

// =========================================================================
// SLIDE 13: CONFUSION MATRIX COMPARISON
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Confusion Matrix & Error Distribution Analysis', 13);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_confusion_matrices.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: CW, h: 2.45
    });
  }

  addHighlightBlock(s, {
    x: M, y: 3.75, w: CW, h: 1.25,
    title: 'False Negative & False Positive Trade-off',
    bullets: [
      'Both RF and XGBoost miss only 8 fraud instances out of 1,643 true fraud cases (Recall = 99.51%).',
      'RF-SMOTE generates only 1 False Alarm (FP=1), whereas Autoencoder generates 1,998 FP due to unsupervised thresholding.'
    ],
    type: 'blue'
  });
}

// =========================================================================
// SLIDE 14: FEATURE IMPORTANCE RANKING
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Feature Importance: Explanatory Power of Synthesized Signals', 14);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_feature_importance.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: 4.6, h: 3.8
    });
  }

  s.addText([
    { text: 'Insights from XGBoost Feature Gain:\n\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• errorBalanceOrig accounts for ~49.9% of model decision splits.\n\n', options: { color: C.textDark, fontSize: 12 } },
    { text: '• newbalanceOrig provides ~47.2% additional predictive power.\n\n', options: { color: C.textDark, fontSize: 12 } },
    { text: '• Combined Impact: Engineered ledger discrepancies capture over 97% of overall fraud dynamics, proving the critical efficacy of domain feature engineering.', options: { color: C.textDark, fontSize: 12 } }
  ], {
    x: M + 4.8, y: 1.2, w: 4.1, h: 3.75
  });
}

// =========================================================================
// SLIDE 15: VISUAL METRICS COMPARISON
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Comparative Evaluation: Precision, Recall & F1-Score', 15);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_metrics_comparison.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: 4.8, h: 3.8
    });
  }

  s.addText([
    { text: 'Resampling Performance Analysis:\n\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• SMOTE consistently outperforms ADASYN across all tree architectures.\n\n', options: { color: C.textDark, fontSize: 12 } },
    { text: '• ADASYN synthesizes excess noise instances in boundary overlap zones, slightly increasing False Positives.\n\n', options: { color: C.textDark, fontSize: 12 } },
    { text: '• Recommendation: Pair SMOTE with XGBoost for optimal throughput and detection precision in production environments.', options: { color: C.textDark, fontSize: 12 } }
  ], {
    x: M + 5.0, y: 1.2, w: 3.9, h: 3.75
  });
}

// =========================================================================
// SLIDE 16: AUTOENCODER RECONSTRUCTION ERROR ANALYSIS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Autoencoder Anomaly Thresholding & Decision Boundary', 16);

  const chartImg = path.join(__dirname, 'slide_assets', 'academic_autoencoder_dist.png');
  if (fs.existsSync(chartImg)) {
    s.addImage({
      path: chartImg,
      x: M, y: 1.15, w: 4.6, h: 3.8
    });
  }

  s.addText([
    { text: 'Threshold Sweep Dynamics:\n\n', options: { bold: true, color: C.navyTitle, fontSize: 13 } },
    { text: '• 95th Percentile (tau = 0.0455):\nBalances Recall (75.2%) with Precision (38.2%).\n\n', options: { color: C.textDark, fontSize: 12 } },
    { text: '• 99.9th Percentile (tau = 0.7460):\nPrecision jumps to 91.5% but Recall drops to 25.4%.\n\n', options: { color: C.textDark, fontSize: 12 } },
    { text: '• Operational Role: Excellent as a secondary zero-day defense layer for unlabelled novel fraud patterns.', options: { color: C.textDark, fontSize: 12 } }
  ], {
    x: M + 4.8, y: 1.2, w: 4.1, h: 3.75
  });
}

// =========================================================================
// SLIDE 17: STREAMLIT WEB APP DEMO
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Interactive Demonstration: Streamlit Real-Time Dashboard', 17);

  addHighlightBlock(s, {
    x: M, y: 1.2, w: 4.3, h: 3.75,
    title: 'Real-Time Inference Pipeline',
    bullets: [
      'Lightweight Streamlit UI with dynamic risk probability gauges.',
      'Instant feature extraction engine (transforms user inputs to 14 feature vector).',
      'Loads trained XGBoost / Random Forest models via Joblib.',
      'Sub-millisecond single-transaction inference latency.'
    ]
  });

  addHighlightBlock(s, {
    x: M + 4.6, y: 1.2, w: 4.3, h: 3.75,
    title: 'Demonstrated Simulation Scenarios',
    bullets: [
      'Scenario 1 (Normal Transfer): Standard money transfer with valid origin and destination deltas -> Output: SAFE (99.9%).',
      'Scenario 2 (Account Drain): High-amount transfer resulting in zero origin balance -> Output: HIGH RISK FRAUD (99.8%).',
      'Batch Mode: Upload CSV to execute batch scoring and generate compliance audit reports.'
    ]
  });
}

// =========================================================================
// SLIDE 18: SUMMARY OF CONTRIBUTIONS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Summary of Project Contributions', 18);

  const contribs = [
    { title: '1. Rigorous Data Governance', desc: 'Constructed an end-to-end leak-free pipeline resolving extreme 0.13% imbalance.' },
    { title: '2. High-Impact Feature Discovery', desc: 'Formulated balance discrepancy equations contributing over 97% classification gain.' },
    { title: '3. Exceptional Empirical Metrics', desc: 'Achieved F1-Score > 0.996 and Recall > 0.995, preventing 99.5% of financial loss.' },
    { title: '4. Production Readiness', desc: 'Packaged models into an operational Streamlit dashboard for real-time inference.' }
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
    title: 'Primary Recommendation',
    text: 'XGBoost + SMOTE is selected as the production architecture due to its superior inference throughput and minimal memory footprint.',
    type: 'blue'
  });
}

// =========================================================================
// SLIDE 19: LIMITATIONS & FUTURE EXTENSIONS
// =========================================================================
{
  const s = pptx.addSlide();
  addAcademicHeader(s, 'Limitations & Future Research Trajectories', 19);

  addHighlightBlock(s, {
    x: M, y: 1.2, w: 4.3, h: 3.75,
    title: 'Current Limitations',
    bullets: [
      'Synthetic Domain Gap: PaySim simulator does not capture zero-day evasion tactics found in production banking.',
      'Static Feature Scope: Lacks relational network topology across interconnected transfer accounts.',
      'Training Retrain Overhead: Random Forest requires substantial retraining time on high-velocity data streams.'
    ],
    type: 'red'
  });

  addHighlightBlock(s, {
    x: M + 4.6, y: 1.2, w: 4.3, h: 3.75,
    title: 'Future Trajectories',
    bullets: [
      'Graph Neural Networks (GNN): Deploy GCN / GraphSAGE to detect structured money-laundering subgraphs.',
      'Stream Architecture: Integrate Apache Kafka / Apache Flink for sub-second distributed processing.',
      'Explainable AI (XAI): Integrate SHAP / TreeExplainer for legally compliant transaction blocking explanations.'
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

  s.addText('THANK YOU FOR YOUR ATTENTION!', {
    x: M, y: 1.3, w: CW, h: 0.6,
    fontSize: 26, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText('CS106 — FINANCIAL FRAUD DETECTION SYSTEM (TEAM 09)', {
    x: M, y: 1.95, w: CW, h: 0.35,
    fontSize: 13, fontFace: 'Segoe UI', color: C.goldSub, align: 'center', bold: true
  });

  s.addShape(pptx.shapes.RECTANGLE, {
    x: M + 1.2, y: 2.6, w: 6.5, h: 2.2,
    fill: { color: '21295C' },
    line: { color: '3B82F6', width: 1 }
  });

  s.addText('QUESTIONS & ANSWERS (Q&A)', {
    x: M + 1.2, y: 2.75, w: 6.5, h: 0.35,
    fontSize: 14, fontFace: F.fontTitle, color: 'FFFFFF', align: 'center', bold: true
  });

  s.addText('• Source Code: https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection\n• Reference: Lopez-Rojas et al., PaySim Mobile Money Simulator, 2016\n• Frameworks: Scikit-learn, XGBoost, Streamlit, Imbalanced-learn\n\nWe welcome all questions and feedback from the Committee.', {
    x: M, y: 3.4, w: CW, h: 1.4,
    fontSize: 10.5, fontFace: F.fontBody, color: 'CBD5E1', align: 'center'
  });
}

const outputFile = path.join(__dirname, '[Nhom9]_Slide_FraudDetection_Academic.pptx');
pptx.writeFile({ fileName: outputFile })
  .then(() => {
    console.log('Successfully generated PPTX: ' + outputFile);
  })
  .catch(err => {
    console.error('Error generating PPTX:', err);
    process.exit(1);
  });
EOF