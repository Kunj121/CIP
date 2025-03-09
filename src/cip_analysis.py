import pandas as pd
import numpy as np
from pull_bloomberg_cip_data import *
cip_data = compute_cip(end = '2025-03-1')

def calculate_cip_statistics(cip_data):
    # Extract only the CIP columns
    cip_columns = [col for col in cip_data.columns if col.startswith('CIP_') and col.endswith('_ln')]
    cip_df = cip_data[cip_columns]

    # Calculate statistics for each currency
    stats = pd.DataFrame({
        'Mean': cip_df.mean(),
        'Median': cip_df.median(),
        'Std Dev': cip_df.std(),
        'Min': cip_df.min(),
        'Max': cip_df.max(),
        'Range': cip_df.max() - cip_df.min(),
        '25th Percentile': cip_df.quantile(0.25),
        '75th Percentile': cip_df.quantile(0.75),
        'IQR': cip_df.quantile(0.75) - cip_df.quantile(0.25),
        'Skewness': cip_df.skew(),
        'Kurtosis': cip_df.kurtosis(),
        'Count': cip_df.count()
    }).transpose()

    # Clean up column names for display
    stats.columns = [col.replace('CIP_', '').replace('_ln', '') for col in stats.columns]

    # Calculate correlation matrix
    corr_matrix = cip_df.corr()
    corr_matrix.columns = [col.replace('CIP_', '').replace('_ln', '') for col in corr_matrix.columns]
    corr_matrix.index = [idx.replace('CIP_', '').replace('_ln', '') for idx in corr_matrix.index]

    # Calculate statistics over time (annual)
    cip_data.index = pd.to_datetime(cip_data.index)
    annual_stats = cip_df.resample('YE').agg(['mean', 'std', 'min', 'max'])

    return {
        'overall_statistics': stats,
        'correlation_matrix': corr_matrix,
        'annual_statistics': annual_stats
    }

# Function to display a nice summary of the statistics
def display_cip_summary(stats_dict, summary = False, corr = False, max_min = False):
    if summary:
        print("=" * 80)
        print("OVERALL CIP STATISTICS (in basis points)")
        print("=" * 80)
        print(stats_dict['overall_statistics'].round(2))
    if corr:

        print("\n" + "=" * 80)
        print("CORRELATION MATRIX")
        print("=" * 80)
        print(stats_dict['correlation_matrix'].round(3))

    if max_min:

        # Additional insights
        mean_values = stats_dict['overall_statistics'].loc['Mean']
        most_positive = mean_values.idxmax()
        most_negative = mean_values.idxmin()

        print("\n" + "=" * 80)
        print("KEY INSIGHTS")
        print("=" * 80)
        print(f"Currency with largest positive mean CIP deviation: {most_positive} ({mean_values[most_positive]:.2f} bps)")
        print(f"Currency with largest negative mean CIP deviation: {most_negative} ({mean_values[most_negative]:.2f} bps)")