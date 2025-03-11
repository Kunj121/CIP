## Description

This dataframe contains data on foreign exchange rates and interest rates used for Covered Interest Parity (CIP) analysis. The dataset includes spot exchange rates, 3-month forward exchange rates, and interest rates for major currency pairs against the US dollar. CIP deviations (or the "cross-currency basis") are calculated as the difference between the implied dollar interest rate from FX swaps and the direct dollar interest rate, providing a measure of market frictions in international currency markets.

## Data Dictionary

### Spot Exchange Rates (vs USD)
- **AUD_CURNCY**: `float64` Australian Dollar spot exchange rate
- **CAD_CURNCY**: `float64` Canadian Dollar spot exchange rate
- **CHF_CURNCY**: `float64` Swiss Franc spot exchange rate
- **EUR_CURNCY**: `float64` Euro spot exchange rate
- **GBP_CURNCY**: `float64` British Pound spot exchange rate
- **JPY_CURNCY**: `float64` Japanese Yen spot exchange rate
- **NZD_CURNCY**: `float64` New Zealand Dollar spot exchange rate
- **SEK_CURNCY**: `float64` Swedish Krona spot exchange rate

### 3-Month Forward Exchange Rates (vs USD)
- **AUD_CURNCY3M**: `float64` Australian Dollar 3-month forward rate
- **CAD_CURNCY3M**: `float64` Canadian Dollar 3-month forward rate
- **CHF_CURNCY3M**: `float64` Swiss Franc 3-month forward rate
- **EUR_CURNCY3M**: `float64` Euro 3-month forward rate
- **GBP_CURNCY3M**: `float64` British Pound 3-month forward rate
- **JPY_CURNCY3M**: `float64` Japanese Yen 3-month forward rate
- **NZD_CURNCY3M**: `float64` New Zealand Dollar 3-month forward rate
- **SEK_CURNCY3M**: `float64` Swedish Krona 3-month forward rate

### 3-Month Interest Rates
- **AUD_IR**: `float64` Australian Dollar 3-month interest rate
- **CAD_IR**: `float64` Canadian Dollar 3-month interest rate
- **CHF_IR**: `float64` Swiss Franc 3-month interest rate
- **EUR_IR**: `float64` Euro 3-month interest rate
- **GBP_IR**: `float64` British Pound 3-month interest rate
- **JPY_IR**: `float64` Japanese Yen 3-month interest rate
- **NZD_IR**: `float64` New Zealand Dollar 3-month interest rate
- **SEK_IR**: `float64` Swedish Krona 3-month interest rate
- **USD_IR**: `float64` US Dollar 3-month interest rate




## Key Formulas

1. **CIP Deviation Calculation**:
   ```
   CIP_deviation = (F/S)*(1+r_d) - (1+r_f)
   ```
   Where:
   - F is the forward exchange rate
   - S is the spot exchange rate
   - r_d is the foreign currency interest rate
   - r_f is the USD interest rate

2. **Annualized CIP Basis (in basis points)**:
   ```
   CIP_basis_bp = CIP_deviation * 10000
   ```

## Data Sources

- Exchange rates (spot and forward): Bloomberg
- Interest rates: Bloomberg


## Notes on Interpretation

- Negative CIP deviations indicate that borrowing USD directly is more expensive than borrowing in the foreign currency and swapping into USD
- Larger absolute deviations indicate greater market frictions or funding pressures
- CIP deviations typically widen during periods of financial stress, at quarter/year-ends due to regulatory reporting requirements, and when intermediary balance sheet constraints are binding
- Post-2008 financial crisis, persistent non-zero CIP deviations have become the norm, contradicting the traditional CIP theory that predicts zero deviations in efficient markets