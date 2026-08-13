# Shadow Broker Apex Engine

### Walk-Forward Machine Learning Algorithmic Trading System for Indian Equities

**Python | Pandas | NumPy | Scikit-learn | yFinance | Flask | AWS/Render | Telegram**

---

## 1. Project Overview

**Shadow Broker Apex Engine** is an automated quantitative paper-trading system designed for the Indian equity market (NSE).

The system combines:

- Technical pattern recognition
- Time-series feature engineering
- Supervised machine learning
- Market-regime filtering
- Volatility-adjusted risk management
- Dynamic position sizing
- Automated market scanning
- Telegram-based trade alerts
- Cloud deployment

The core objective is not to predict every market movement. Instead, the system attempts to identify a specific type of bullish momentum setup and use a machine-learning model to filter those setups based on their historical probability of reaching a predefined profit target.

The strategy operates on a broad universe of NSE equities and uses the Nifty 50 as a macro-level market filter.

---

# 2. System Architecture

```text
                    HISTORICAL MARKET DATA
                             │
                             ▼
                    Data Ingestion Layer
                     (yFinance / OHLCV)
                             │
                             ▼
                  Technical Feature Engine
                             │
              ┌──────────────┼──────────────┐
              │              │              │
             RSI             ATR        Volume Ratio
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                    Technical Setup Filter
                 EMA Trend + Pullback + Cross
                             │
                             ▼
                     Feature Vector
          [RSI, Volume Ratio, EMA Distance, ATR %]
                             │
                             ▼
                    StandardScaler
                             │
                             ▼
                 Random Forest Classifier
                             │
                             ▼
                AI Probability >= 62% ?
                       │           │
                      NO          YES
                       │           │
                     REJECT        ▼
                             Macro Regime Filter
                              Nifty > 200 EMA
                                  │
                                  ▼
                         Risk Management Engine
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              Stop-Loss Logic            Position Sizing
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                            Trade Signal
                                  │
                                  ▼
                         Telegram Alert /
                          Paper Execution
```

---

# 3. Trading Universe

The system was tested across a broad universe of **302 NSE equities** covering:

- Nifty 50
- Nifty Next 50
- Mid-cap equities
- Small-cap equities

During the backtest, **299 of the 302 securities successfully returned usable historical data**.

Three symbols were skipped because of Yahoo Finance data availability issues:

- ZOMATO.NS
- GUJGASLTD.NS
- AKZOINDIA.NS

These are data-provider issues rather than strategy-level failures.

The backtest log confirms that 299/302 securities were successfully loaded.

---

# 4. Strategy Logic

The strategy is built around a bullish pullback-and-recovery setup.

## 4.1 Trend Filter

Three exponential moving averages are calculated:

- **13 EMA** — short-term momentum
- **34 EMA** — intermediate trend
- **100 EMA** — primary trend baseline

A setup is considered structurally bullish when:

```text
Close > EMA(100)
AND
EMA(34) > EMA(100)
```

This prevents the model from evaluating setups that occur inside an established longer-term downtrend.

---

# 5. Pullback + Crossover Trigger

The system then looks for evidence that the stock recently pulled back below the fast EMA and has now recovered.

The setup requires:

```text
Previous Close < Previous 13 EMA
AND
Current Close >= Current 13 EMA
```

with an additional recent-pullback condition.

Conceptually:

```text
Uptrend
   ↓
Price pulls below 13 EMA
   ↓
Price recovers
   ↓
Price crosses back above 13 EMA
   ↓
Candidate setup
```

This is important because the machine-learning model is **not scanning every daily bar indiscriminately**.

The technical strategy first identifies a particular market structure. The ML model then acts as a **probability filter** on those candidate setups.

---

# 6. Feature Engineering

For every candidate setup, four primary features are generated.

## RSI

**14-period Relative Strength Index**

Used as a momentum-state variable.

```text
F_RSI = RSI(14)
```

It helps distinguish weak, neutral, and strongly positive momentum conditions.

---

## Volume Ratio

Current volume is normalized against its 20-day average:

```text
F_Vol_Ratio = Current Volume / 20-Day Average Volume
```

A value above 1 indicates above-average trading activity.

This provides the model with information about whether the price move is occurring with relatively strong participation.

---

## Distance From Fast EMA

The normalized distance between price and the 13 EMA:

```text
F_Distance_EMA =
(Close - EMA13) / Close
```

This describes how extended the price is relative to the trigger level.

---

## ATR Percentage

ATR is normalized by stock price:

```text
F_ATR_Pct = ATR(14) / Close
```

This allows the model to distinguish low-volatility and high-volatility securities without relying solely on absolute rupee values.

---

# 7. Machine Learning Model

The model is a:

```text
RandomForestClassifier
```

Configuration:

```text
Number of trees = 100
Maximum depth = 5
Class weighting = balanced
Random state = 42
```

The relatively shallow tree depth is intended to control model complexity and reduce the risk of overfitting.

Before training, the four features are standardized using:

```text
StandardScaler
```

---

# 8. ML Target Definition

The model solves a binary classification problem:

> Given that a technical setup has occurred, does the stock reach at least +6% within the following 15 trading days?

The target is defined as:

```text
Target = 1
if future 15-day High >= Entry Close × 1.06

Target = 0
otherwise
```

Therefore:

```text
Prediction = Probability that the setup reaches +6%
```

The live trading engine only accepts predictions where:

```text
AI Probability >= 62%
```

This threshold is intentionally selective: the model is used as a **trade filter**, rather than generating a trade for every technical setup.

---

# 9. Walk-Forward Backtesting

A major part of this project is the attempt to avoid look-ahead bias.

A naïve backtest could train the model on the entire 2019–2024 dataset and then evaluate trades using information that would not have been available historically.

This implementation instead uses a **walk-forward process**.

Conceptually:

```text
Historical Data
      │
      ▼
Train model using information available
before the current test period
      │
      ▼
Generate current-period predictions
      │
      ▼
Advance through time
      │
      ▼
Retrain model periodically
      │
      ▼
Continue testing
```

The model was retrained approximately every **21 calendar days** during the test period.

The number of historical training setups therefore increases through time.

Examples from the backtest:

```text
Jan 2022   →  8,854 training setups
Jan 2023   → 11,125 training setups
Jan 2024   → 14,427 training setups
Dec 2024   → 18,351 training setups
```

This means the model continuously incorporates newly available historical observations rather than remaining fixed for the entire three-year test.

---

# 10. Avoiding Future Information During Training

There is an important timing issue with the target.

A setup occurring today cannot be labeled immediately because its target depends on the next 15 trading days.

Therefore, the backtester excludes the most recent historical setups whose 15-day outcome would not yet have been known.

This prevents the model from being trained on incomplete future labels.

---

# 11. Signal Execution Assumption

The backtester does **not** enter a position at the same closing price that generated the signal.

Instead:

```text
Day T
Signal generated using completed OHLCV data

        ↓

Day T+1
Trade entered at opening price
```

This is a more conservative and realistic assumption than using the signal day's closing price.

Transaction costs and slippage are also incorporated into the backtester.

---

# 12. Macro Market-Regime Filter

Before individual stock signals are considered, the system checks the Nifty 50.

The rule is:

```text
Nifty Close > Nifty 200 EMA
        ↓
Market regime = bullish
```

If:

```text
Nifty Close < Nifty 200 EMA
```

the strategy does not generate new long positions.

This acts as a **system-level safety lock**.

The rationale is straightforward:

> A stock-level bullish setup has a lower priority when the broader market is structurally weak.

---

# 13. Dynamic Risk Management

Initial portfolio capital:

```text
₹36,000
```

Maximum risk per trade:

```text
4%
```

Therefore:

```text
Maximum planned risk = ₹36,000 × 4%
                    = ₹1,440
```

The system does not use a fixed number of shares for every stock.

Instead, position size adapts to the stock's volatility and stop distance.

---

# 14. ATR-Based Stop Loss

The stop-loss distance is derived from the current price, today's low, and ATR:

```text
Risk Per Share =
max(
    Close - (Low - 0.3 × ATR),
    Close × 0.005
)
```

This means a highly volatile stock receives a wider stop and therefore a smaller position.

A lower-volatility stock can receive a tighter stop and therefore a larger position, subject to the capital constraints.

This creates a **risk-normalized position sizing framework**.

---

# 15. Position Sizing

The theoretical position size is:

```text
Quantity =
floor(Max Risk / Risk Per Share)
```

The system also imposes a second constraint:

```text
Maximum position value = 50% of initial capital
```

For ₹36,000:

```text
Maximum position value = ₹18,000
```

Therefore the final quantity is the minimum of:

```text
Risk-based quantity
Capital-based quantity
Available cash quantity
```

---

# 16. Portfolio-Level Controls

The backtester also imposes portfolio constraints:

```text
Maximum simultaneous positions = 6

Maximum account heat = 15%
```

Account heat represents the aggregate predefined risk of currently open positions relative to the initial portfolio.

This prevents the system from taking a large number of individually acceptable trades that collectively create excessive portfolio risk.

---

# 17. Exit Logic

Each trade has two primary exit conditions.

### Target

```text
Target = Entry × 1.06
```

Equivalent to:

```text
+6%
```

### Stop Loss

Determined dynamically using the ATR-based risk calculation.

If both the stop and target are theoretically touched on the same daily candle, the backtester assumes the **stop was hit first**.

This is deliberately conservative because daily OHLC data does not reveal the exact intraday sequence of prices.

---

# 18. Backtest Period

The model uses historical data beginning in:

```text
2019
```

The out-of-sample test period begins:

```text
January 2022
```

and runs through:

```text
December 2024
```

The resulting test therefore covers approximately three years of historical market behavior.

---

# 19. Backtest Results

The completed run produced:

| Metric | Result |
|---|---:|
| Initial Capital | ₹36,000 |
| Final Equity | ₹56,044.08 |
| Total Return | **55.68%** |
| CAGR | **15.96%** |
| Maximum Drawdown | **-38.13%** |
| Number of Trades | **246** |
| Win Rate | **60.16%** |
| Profit Factor | **1.29** |
| Average Winning Trade | ₹600.97 |
| Average Losing Trade | -₹703.20 |

---

# 20. What These Results Actually Mean

## 20.1 Total Return: +55.68%

The initial ₹36,000 grew to approximately:

```text
₹56,044
```

The absolute increase was approximately:

```text
₹20,044
```

over the test period.

This indicates that the strategy generated positive cumulative returns under the backtest assumptions.

---

## 20.2 CAGR: 15.96%

CAGR is the annualized compound growth rate.

It answers:

> What constant annual growth rate would transform ₹36,000 into ₹56,044 over the test period?

The answer is approximately:

```text
15.96% per year
```

CAGR is more useful than simply reporting total return because the test spans multiple years.

---

# 21. The Most Important Result: Maximum Drawdown

Maximum drawdown was:

```text
-38.13%
```

This is a significant risk characteristic.

It means the portfolio experienced a peak-to-trough decline of approximately 38% at its worst point during the backtest.

For example, conceptually:

```text
Portfolio Peak
      │
      ▼
   ₹X
      │
      │  -38.13%
      ▼
Trough
```

This is why the project should **not** be presented as:

> "A highly profitable AI trading system."

A more technically honest conclusion is:

> "A positive-return ML-filtered trading strategy with meaningful drawdown and moderate trading efficiency."

The 38.13% drawdown is actually an important finding because it identifies a major area for future optimization.

---

# 22. Win Rate: 60.16%

Out of 246 completed trades, approximately 60% were profitable.

That is:

```text
Winning trades ≈ 148
Losing trades ≈ 98
```

The exact counts can be obtained from the exported trade log.

A win rate above 50% is useful, but **win rate alone does not determine profitability**.

---

# 23. Profit Factor: 1.29

Profit Factor is:

```text
Gross Profit / Gross Loss
```

A value of:

```text
1.29
```

means that for approximately every ₹1.00 of gross loss, the system generated ₹1.29 of gross profit.

This is a more informative statistic than win rate alone.

However, 1.29 is not exceptionally high. It indicates a positive trading edge in the backtest, but not an extremely strong one.

---

# 24. Average Winner vs Average Loser

Average winning trade:

```text
+₹600.97
```

Average losing trade:

```text
-₹703.20
```

Therefore, the average losing trade is larger than the average winning trade.

This means the strategy's positive expectancy relies significantly on its relatively high win rate.

The system is approximately:

```text
Higher win probability
+
Controlled losses
+
Frequent enough successful targets
=
Positive expectancy
```

This is a very important characteristic to understand during an interview.

---

# 25. Why the Strategy Can Make Money Despite Larger Average Losses

The expected value of a trade can be approximated as:

```text
Expectancy =
Win Rate × Average Win
-
Loss Rate × Average Loss
```

Using the reported statistics:

```text
≈ 0.6016 × ₹600.97
  -
  0.3984 × ₹703.20
```

which is approximately:

```text
+₹81 per trade
```

before considering any differences between the reported summary metrics and exact trade-level rounding.

This is consistent with the positive profit factor and positive total return.

---

# 26. Why the ML Model Matters

The Random Forest does not replace the trading strategy.

Instead:

```text
Technical Setup
       ↓
Candidate Trade
       ↓
ML Probability Filter
       ↓
Only high-confidence setups continue
       ↓
Risk Management
       ↓
Trade
```

This architecture separates:

### Strategy generation

"What market structure do we want?"

from:

### Statistical filtering

"Based on historical examples, how likely is this setup to reach the target?"

from:

### Risk management

"How much capital should we risk if we take it?"

This separation is one of the strongest architectural aspects of the project.

---

# 27. Why Random Forest?

Random Forest was selected because it:

- Handles nonlinear relationships
- Captures interactions between technical features
- Requires relatively little preprocessing
- Is robust for small-to-medium feature sets
- Provides probability estimates
- Allows feature-importance analysis

The model uses only four primary features, deliberately keeping the feature space relatively compact.

---

# 28. Cloud / Automation Architecture

The original live engine also contains an operational layer.

```text
Python Scheduler
       │
       ▼
Periodic Market Scan
       │
       ▼
NSE Data
       │
       ▼
Strategy + ML
       │
       ▼
Risk Engine
       │
       ▼
Telegram Bot API
```

A Flask micro-server runs in a separate thread to provide a health-check endpoint for cloud deployment environments.

The application can therefore run as a continuously operating service rather than requiring manual execution for every scan.

---

# 29. Technologies Used

### Programming

- Python 3.10+
- Object-oriented / modular Python design
- NumPy
- Pandas

### Machine Learning

- Scikit-learn
- Random Forest
- StandardScaler

### Market Data

- yFinance
- NSE equity OHLCV data

### Automation

- Python `schedule`
- `threading`
- `requests`

### Deployment

- Flask
- Linux
- AWS EC2
- Render

### Communication

- Telegram Bot API

---

# 30. Project Structure

```text
shadow-broker-apex-engine/
│
├── main.py
├── shadow_broker_backtest.py
├── requirements.txt
├── README.md
│
├── results/
│   ├── trade_log.csv
│   ├── equity_curve.csv
│   ├── performance_summary.csv
│   ├── equity_curve.png
│   └── drawdown.png
│
└── screenshots/
    ├── telegram-alert.png
    ├── model-output.png
    └── deployment.png
```

---

# 31. Limitations

This is a research backtest and should not be interpreted as proof of future profitability.

Important limitations include:

### Survivorship Bias

The stock universe is based on a selected current/curated universe rather than a historically reconstructed list of every stock that belonged to the relevant indices at each point in time.

### Data Provider Dependency

Historical data comes from Yahoo Finance through `yfinance`. Three securities failed during this run because historical data was unavailable.

### Daily Data Resolution

The backtest uses daily OHLC data.

If both the stop and target occur during the same candle, the exact intraday order cannot be known. The backtester therefore assumes the stop occurred first.

### Transaction Cost Assumptions

Commission and slippage are modeled assumptions rather than a complete broker-specific execution simulation.

### Model Calibration

The 62% probability threshold and strategy parameters are model choices and should be subjected to further out-of-sample validation.

### No Fundamental Data

The model currently uses price, volatility, momentum, and volume information rather than company fundamentals.

---

# 32. Future Improvements

Potential next steps include:

1. Reconstructing a historical point-in-time stock universe.
2. Adding Nifty/sector-relative strength features.
3. Testing multiple probability thresholds.
4. Performing hyperparameter optimization with nested walk-forward validation.
5. Adding transaction-cost sensitivity analysis.
6. Comparing against Nifty 50 buy-and-hold.
7. Adding Sharpe and Sortino ratios.
8. Performing Monte Carlo trade-sequence analysis.
9. Testing different market-regime definitions.
10. Evaluating feature importance and permutation importance.
11. Adding sector exposure constraints.
12. Testing alternative models such as XGBoost or logistic regression.
13. Running a completely untouched final holdout period.

---

# 33. Key Takeaway

The backtest produced a **55.68% cumulative return and 15.96% CAGR** from ₹36,000 over the tested period, across 246 trades.

However, the strategy also experienced a **38.13% maximum drawdown** and a **1.29 profit factor**.

Therefore, the main conclusion is not simply that the model was profitable.

The more meaningful conclusion is:

> **The combination of technical setup detection, supervised ML filtering, macro-regime control, and volatility-adjusted risk management produced a positive historical trading edge, while the substantial drawdown demonstrates that further portfolio-level risk optimization is necessary.**

That trade-off is central to the project's quantitative analysis and is an important topic for further research.

---

## Disclaimer

This project is for educational and research purposes only.

Backtested performance does not guarantee future results. Historical simulations contain modeling assumptions and may differ materially from live execution due to liquidity, slippage, market impact, data quality, and changing market regimes.

No investment recommendation is being made.
