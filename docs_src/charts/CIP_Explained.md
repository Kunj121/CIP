**Description:** This chart plots CIP deviations over time for major currency pairs against the US dollar. It measures the difference between the implied dollar interest rate from foreign exchange swaps and the direct dollar interest rate in money markets. The CIP deviation (or "basis") quantifies arbitrage opportunities in international financial markets that persist due to balance sheet constraints and regulatory factors.

**Relevance for Financial Stability:** CIP deviations reflect funding stresses in global dollar markets and indicate potential constraints on financial intermediaries' ability to arbitrage across markets. Persistent or widening deviations may signal growing stress in the international monetary system and reduced market functioning.

**Direction of Risk:** When CIP deviations widen (become more negative), risk in financial markets is typically higher. Larger absolute deviations indicate greater market dysfunction and potential stress in dollar funding markets. Sudden spikes in CIP deviations often coincide with periods of market turmoil.

**Formulas Used:** CIP Deviation = (F/S) × (1 + r_d) - (1 + r_f)
Where F is the forward rate, S is the spot rate, r_d is the domestic interest rate, and r_f is the foreign interest rate.

**Data Cleaning Information:** The data combines information from multiple sources including Bloomberg terminal data on FX spot and forward rates and Refinitiv data on interest rates. Maturity matching and day count convention adjustments are performed to ensure accurate CIP calculations.

**What does this add that other charts might not?** It provides a window into international financial conditions and dollar funding pressures that might not be apparent in domestic U.S. financial metrics. CIP deviations serve as an early warning indicator for stresses in the global financial system, often widening before other market stress indicators. The visualization of deviations across multiple currency pairs helps identify whether stress is currency-specific or systematic across global markets.