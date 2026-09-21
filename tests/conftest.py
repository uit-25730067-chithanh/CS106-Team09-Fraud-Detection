"""Force a headless matplotlib backend before any test imports pyplot.

Without this, `show=True` code paths call `plt.show()` which blocks on an
interactive backend (TkAgg/QtAgg) waiting for a window to close -- hanging
the test run instead of failing it.
"""

import matplotlib

matplotlib.use("Agg")
