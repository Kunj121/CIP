import sys
import os
import pandas as pd
import numpy as np
import argparse  # ✅ Fix: Handle command-line arguments

# Add the 'src/' folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from pull_bloomberg_cip_data import *

def calculate_cip_statistics(cip_data):
    """
    Compute key statistics on CIP deviations dataset.
    Returns a dictionary containing:
    - overall_statistics: Summary statistics (mean, std, min, max, etc.)
    - correlation_matrix: Correlation matrix of CIP deviations
    - annual_statistics: CIP statistics computed on a yearly basis
    """

    if cip_data is None or cip_data.empty:
        raise ValueError("Error: cip_data is empty or None. Check if compute_cip() is working correctly.")

    stats_dict = {}

    # Extract only the CIP columns
    cip_columns = [col for col in cip_data.columns if col.startswith('CIP_') and col.endswith('_ln')]
    cip_df = cip_data[cip_columns]

    if cip_df.empty:
        raise ValueError("Error: cip_df is empty after filtering CIP columns.")

    # Compute overall statistics
    stats_dict["overall_statistics"] = cip_df.describe()

    # Compute correlation matrix
    stats_dict["correlation_matrix"] = cip_df.corr()

    # Compute annual statistics
    cip_data.index = pd.to_datetime(cip_data.index)
    stats_dict["annual_statistics"] = cip_df.resample('YE').agg(['mean', 'std', 'min', 'max'])

    print("DEBUG: Stats dictionary created with keys ->", stats_dict.keys())  # Debugging output

    return stats_dict


### **🖥️ Display Functions**
def display_cip_summary(stats_dict):
    """Display overall CIP statistics."""
    if "overall_statistics" not in stats_dict:
        raise KeyError("Key 'overall_statistics' not found in stats dictionary.")

    print("\n" + "=" * 80)
    print("OVERALL CIP STATISTICS (in basis points)")
    print("=" * 80)
    print(stats_dict["overall_statistics"].round(2))


def display_cip_corr(stats_dict):
    """Display the correlation matrix of CIP deviations."""
    if "correlation_matrix" not in stats_dict:
        raise KeyError("Key 'correlation_matrix' not found in stats dictionary.")

    print("\n" + "=" * 80)
    print("CORRELATION MATRIX")
    print("=" * 80)
    print(stats_dict["correlation_matrix"].round(3))


def display_cip_max_min(stats_dict):
    """Display min/max statistics for CIP analysis."""
    print("\nDEBUG: Available keys in stats_dict:", stats_dict.keys())

    if "overall_statistics" not in stats_dict:
        raise KeyError("Key 'overall_statistics' not found in stats dictionary.")

    mean_values = stats_dict["overall_statistics"].loc["mean"]  # Fix: Use lowercase "mean"
    most_positive = mean_values.idxmax()
    most_negative = mean_values.idxmin()

    print("\n" + "=" * 80)
    print("EXTREME CIP DEVIATIONS")
    print("=" * 80)
    print(f"Most Positive CIP Deviation: {most_positive} ({mean_values[most_positive]:.2f} bps)")
    print(f"Most Negative CIP Deviation: {most_negative} ({mean_values[most_negative]:.2f} bps)")