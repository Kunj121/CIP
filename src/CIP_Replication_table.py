"""
Saves CIP table in Output
"""

import pull_bloomberg_cip_data
from settings import config
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

# Setup paths
DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

sns.set()

# Load data
df = pull_bloomberg_cip_data.load_raw(end='2020-01-01', excel=True)


# Save figure
filename = OUTPUT_DIR / 'CIP_Replication.pdf'


print(f"Table saved at {filename}")

# Show plot
plt.show()
