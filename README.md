# Financial Fraud Detection System (Fraud Shield)

<p align="center">
  <img src="docs/cover.png" alt="Financial Fraud Detection Project Cover" width="100%" style="border-radius: 8px;" />
</p>

<p align="center">
  <a href="https://www.uit.edu.vn/"><img src="https://img.shields.io/badge/UIT-CS106.F31.CN2.TTNT-blue.svg?style=for-the-badge&logo=vimeo" alt="UIT CS106" /></a>
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/XGBoost-2.0%2B-EB1C24.svg?style=for-the-badge" alt="XGBoost" />
  <img src="https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Tests-110%20passed-22C55E.svg?style=for-the-badge&logo=pytest&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/badge/License-MIT-gray.svg?style=for-the-badge" alt="License MIT" />
</p>

<p align="center">
  <b>English</b> | <a href="README-vi.md">Tiếng Việt</a>
</p>

> **Final Project for Artificial Intelligence (CS106.F31.CN2.TTNT)**  
> **University of Information Technology — VNU-HCM (UIT)**  
> **Topic 07:** Financial Fraud Detection System  
> **Conducted by:** Team 09 (7 members)  
> **Advisor:** Assoc. Prof. Dr. Nguyen Dinh Hien

---

## Table of Contents

1. [Problem Statement & Real-World Context](#1-problem-statement--real-world-context)
2. [Engineering Journey & 3 Academic Pillars](#2-engineering-journey--3-academic-pillars)
3. [Domain Knowledge Representation & 14 Engineered Features](#3-domain-knowledge-representation--14-engineered-features)
4. [End-to-End System Architecture](#4-end-to-end-system-architecture)
5. [Experimental Results & Model Benchmark](#5-experimental-results--model-benchmark)
6. [Controlled Ablation Study & Feature Pruning](#6-controlled-ablation-study--feature-pruning)
7. [Interactive Streamlit Web Dashboard](#7-interactive-streamlit-web-dashboard)
8. [Repository Directory Layout](#8-repository-directory-layout)
9. [Installation & Experiment Replication Guide](#9-installation--experiment-replication-guide)
10. [Team Members & Role Allocation](#10-team-members--role-allocation)
11. [Academic Deliverables & License](#11-academic-deliverables--license)
12. [Acknowledgements](#12-acknowledgements)

---

## 1. Problem Statement & Real-World Context

In today's digital economy, mobile money services and digital wallets have experienced exponential transaction growth. However, financial fraud schemes have grown increasingly sophisticated (money laundering, account takeover, layered mule transfers), causing tens of billions of dollars in losses annually and eroding user trust.

Detecting fraudulent transactions on the real-world simulated [PaySim Mobile Money Dataset (Kaggle)](https://www.kaggle.com/datasets/ealaxi/paysim1) (6,362,620 raw records) introduces two fundamental challenges:

* **Extreme Class Imbalance:** Fraudulent transactions account for only **~0.129%** of all records (approximately 1 fraudulent transaction per 775 legitimate ones). Conventional classifiers readily fall victim to the "Accuracy Paradox" by blindly predicting the majority normal class.
* **Asymmetric Cost Matrix:**
  * *Missed Fraud (False Negative - FN):* Causes direct financial theft for account holders, regulatory penalties, and reputational risk for financial institutions.
  * *False Alarm (False Positive - FP):* Wrongfully freezes accounts of legitimate customers, creates friction, and overburdens fraud investigation teams.

---

## 2. Engineering Journey & 3 Academic Pillars

Incorporating constructive academic critiques from the project advisor (**Assoc. Prof. Dr. Nguyen Dinh Hien**) during the Stage 1 defense, Team 09 restructured the entire project around **3 methodological pillars**:

```text
                       ╔══════════════════════════════════════════════════════════╗
                       ║        TEAM 09 CORE METHODOLOGICAL PILLARS (AI CS106)    ║
                       ╚══════════════════════════════════════════════════════════╝
                                    │                           │
          ┌─────────────────────────┴─────────────┐             └─────────────────────────┐
          ▼                                       ▼                                       ▼
 ┌─────────────────────────────┐        ┌─────────────────────────────┐        ┌─────────────────────────────┐
 │    PILLAR 1: EMPIRICAL      │        │    PILLAR 2: LEAK-FREE      │        │ PILLAR 3: KNOWLEDGE REPR.   │
 │  • Controlled Ablation      │        │  • 4-stage anti-leak guards │        │  • Double-entry accounting  │
 │  • Quantitative F1 / FP     │        │  • Isolated Scaler & Resamp │        │  • 14 domain features       │
 │  • Feature Pruning study    │        │  • Prevalence Projection    │        │  • Interpretable decisions  │
 └─────────────────────────────┘        └─────────────────────────────┘        └─────────────────────────────┘
```

1. **Pillar 1 — Empirical Quantitative Evidence:** Avoid subjective conclusions. Design independent **Ablation Studies** to rigorously quantify the contribution of balance-related variables to model performance.
2. **Pillar 2 — Anti-Leakage Defense & Reality Projection:**
   * Enforce **4 Leak-Free Gates**: Strictly isolate the Train and Test splits across all feature scaling (`StandardScaler`), decision threshold tuning, and oversampling algorithms (`SMOTE-NC` / `ADASYN`).
   * Perform **Prevalence Projection (0.129%)**: Re-project evaluation metrics back to the true banking transaction distribution to reflect realistic false alarm rates in production.
3. **Pillar 3 — Domain Knowledge Representation (AI Core):** Reject black-box training on raw tabular columns. Instead, apply core AI principles to encode double-entry accounting rules and cash-flow dynamics into the feature space.

---

## 3. Domain Knowledge Representation & 14 Engineered Features

Before model training, raw data is filtered and enriched through domain rules:
* **High-Risk Domain Filtering:** Exploratory analysis revealed that **100% of fraud cases** occur exclusively within two transaction types: `TRANSFER` and `CASH_OUT`. Removing three benign types (`PAYMENT`, `CASH_IN`, `DEBIT`) safely reduces data volume by **56.5%** with zero fraud sample loss.
* **14 Engineered Domain Features:**

| No. | Feature Name | Category | Knowledge Representation & Business Rationale |
|:---:|---|:---:|---|
| **1** | `amount` | Raw | Monetary value transferred in the transaction. |
| **2** | `oldbalanceOrg` | Raw | Initial account balance of the origin sender before transaction. |
| **3** | `newbalanceOrig` | Raw | New balance of the origin sender after transaction. |
| **4** | `oldbalanceDest` | Raw | Initial account balance of the destination recipient before transaction. |
| **5** | `newbalanceDest` | Raw | New balance of the destination recipient after transaction. |
| **6** | `type_CASH_OUT` | One-Hot | Indicator for cash withdrawal at ATM/agent (final stage of laundering). |
| **7** | `type_TRANSFER` | One-Hot | Indicator for funds transfer between accounts. |
| **8** | `errorBalanceOrig` | **Double-Entry** | `oldbalanceOrg - amount - newbalanceOrig`: Accounting balance error on sender side. |
| **9** | `errorBalanceDest` | **Double-Entry** | `oldbalanceDest + amount - newbalanceDest`: Accounting balance error on receiver side. |
| **10** | `amount_to_oldbalance_ratio` | Financial Ratio | Transfer amount relative to origin balance; detects overdrawn transfers. |
| **11** | `amount_to_dest_ratio` | Financial Ratio | Transfer amount relative to destination balance; detects cash dumping into fresh accounts. |
| **12** | `is_emptying_origin` | **Drainage Flag** | Binary flag `(oldbalanceOrg == amount)`: Detects complete account drainage (present in **97.55%** of all fraud events). |
| **13** | `hour_of_day` | Temporal Cycle | `step % 24`: Transaction hour within the 24-hour daily cycle. |
| **14** | `is_night_transaction` | Risk Window | Binary indicator for transactions initiated during late-night hours (00:00 – 06:00). |

---

## 4. End-to-End System Architecture

The complete pipeline spans data ingestion, clean preprocessing, multi-model training, and an interactive audit dashboard:

```text
[Raw PaySim Dataset: 6.36M records]
               │
               ▼
[Stage 1: Domain Filtering & Stratified Downsampling]
  ├── Retain high-risk types only: TRANSFER & CASH_OUT (safely drops 56.5% benign traffic)
  └── Stratified downsampling to 200,000 samples (preserves all 8,213 original fraud cases)
               │
               ▼
[Stage 2: Leak-Free Train / Test Partitioning]
  ├── Train Set (80% ~ 160,000 samples) ──► Fit StandardScaler ──► Oversampling (SMOTE-NC / ADASYN)
  └── Test Set  (20% ~ 40,000 samples)  ──► Transform Scaler   ──► Preserves true class imbalance
               │
               ├───────────────────────────────────────────────┐
               ▼                                               ▼
[Stage 3A: Supervised Learning Models]         [Stage 3B: Unsupervised Learning Model]
  ├── Random Forest (200 trees, max_depth=20)     └── Deep Autoencoder (Reconstruction Error)
  └── XGBoost (n_estimators=300, max_depth=6)         • Learns normal transaction patterns
               │                                       • Sets anomaly threshold at 95th percentile
               ├───────────────────────────────────────────────┘
               ▼
[Stage 4: Multi-Model Evaluation Hub]
  ├── Computes Precision, Recall, F1, ROC-AUC, PR-AUC, and Inference Latency
  └── Generates ROC Curves, PR Curves, Confusion Matrices, and Feature Importance plots
               │
               ▼
[Stage 5: Interactive Streamlit Web Dashboard]
  ├── Real-time single transaction assessment (manual input form + presets)
  ├── Batch audit processing via uploaded CSV / JSON files
  └── 4-stage transparent inspection modal explaining risk decisions
```

---

## 5. Experimental Results & Model Benchmark

All candidate models were evaluated on the independent test split (**40,000 transactions**, maintaining natural class distribution):

| Model Architecture | Imbalance Strategy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Training Duration |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Random Forest** | **SMOTE-NC** | **0.9994** | **0.9951** | **0.9973** | **0.9994** | **0.9983** | 1,187.0 s |
| Random Forest | ADASYN | 0.9982 | 0.9951 | 0.9966 | 0.9992 | 0.9978 | 1,245.3 s |
| **XGBoost** | **SMOTE-NC** | 0.9976 | 0.9951 | 0.9963 | 0.9993 | 0.9969 | **57.9 s** *(20x faster)* |
| XGBoost | ADASYN | 0.9957 | 0.9951 | 0.9954 | 0.9994 | 0.9976 | 62.1 s |
| **Deep Autoencoder** | Unsupervised | 0.3822 | 0.7523 | 0.5069 | 0.9318 | 0.5973 | 142.6 s |

---

### Visual Benchmark Evidence

#### 1. Confusion Matrix Component Decomposition
Detailed counts of True Positives, True Negatives, False Positives, and False Negatives across the 40,000-sample test set:

<p align="center">
  <img src="reports/figures/confusion_matrix_components.png" alt="Confusion Matrix Components" width="95%" style="border-radius: 6px;" />
</p>

> **Matrix Insights:**
> * **Random Forest (SMOTE-NC):** Achieves near-perfect discrimination with only **1 False Positive (FP = 1)** out of 38,358 legitimate transactions, correctly flagging **1,634 out of 1,642 fraud cases** (only 8 missed).
> * **XGBoost (SMOTE-NC):** Incurs **4 False Positives (FP = 4)** while missing the same 8 fraud cases, but requires only **57.94 seconds** for training and sub-millisecond inference, making it the premier candidate for high-throughput, real-time production pipelines.

#### 2. Comprehensive ROC & PR Curves
Model discriminative capability and stability under extreme data imbalance:

<p align="center">
  <img src="reports/figures/roc_curves_all.png" alt="ROC Curves Comparison" width="48%" style="border-radius: 6px; display: inline-block; margin-right: 2%;" />
  <img src="reports/figures/pr_curves_all.png" alt="PR Curves Comparison" width="48%" style="border-radius: 6px; display: inline-block;" />
</p>

#### 3. Feature Importance Analysis
Empirical validation of the double-entry accounting features:

<p align="center">
  <img src="reports/figures/feature_importance_comparison.png" alt="Feature Importance Comparison" width="90%" style="border-radius: 6px;" />
</p>

> **Key Observation:** In the XGBoost model, the two domain-engineered double-entry features (`errorBalanceOrig` and `errorBalanceDest`) account for **97.1% of total decision tree Gain**, completely dominating the raw unengineered columns.

---

## 6. Controlled Ablation Study & Feature Pruning

Addressing the defense critique (*"Does the model blindly rely on balance fields or learn true accounting logic?"*), Team 09 conducted an independent 3-scenario ablation experiment on XGBoost (SMOTE-NC):

| Experimental Scenario | Feature Count | Recall | F1-Score | FP / 1M Tx | Operational Impact & Audit Assessment |
|---|:---:|:---:|:---:|:---:|---|
| **Scenario 1: Full_14 (Baseline)** | 14 features | **0.9951** | **0.9945** | 261 | Baseline model leveraging all double-entry and temporal attributes. |
| **Scenario 2: Pruned_12 (Optimized)** | 12 features *(removes `is_night`, `is_large`)* | **0.9951** | **0.9948** | **235** | **Maintains identical Recall**, slightly increases F1, and cuts false alarms from 261 to **235 per million transactions**, delivering a lighter, more robust production model. |
| **Scenario 3: No_Balance_6 (Balance Stripped)** | 6 pure transaction features | 0.7127 | 0.7116 | 12,436 | **F1 drops by 28.3%**, missed fraud cases jump from 8 to **472 (59x increase)**, and false alarms surge **47x**. |

<p align="center">
  <img src="reports/figures/ablation_study_comparison.png" alt="Ablation Study Comparison" width="90%" style="border-radius: 6px;" />
</p>

> **Practical Takeaways from Ablation Study:**
> 1. Balance features are not mere arithmetic values; they reflect **double-entry bookkeeping invariants**: fraudsters compromising an account attempt to drain all available liquidity (`oldbalanceOrg == amount`), creating an irreconcilable balance discrepancy.
> 2. The **Pruned_12** scenario demonstrates that discarding weakly discriminating indicators (`is_night_transaction`, `is_large_transaction`) reduces overfitting risks and yields superior generalization on noisy production traffic.

---

## 7. Interactive Streamlit Web Dashboard

The **Fraud Shield Web Dashboard** is designed specifically for fraud analysts and bank auditors:

* **Real-Time Single Transaction Assessment:** Supports manual parameter entry and instant testing via pre-configured scenarios (Legitimate transfer, Virtual mule laundering, Midnight account drainage).
* **3-Tier Risk Classification:**
  * **Legitimate (Low Risk):** Fraud probability < 30%.
  * **Suspicious (Medium Risk):** Fraud probability between 30% – 50%; triggers step-up biometric verification.
  * **Fraud Alert (High Risk):** Fraud probability ≥ 50%; immediate transaction freeze.
* **4-Stage Pipeline Modal:** Transparently reveals raw input ingestion, 14-feature transformation, scaler normalization, and final XGBoost probability scoring.

<p align="center">
  <img src="demo/screenshots/prediction-fraud.png" alt="Fraud Prediction Warning" width="48%" style="border-radius: 6px; display: inline-block; margin-right: 2%;" />
  <img src="demo/screenshots/prediction-warning.png" alt="Warning Prediction State" width="48%" style="border-radius: 6px; display: inline-block;" />
</p>
<p align="center">
  <img src="demo/screenshots/dashboard-dark.png" alt="Dashboard Dark Mode" width="98%" style="border-radius: 6px; margin-top: 10px;" />
</p>

> **System Demo Video:** Watch the **1 minute 37 second** system walkthrough video at [Fraud Shield Demo Video](https://aceteam-uit.vercel.app/l/70vGyu) (referenced on **Slide 20 of the official presentation deck**).

---

## 8. Repository Directory Layout

The repository strictly follows UIT academic curation standards (`uit:repo-curator`):

```text
CS106-Team09-Fraud-Detection/
├── docs/                                           ← System architecture and design documentation
│   ├── cover.png                                   ← Official project banner
│   ├── system-architecture.md                      ← Layered system architecture design
│   ├── code-standards.md                           ← Coding standards and module contracts
│   ├── project-roadmap.md                          ← 4-sprint roadmap and task log
│   └── project-overview-pdr.md                     ← Project overview and research foundations
├── src/                                            ← Modular Python source code (<200 lines/file)
│   ├── preprocessing/                              ← Ingestion, filtering, splitting, scaler, resampling
│   │   ├── data_loader.py
│   │   ├── data_splitter.py
│   │   ├── feature_scaler.py
│   │   └── imbalance_handler.py
│   ├── models/                                     ← Machine learning model definitions and training
│   │   ├── random_forest_model.py
│   │   ├── xgboost_model.py
│   │   └── autoencoder_model.py
│   ├── evaluation/                                 ← Metrics calculation, plotting, and reporting
│   │   ├── metrics_calculator.py
│   │   ├── model_comparator.py
│   │   ├── confusion_matrix_plot.py
│   │   ├── plot_roc_curve.py
│   │   ├── plot_feature_importance.py
│   │   └── prevalence_projection.py
│   └── utils/                                      ← Constants, random seeds, and utility helpers
│       └── helpers.py
├── notebooks/                                      ← 6 Jupyter Notebooks running cleanly (100% executed)
│   ├── 01_eda.ipynb                                ← Exploratory data analysis and correlation study
│   ├── 02_imbalance_handling.ipynb                 ← SMOTE-NC and ADASYN resampling experiments
│   ├── 03_model_random_forest.ipynb                ← Random Forest training and tuning
│   ├── 04_model_xgboost.ipynb                      ← XGBoost training and hyperparameter optimization
│   ├── 05_model_autoencoder.ipynb                  ← Deep Autoencoder anomaly detection network
│   └── 06_evaluation_comparison.ipynb              ← Comprehensive multi-model cross-evaluation
├── data/
│   ├── raw/                                        ← Raw data folder (paysim.csv, gitignored)
│   └── processed/                                  ← 8 lightweight processed .pkl files (~18MB total)
│       └── README.md                               ← Usage documentation for processed data
├── models/                                         ← Pre-trained model weights and fitted scalers
│   ├── scaler.pkl                                  ← Pre-fitted StandardScaler on training split
│   ├── xgb_smote.json                              ← XGBoost checkpoint (SMOTE-NC)
│   ├── xgb_adasyn.json                             ← XGBoost checkpoint (ADASYN)
│   └── autoencoder_meta.json                       ← Autoencoder network weights and threshold
├── reports/                                        ← Empirical evidence and comparative benchmark logs
│   ├── figures/                                    ← 10 high-resolution figures (ROC, PR, CM, Ablation)
│   ├── model_comparison.csv                        ← Benchmark metrics table across 5 configurations
│   ├── ablation_study_results.csv                  ← Quantitative results of 3 ablation scenarios
│   ├── ablation_study_summary.txt                  ← In-depth analytical summary of ablation study
│   └── *.pkl, *.txt                                ← Prediction caches and training logs
├── demo/                                           ← Interactive Streamlit Fraud Shield Web Application
│   ├── app.py                                      ← Application entry point
│   ├── inference.py                                ← Real-time XGBoost inference interface
│   ├── analysis_pipeline.py                        ← 4-stage transaction inspection pipeline
│   ├── history_store.py                            ← Local transaction history store
│   ├── screenshots/                                ← UI screenshots captured via Playwright
│   └── requirements-demo.txt                       ← Lightweight dependencies for demo only
├── slide/                                          ← Academic presentation materials
│   ├── [Nhom9]_Slide_FraudDetection.pdf            ← Official 21-page slide deck (UIT standard)
│   └── slide_assets/                               ← Extracted graphics and presentation figures
├── scripts/                                        ← Standalone experiment runners
│   ├── run_ablation_study.py                       ← Replicability script for 3 ablation scenarios
│   └── plot_ablation_study.py                      ← Plot generator for ablation comparison
├── tests/                                          ← Automated test suite (110 unit and integration tests)
│   ├── demo/                                       ← Tests for demo inference flow and UI logic
│   └── evaluation/                                 ← Tests for metric calculations and plotting
├── requirements.txt                                ← Full project dependency manifest
├── pytest.ini                                      ← Automated Pytest test configuration
├── run_preprocessing.py                            ← Complete data preprocessing pipeline script
├── LICENSE                                         ← MIT Open-Source License
├── README-vi.md                                    ← Vietnamese project documentation
└── README.md                                       ← English project documentation (this file)
```

---

## 9. Installation & Experiment Replication Guide

### 1. Environment Setup

Requires Python **3.10 to 3.12** (Python 3.11 or 3.12 recommended):

```bash
# Clone the repository
git clone git@github.com-uit:uit-25730067-chithanh/CS106-Team09-Fraud-Detection.git
cd CS106-Team09-Fraud-Detection

# Initialize and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate        # On Linux / macOS
# .venv\Scripts\activate         # On Windows

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Launch Streamlit Web Demo

Pre-fitted scalers and lightweight model checkpoints are bundled under `models/`. The interactive interface can be launched immediately without re-training:

```bash
streamlit run demo/app.py
```
*Access the dashboard at:* `http://localhost:8501`.

### 3. Replicate Ablation Study

To re-run the 3 ablation scenarios and re-generate the comparison chart:

```bash
# Execute 3 experimental scenarios on XGBoost
python3 scripts/run_ablation_study.py

# Generate comparison plots in reports/figures/
python3 scripts/plot_ablation_study.py
```

### 4. Execute Automated Test Suite

The automated test suite verifies data integrity, metric calculations, and real-time inference logic:

```bash
python3 -m pytest -q
```
*Expected result:* `110 passed` in ~20 seconds.

---

## 10. Team Members & Role Allocation

The official team roster and task allocations are aligned with `Danh_sach_nhom.xlsx` and Page 4 of the official Academic Report:

| No. | Full Name | Student ID | Course Code | Role | Primary Project Responsibilities |
|:---:|---|:---:|:---:|:---:|---|
| **1** | **Tran Hoang Hon** | `26410046` | CS106.F31.CN2.TTNT | **Team Lead** | Project management (PM), overall sprint coordination, presentation slide deck, and final deliverable packaging |
| **2** | **Dang Chi Thanh** | `25730067` | CS106.F31.CN2.TTNT | **Member** | System architecture design, Exploratory Data Analysis (EDA), data preprocessing pipeline, and 14-feature engineering; Notebook 01 |
| **3** | **Hoang Cao Son** | `25730061` | CS106.F31.CN2.TTNT | **Member** | Class imbalance handling (SMOTE-NC, ADASYN), Random Forest model research, training, and optimization; Notebook 02 & 03 |
| **4** | **Bui Thi My Cam** | `25730013` | CS106.F31.CN2.TTNT | **Member** | XGBoost model research, training, and hyperparameter tuning; Deep Autoencoder neural network for anomaly detection; Notebook 04 & 05 |
| **5** | **Nguyen Duy Khang** | `26410055` | CS106.F31.CN2.TTNT | **Member** | Multi-model cross-evaluation pipeline (ROC-AUC, PR-AUC, F1-Score), comparative benchmarking, and visualization; Notebook 06 |
| **6** | **Vu Van Duy** | `26410031` | CS106.F31.CN2.TTNT | **Member** | Academic report authoring (Chapters 1–7), theoretical foundations, experimental analysis, and confidence interval estimation |
| **7** | **Pham Thanh Trung** | `26410141` | CS106.F31.CN2.TTNT | **Member** | Streamlit Web Demo design and development, real-time inference integration, and video walkthrough production |

*Note:* 100% of team members contributed responsibly and mutually approved all project deliverables.

---

## 11. Academic Deliverables & License

* **Full Academic Report (31-page PDF, UIT Standard):** The official report `[Nhom9]_Report_FraudDetection.pdf` was submitted to the UIT Moodle LMS system under institutional academic integrity and anti-plagiarism guidelines.
* **Official Presentation Deck (21-page PDF):** Available directly at [[Nhom9]_Slide_FraudDetection.pdf](slide/[Nhom9]_Slide_FraudDetection.pdf).
* **User Manual:** Clean print-ready academic documentation available at `Huong_dan_su_dung.pdf`.
* **Open-Source License:** This project is distributed under the **MIT License**. For details, see [LICENSE](LICENSE).

---

## 12. Acknowledgements

Team 09 would like to express our sincere gratitude to **Assoc. Prof. Dr. Nguyen Dinh Hien** (Course Instructor for Artificial Intelligence - CS106) for his dedicated guidance, constructive critiques, and valuable recommendations that helped the team refine and elevate the quality of this project following the Stage 1 defense.

---

<p align="center">
  <i>Artificial Intelligence Course Project (CS106.F31.CN2.TTNT) — University of Information Technology, VNU-HCM.</i>
</p>
