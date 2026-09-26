import matplotlib.pyplot as plt
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

scenarios = ['Full 14 Feats\n(Baseline)', 'Pruned 12 Feats\n(Tối ưu hóa)', 'No-Balance 6 Feats\n(Bỏ nhóm số dư)']
x = np.arange(len(scenarios))
width = 0.32

# Data
recall = [0.9951, 0.9951, 0.7127]
f1 = [0.9945, 0.9948, 0.7116]
fp_per_mil = [261, 235, 12436]

# Colors
c_blue = '#1E3A8A'
c_teal = '#0D9488'
c_red = '#DC2626'
c_gray = '#64748B'

# Plot 1: Classification Metrics (Recall & F1)
bars1 = ax1.bar(x - width/2, recall, width, label='Recall (Độ bao phủ)', color=c_blue, edgecolor='none', alpha=0.9)
bars2 = ax1.bar(x + width/2, f1, width, label='F1-Score', color=c_teal, edgecolor='none', alpha=0.9)

ax1.set_title('(a) Hiệu năng Nhận diện Gian lận (Recall & F1-Score)', fontsize=12, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(scenarios, fontsize=10, fontweight='medium')
ax1.set_ylim(0.5, 1.05)
ax1.set_ylabel('Điểm số (0.0 - 1.0)', fontsize=10)
ax1.legend(loc='lower left', frameon=True, fontsize=10)

# Add text labels on bars
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.012, f'{yval:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_blue)
for bar in bars2:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.012, f'{yval:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_teal)

# Highlight drop
ax1.annotate('Giảm 28.3% F1\nkhi bỏ số dư!', xy=(2 + width/2, 0.7116), xytext=(1.55, 0.58),
             arrowprops=dict(arrowstyle='->', color=c_red, lw=1.5),
             fontsize=9.5, fontweight='bold', color=c_red, ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor='#FCA5A5', alpha=0.9))

# Plot 2: Cost & Reliability (FP per Million)
colors_bar2 = [c_blue, c_teal, c_red]
bars3 = ax2.bar(scenarios, fp_per_mil, color=colors_bar2, width=0.45, alpha=0.9)
ax2.set_title('(b) Chi phí Báo động Giả Quy chiếu (FP / 1 Triệu Giao dịch)', fontsize=12, fontweight='bold', pad=15)
ax2.set_ylabel('Số ca báo động giả / 1 triệu giao dịch (Log scale)', fontsize=10)
ax2.set_yscale('log')
ax2.set_ylim(50, 40000)

for bar in bars3:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval * 1.25, f'{yval:,} ca', ha='center', va='bottom', fontsize=9.5, fontweight='bold',
             color=c_red if yval > 1000 else '#1E293B')

ax2.annotate('Tăng vọt gấp 47 lần!\n(Gây tê liệt đội ngũ kiểm toán)', xy=(2, 12436), xytext=(1.45, 2500),
             arrowprops=dict(arrowstyle='->', color=c_red, lw=1.5),
             fontsize=9.5, fontweight='bold', color=c_red, ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor='#FCA5A5', alpha=0.9))

plt.tight_layout()
out_dir = 'assignments/Final/draft/fraud-detection/reports/figures'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'ablation_study_comparison.png')
plt.savefig(out_path, dpi=300)
print(f"Successfully generated figure: {out_path}")
