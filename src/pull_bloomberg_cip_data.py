import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from io import BytesIO
import os

def download():
    target_file = "../data_manual/CIP_2025.xlsx"
    import requests, os
    url = "https://raw.githubusercontent.com/Kunj121/CIP/main/data_manual/CIP_2025.xlsx"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error on bad responses
    # Ensure the data_manual folder exists.
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    # Write the file to the target path.
    with open(target_file, "wb") as f:
        f.write(response.content)
    print(f"File saved to {os.path.abspath(target_file)}")
    df =  pd.read_excel(target_file)
    return df




def fetch_bloomberg_historical_data():
    """
    Fetch historical data from Bloomberg using xbbg for predefined sets of tickers,
    clean up the data, and merge into a single DataFrame similar to the existing process.

    Parameters
    ----------
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format, defaults to "2010-01-01"
    end_date : str, optional
        End date in 'YYYY-MM-DD' format, defaults to "2025-12-31"

    Returns
    -------
    pandas.DataFrame
        A merged DataFrame containing all the processed historical data
        (spot rates, swap rates, interest rates) for AUD, CAD, CHF, EUR,
        GBP, JPY, NZD, and SEK (with USD as reference).
    """
    from xbbg import blp
    start_date = "2010-01-01"
    end_date = "2025-12-31"

    # Tickers for Spot Rates
    currency_tickers = [
        "ADSOC CMPN Curncy",  # AUD
        "CDSOC CMPN Curncy",  # CAD
        "SFSNTC CMPN Curncy", # CHF
        "EUSWEC CMPN Curncy", # EUR
        "BPSWSC CMPN Curncy", # GBP
        "JYSOC CMPN Curncy",  # JPY
        "NDSOC CMPN Curncy",  # NZD
        "USSOC CMPN Curncy",  # USD/SEK
    ]

    # Tickers for 3M interest rates (overnight or 3M LIBOR, depending on the data vendor)
    rate_tickers = [
        "US0003M CMPN Curncy",  # USD
        "EE0003M CMPN Curncy",  # EUR
        "JY0003M CMPN Curncy",  # JPY
        "AU0003M CMPN Curncy",  # AUD
        "CD0003M CMPN Curncy",  # CAD
        "SF0003M CMPN Curncy",  # CHF
        "NZ0003M CMPN Curncy",  # NZD
        "SK0003M CMPN Curncy"   # SEK
    ]

    # Tickers for 3M swap rates (or 3M forward quotes)
    swap_tickers = [
        "AUD CMPN Curncy",
        "CAD CMPN Curncy",
        "CHF CMPN Curncy",
        "EUR CMPN Curncy",
        "GBP CMPN Curncy",
        "JPY CMPN Curncy",
        "NZD CMPN Curncy",
        "SEK CMPN Curncy"
    ]

    # Mapping from Bloomberg columns to simpler names
    currency_mapping = {
        "ADSOC CMPN Curncy_PX_LAST": "AUD",
        "CDSOC CMPN Curncy_PX_LAST": "CAD",
        "SFSNTC CMPN Curncy_PX_LAST": "CHF",
        "EUSWEC CMPN Curncy_PX_LAST": "EUR",
        "BPSWSC CMPN Curncy_PX_LAST": "GBP",
        "JYSOC CMPN Curncy_PX_LAST": "JPY",
        "NDSOC CMPN Curncy_PX_LAST": "NZD",
        "USSOC CMPN Curncy_PX_LAST": "SEK"
    }

    rate_mapping = {
        "US0003M CMPN Curncy_PX_LAST": "USD_IR",
        "EE0003M CMPN Curncy_PX_LAST": "EUR_IR",
        "JY0003M CMPN Curncy_PX_LAST": "JPY_IR",
        "AU0003M CMPN Curncy_PX_LAST": "AUD_IR",
        "CD0003M CMPN Curncy_PX_LAST": "CAD_IR",
        "SF0003M CMPN Curncy_PX_LAST": "CHF_IR",
        "NZ0003M CMPN Curncy_PX_LAST": "NZD_IR",
        "SK0003M CMPN Curncy_PX_LAST": "SEK_IR"
    }

    swap_mapping = {
        "AUD CMPN Curncy_PX_LAST": "AUD_CURNCY3M",
        "CAD CMPN Curncy_PX_LAST": "CAD_CURNCY3M",
        "CHF CMPN Curncy_PX_LAST": "CHF_CURNCY3M",
        "EUR CMPN Curncy_PX_LAST": "EUR_CURNCY3M",
        "GBP CMPN Curncy_PX_LAST": "GBP_CURNCY3M",
        "JPY CMPN Curncy_PX_LAST": "JPY_CURNCY3M",
        "NZD CMPN Curncy_PX_LAST": "NZD_CURNCY3M",
        "SEK CMPN Curncy_PX_LAST": "SEK_CURNCY3M"
    }

    fields = ["PX_LAST"]

    # Helper to flatten the multi-index
    def process_df(df, column_mapping):
        if not df.empty:
            df.columns = [f"{t[0]}_{t[1]}" for t in df.columns]
            df.rename(columns=column_mapping, inplace=True)
            df.set_index('date', inplace=True)
        return df

    # Pull each set of tickers
    currency_df = process_df(
        blp.bdh(
            tickers=currency_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        ),
        currency_mapping
    )

    rate_df = process_df(
        blp.bdh(
            tickers=rate_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        ),
        rate_mapping
    )

    swap_df = process_df(
        blp.bdh(
            tickers=swap_tickers,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
        ),
        swap_mapping
    )

    # For demonstration, we replicate the "3M forward" concept by appending
    # the spot data (currency_df) to the swap rates (swap_df).
    # In a real scenario, you might need the forward points separately
    # to add to / subtract from spot. This code treats 'swap_df' as 3M rates.

    # We keep the original spot rates in swap_df as well for reference:
    cols = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
    for col in cols:
        swap_df[f"{col}_CURNCY"] = currency_df[col]

    # Convert certain currencies to reciprocals
    reciprocal_currencies = ['EUR', 'GBP', 'AUD', 'NZD']
    for ccy in reciprocal_currencies:
        if ccy in currency_df.columns:
            currency_df[ccy] = 1.0 / currency_df[ccy]
        if f"{ccy}_CURNCY" in swap_df.columns:
            swap_df[f"{ccy}_CURNCY"] = 1.0 / swap_df[f"{ccy}_CURNCY"]
        if f"{ccy}_CURNCY3M" in swap_df.columns:
            swap_df[f"{ccy}_CURNCY3M"] = 1.0 / swap_df[f"{ccy}_CURNCY3M"]

    # Rename columns so currency_df columns read as "XXX_CURNCY"
    for col in cols:
        if col in currency_df.columns:
            currency_df.rename(columns={col: f"{col}_CURNCY"}, inplace=True)

    # Merge all
    df_merged = (
        currency_df
        .merge(swap_df, left_index=True, right_index=True, how='inner')
        .merge(rate_df, left_index=True, right_index=True, how='inner')
    )

    return df_merged


def plot_cip(end ='2025-03-01',excel=True):
    """
    Reads data from Excel if excel=True, otherwise fetch from Bloomberg using xbbg.

    After retrieving data, calculates a CIP measure and cleans outliers.
    Finally, plots the CIP spreads for a 2010-2019 subset and the full range.

    Parameters
    ----------
    start : str, optional
        Start date in 'YYYY-MM-DD' format, used if excel=False
    end : str, optional
        End date in 'YYYY-MM-DD' format, used if excel=False
    excel : bool, optional
        If True, read from a local Excel file. If False, use Bloomberg xbbg.

    Returns
    -------
    df_merged : pandas.DataFrame
        Final cleaned DataFrame with CIP spreads and underlying data.
    """

    start = '2010-01-01'
    if excel:
        # 1) Load from Excel
        filepath = "./data_manual/CIP_2025.xlsx"
        data = pd.read_excel(filepath, sheet_name=None)

        df_spot = data["Spot"]
        exchange_rates = df_spot.set_index("Date")

        df_forward = data["Forward"]
        forward_rates = df_forward.set_index("Date")

        df_ir = data["OIS"]
        interest_rates = df_ir.set_index("Date")
        # Standard columns
        cols = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
        exchange_rates.columns = cols
        forward_rates.columns = cols

        # Convert forward points to forward rates
        # Non-JPY: forward points are per 10,000; JPY: per 100
        forward_rates[[c for c in cols if c != 'JPY']] /= 10000
        forward_rates['JPY'] /= 100
        forward_rates = exchange_rates + forward_rates

        # Rename to keep track
        exchange_rates.columns = [f"{name}_CURNCY" for name in exchange_rates.columns]
        forward_rates.columns = [f"{name}_CURNCY3M" for name in forward_rates.columns]
        interest_rates.columns = [f"{name}_IR" for name in interest_rates.columns]

        # Merge
        df_merged = (
            exchange_rates
            .merge(forward_rates, left_index=True, right_index=True, how='inner')
            .merge(interest_rates, left_index=True, right_index=True, how='inner')
        )

        # Convert to reciprocal for these currencies
        reciprocal_currencies = ['EUR', 'GBP', 'AUD', 'NZD']
        for ccy in reciprocal_currencies:
            df_merged[f"{ccy}_CURNCY"] = 1.0 / df_merged[f"{ccy}_CURNCY"]
            df_merged[f"{ccy}_CURNCY3M"] = 1.0 / df_merged[f"{ccy}_CURNCY3M"]

    else:
        # 2) Pull from Bloomberg
        df_merged = fetch_bloomberg_historical_data(start, end)

    # List of all the core currencies
    currencies = ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'SEK']

    ######################################
    # Compute the log CIP basis in basis points
    ######################################
    for ccy in currencies:
        fwd_col    = f'{ccy}_CURNCY3M'
        spot_col   = f'{ccy}_CURNCY'
        ir_col     = f'{ccy}_IR'
        usd_ir_col = 'USD_IR'  # The US interest rate column

        # CIP in log terms (bps) = 100*100 x [ domestic_i - (logF - logS)*(360/90) - foreign_i ]
        cip_col = f'CIP_{ccy}_ln'
        df_merged[cip_col] = 100*100 * (
            (df_merged[ir_col] / 100.0)               # domestic interest rate
            - (360.0 / 90.0) * (
                np.log(df_merged[fwd_col]) - np.log(df_merged[spot_col])
            )
            - (df_merged[usd_ir_col] / 100.0)         # foreign interest rate (USD)
        )

    ######################################
    # Rolling outlier cleanup (45-day window)
    ######################################
    window_size = 45
    for ccy in currencies:
        cip_col = f'CIP_{ccy}_ln'
        if cip_col not in df_merged.columns:
            continue

        # Rolling median over 45 days
        rolling_median = df_merged[cip_col].rolling(window_size).median()

        # Absolute deviation from median
        abs_dev = (df_merged[cip_col] - rolling_median).abs()

        # Rolling mean of abs_dev (proxy for MAD)
        rolling_mad = abs_dev.rolling(window_size).mean()

        # Mark outliers (abs_dev / mad >= 10) and replace with NaN
        outlier_mask = (abs_dev / rolling_mad) >= 10
        df_merged.loc[outlier_mask, cip_col] = np.nan

    # Create a separate DataFrame for the CIP columns
    cip_cols = [f'CIP_{c}_ln' for c in currencies if f'CIP_{c}_ln' in df_merged.columns]
    spreads = df_merged[cip_cols].copy()

    # Shorten column names for plotting
    spreads.columns = [c[4:7] for c in spreads.columns]  # e.g., CIP_AUD_ln -> AUD





    def plot_spreads(spreads_df, yr):
        """
        Plots the CIP spreads in basis points.
        Saves both a PDF and PNG with the specified yr suffix in the filename.
        """
        fig, ax = plt.subplots(figsize=(13, 8), dpi=300)

        # Plot each column in the DataFrame
        for column in spreads_df.columns:
            ax.plot(spreads_df.index, spreads_df[column], label=column, linewidth=1, antialiased=True)

        ax.set_xlabel("Dates", fontsize=14)
        ax.set_ylabel("Arbitrage Spread (bps)", fontsize=14)

        # Format the x-axis for years
        ax.xaxis.set_major_locator(mdates.YearLocator(2))
        ax.xaxis.set_minor_locator(mdates.YearLocator(1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=0)

        # Horizontal grid lines only
        ax.yaxis.grid(True, linestyle="--", alpha=0.5)
        ax.xaxis.grid(False)

        # Hard limit the y-axis
        ax.set_ylim([-50, 210])

        # Legend below the plot
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=4, fontsize=12, frameon=True)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout(rect=[0, 0.15, 1, 1])  # ensure legend fits

        plt.savefig(f"spread_plot_{yr}.pdf", format="pdf", bbox_inches='tight')
        plt.savefig(f"spread_plot_{yr}.png", dpi=300, bbox_inches='tight')

    # Plot from start to 2019, and the full range
    if isinstance(df_merged.index, pd.DatetimeIndex):
        plot_spreads(spreads.loc[:end], 'rep')




def load_raw(end ='2025-03-01',excel=False, plot = False):
    """
    Reads data from Excel if excel=True, otherwise fetch from Bloomberg using xbbg.

    After retrieving data, calculates a CIP measure and cleans outliers.
    Finally, plots the CIP spreads for a 2010-2019 subset and the full range.

    Parameters
    ----------
    start : str, optional
        Start date in 'YYYY-MM-DD' format, used if excel=False
    end : str, optional
        End date in 'YYYY-MM-DD' format, used if excel=False
    excel : bool, optional
        If True, read from a local Excel file. If False, use Bloomberg xbbg.

    Returns
    -------
    df_merged : pandas.DataFrame
        Final cleaned DataFrame with CIP spreads and underlying data.
    """

    start = '2010-01-01'
    if excel:
        # 1) Load from Excel
        filepath = "./data_manual/CIP_2025.xlsx"
        data = pd.read_excel(filepath, sheet_name=None)

        df_spot = data["Spot"]
        exchange_rates = df_spot.set_index("Date")

        df_forward = data["Forward"]
        forward_rates = df_forward.set_index("Date")

        df_ir = data["OIS"]
        interest_rates = df_ir.set_index("Date")

        # Standard columns
        cols = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
        exchange_rates.columns = cols
        forward_rates.columns = cols

        # Convert forward points to forward rates
        # Non-JPY: forward points are per 10,000; JPY: per 100
        forward_rates[[c for c in cols if c != 'JPY']] /= 10000
        forward_rates['JPY'] /= 100
        forward_rates = exchange_rates + forward_rates

        # Rename to keep track
        exchange_rates.columns = [f"{name}_CURNCY" for name in exchange_rates.columns]
        forward_rates.columns = [f"{name}_CURNCY3M" for name in forward_rates.columns]
        interest_rates.columns = [f"{name}_IR" for name in interest_rates.columns]

        # Merge
        df_merged = (
            exchange_rates
            .merge(forward_rates, left_index=True, right_index=True, how='inner')
            .merge(interest_rates, left_index=True, right_index=True, how='inner')
        )

        # Convert to reciprocal for these currencies
        reciprocal_currencies = ['EUR', 'GBP', 'AUD', 'NZD']
        for ccy in reciprocal_currencies:
            df_merged[f"{ccy}_CURNCY"] = 1.0 / df_merged[f"{ccy}_CURNCY"]
            df_merged[f"{ccy}_CURNCY3M"] = 1.0 / df_merged[f"{ccy}_CURNCY3M"]

    else:
        # 2) Pull from Bloomberg
        df_merged = fetch_bloomberg_historical_data(start, end)

    return df_merged.loc[:end]

def compute_cip(end = '2020-01-01'):
    df_merged = load_raw(end = end, excel=True)

    # List of all the core currencies
    currencies = ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'SEK']

    ######################################
    # Compute the log CIP basis in basis points
    ######################################
    for ccy in currencies:
        fwd_col = f'{ccy}_CURNCY3M'
        spot_col = f'{ccy}_CURNCY'
        ir_col = f'{ccy}_IR'
        usd_ir_col = 'USD_IR'  # The US interest rate column

        # CIP in log terms (bps) = 100*100 x [ domestic_i - (logF - logS)*(360/90) - foreign_i ]
        cip_col = f'CIP_{ccy}_ln'
        df_merged[cip_col] = 100 * 100 * (
                (df_merged[ir_col] / 100.0)  # domestic interest rate
                - (360.0 / 90.0) * (
                        np.log(df_merged[fwd_col]) - np.log(df_merged[spot_col])
                )
                - (df_merged[usd_ir_col] / 100.0)  # foreign interest rate (USD)
        )

    ######################################
    # Rolling outlier cleanup (45-day window)
    ######################################
    window_size = 45
    for ccy in currencies:
        cip_col = f'CIP_{ccy}_ln'
        if cip_col not in df_merged.columns:
            continue

        # Rolling median over 45 days
        rolling_median = df_merged[cip_col].rolling(window_size).median()

        # Absolute deviation from median
        abs_dev = (df_merged[cip_col] - rolling_median).abs()

        # Rolling mean of abs_dev (proxy for MAD)
        rolling_mad = abs_dev.rolling(window_size).mean()

        # Mark outliers (abs_dev / mad >= 10) and replace with NaN
        outlier_mask = (abs_dev / rolling_mad) >= 10
        df_merged.loc[outlier_mask, cip_col] = np.nan

    # Create a separate DataFrame for the CIP columns
    cip_cols = [f'CIP_{c}_ln' for c in currencies if f'CIP_{c}_ln' in df_merged.columns]
    spreads = df_merged[cip_cols].copy()

    # Shorten column names for plotting
    spreads.columns = [c[4:7] for c in spreads.columns]  # e.g., CIP_AUD_ln -> AUD

    return df_merged.iloc[:, -8:]


def load_raw_pieces(end ='2025-03-01',excel=False, plot = False):
    """
    Reads data from Excel if excel=True, otherwise fetch from Bloomberg using xbbg.

    After retrieving data, calculates a CIP measure and cleans outliers.
    Finally, plots the CIP spreads for a 2010-2019 subset and the full range.

    Parameters
    ----------
    start : str, optional
        Start date in 'YYYY-MM-DD' format, used if excel=False
    end : str, optional
        End date in 'YYYY-MM-DD' format, used if excel=False
    excel : bool, optional
        If True, read from a local Excel file. If False, use Bloomberg xbbg.

    Returns
    -------
    df_merged : pandas.DataFrame
        Final cleaned DataFrame with CIP spreads and underlying data.
    """

    start = '2010-01-01'
    if excel:
        # 1) Load from Excel
        filepath = "./data_manual/CIP_2025.xlsx"
        data = pd.read_excel(filepath, sheet_name=None)

        df_spot = data["Spot"]
        exchange_rates = df_spot.set_index("Date")

        df_forward = data["Forward"]
        forward_rates = df_forward.set_index("Date")

        df_ir = data["OIS"]
        interest_rates = df_ir.set_index("Date")

        # Standard columns
        cols = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "SEK"]
        exchange_rates.columns = cols
        forward_rates.columns = cols

        # Convert forward points to forward rates
        # Non-JPY: forward points are per 10,000; JPY: per 100
        forward_rates[[c for c in cols if c != 'JPY']] /= 10000
        forward_rates['JPY'] /= 100
        forward_rates = exchange_rates + forward_rates

        # Rename to keep track
        exchange_rates.columns = [f"{name}_CURNCY" for name in exchange_rates.columns]
        forward_rates.columns = [f"{name}_CURNCY3M" for name in forward_rates.columns]
        interest_rates.columns = [f"{name}_IR" for name in interest_rates.columns]

        # Merge
        df_merged = (
            exchange_rates
            .merge(forward_rates, left_index=True, right_index=True, how='inner')
            .merge(interest_rates, left_index=True, right_index=True, how='inner')
        )

        # Convert to reciprocal for these currencies
        reciprocal_currencies = ['EUR', 'GBP', 'AUD', 'NZD']
        for ccy in reciprocal_currencies:
            df_merged[f"{ccy}_CURNCY"] = 1.0 / df_merged[f"{ccy}_CURNCY"]
            df_merged[f"{ccy}_CURNCY3M"] = 1.0 / df_merged[f"{ccy}_CURNCY3M"]

    else:
        # 2) Pull from Bloomberg
        df_merged = fetch_bloomberg_historical_data(start, end)


    exchange_rates_df = df_merged.iloc[:,:8]
    forward_rates_df = df_merged.iloc[:, 8:16]
    interest_rates_df = df_merged.iloc[:, -9:]

    return exchange_rates_df, forward_rates_df, interest_rates_df
