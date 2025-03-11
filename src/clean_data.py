"""
Cleans the raw data pulled from Github and pushes it into a csv
"""

from src.settings import config
from pathlib import Path
import src.pull_bloomberg_cip_data

DATA_DIR = Path(config("DATA_DIR"))  # Should point to '_data'

df = src.pull_bloomberg_cip_data.load_raw('2025-03-01')
output_file = DATA_DIR / "tidy_data.csv"

df.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")