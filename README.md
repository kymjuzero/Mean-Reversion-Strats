# Ornstein-Uhlenbeck Process - Mean Reversion Trading Strategy

**By Josephina Kim (JK)** 🚀

Complete implementation of the Ornstein-Uhlenbeck (OU) process for mean reversion trading with parameter estimation and trading signal generation. Built following the methodology from [QuestDB's OU Process Guide](https://questdb.com/glossary/ornstein-uhlenbeck-process-for-mean-reversion/).

*AKA Josephina's god strategy LOL* 😎

## What's This About?

So basically, I built this OU process model for mean reversion trading. The whole idea is that when prices stray away from their mean, they tend to revert back (hence "mean reversion" - pretty clever name right? lol). 

The main focus was on figuring out how to estimate the OU parameters (θ, μ, σ) from real data. Once we have those, we can generate trading signals:
- **Price goes ABOVE mean** → SELL signal (it's gonna drop back, trust me)
- **Price goes BELOW mean** → BUY signal (it's gonna bounce back up)
- **Price near mean** → HOLD (nothing exciting happening here)

Pretty straightforward strategy, but the math behind it is actually pretty cool ngl.

## Overview

The OU process models mean-reverting behavior using this equation:

```
dX_t = θ(μ - X_t)dt + σdW_t
```

Where:
- **θ** (theta): How fast it reverts to mean (mean reversion speed)
- **μ** (mu): The long-term mean level (where prices want to hang out)
- **σ** (sigma): Volatility (how random/chaotic things get)
- **dW_t**: Random noise (Brownian motion - basically randomness)

## Strategy Logic

The trading signals are based on deviations from the mean using **stationary variance**:

- **SELL Signal**: When price > μ + k × σ_stationary (expect reversion down)
- **BUY Signal**: When price < μ - k × σ_stationary (expect reversion up)  
- **HOLD Signal**: When price is within ±k × σ_stationary threshold

Where:
- σ_stationary = √(σ² / (2θ)) - the long-term standard deviation around the mean
- k = threshold multiplier (I set it to 2.0, but you can tweak it)

## Files

- `ou_estimator.py`: Parameter estimation (MLE, regression, OLS methods)
- `ou_process.py`: OU process simulation (the actual model)
- `trading_strategy.py`: Trading strategy with signal generation
- `demo.py`: Complete demo - **run this to see everything!**
- `parameter_analysis.py`: Detailed parameter estimation with step-by-step calculations
- `DERIVATION.md`: Complete mathematical derivation (if you're into that stuff)

## Installation

Super easy setup:

```bash
pip install -r requirements.txt
```

That's it! Just make sure you have Python 3.7+ installed.

## Usage

### Run the Complete Demo (Recommended)

```bash
python3 demo.py
```

This will:
1. Generate synthetic OU process data (500 data points)
2. Show detailed parameter estimation with step-by-step calculations (this is the main focus!)
3. Compare different estimation methods (MLE, Regression, OLS)
4. Build the trading strategy
5. Generate trading signals with examples
6. Run a backtest to see how it performs
7. Create a sick visualization saved to `ou_analysis.png`

### Run Parameter Analysis Only

If you just want to see the parameter estimation stuff:

```bash
python3 parameter_analysis.py
```

This shows the step-by-step calculations for how we estimate θ, μ, and σ. Pretty neat to see all the intermediate values!

## Parameter Estimation Strategy (The Main Focus!)

This is where the magic happens. The QuestDB methodology is actually pretty clean:

### 1. Theta (θ) - Mean Reversion Speed

**Formula**: θ = -ln(ρ) / Δt

Where ρ is the lag-1 autocorrelation:
- ρ = Corr(X_t, X_{t+1}) - basically how correlated each point is with the next one
- Higher θ = faster mean reversion (prices bounce back quicker)

**How it works**: We calculate the autocorrelation, then use that to figure out θ. The math checks out, I promise lol.

### 2. Mu (μ) - Long-term Mean

**Formula**: μ = (1/n) Σ X_i

Just the sample mean of the data. Nothing fancy here - just take the average. Easy peasy.

### 3. Sigma (σ) - Volatility

**Formula**: σ² = (2θ / [n(1-e^(-2θΔt))]) Σ [X_{i+1} - X_i - μ(1-e^(-θΔt))]²

This one's a bit more involved, but it's the Maximum Likelihood Estimator. The formula looks scary but it's just calculating the variance of the residuals in a clever way.

## Parameter Estimation Methods

I implemented three different methods so you can compare:

1. **Maximum Likelihood Estimation (MLE)**: Uses autocorrelation and closed-form formulas (this is what QuestDB recommends)
2. **Regression Method**: Linear regression on lagged data (simple and intuitive)
3. **Ordinary Least Squares (OLS)**: Direct OLS estimation on the discretized SDE (alternative approach)

The demo shows comparisons between all three, which is pretty useful for understanding which method works best for your data.

## Trading Signal Generation

### Stationary Variance Approach

The strategy uses **stationary variance** for signal generation (as recommended by QuestDB):

```
σ_stationary = √(σ² / (2θ))
z = (X_t - μ) / σ_stationary
```

### Signal Rules

- **SELL**: z > 2.0 (price above mean, expect downward reversion)
- **BUY**: z < -2.0 (price below mean, expect upward reversion)
- **HOLD**: -2.0 ≤ z ≤ 2.0 (price near mean, no strong signal)

The z-score basically tells us how many standard deviations away from the mean we are. If it's way above (like >2σ), we expect it to drop. If it's way below (<-2σ), we expect it to bounce back up. Simple but effective!

## Key Features

- ✅ Exact QuestDB methodology implementation (follows the article to a T)
- ✅ Multiple parameter estimation methods with detailed comparison
- ✅ Step-by-step parameter estimation calculations (shows ALL the math)
- ✅ Trading signal generation using stationary variance
- ✅ Position sizing based on deviation
- ✅ Stop-loss calculation using stationary variance
- ✅ Comprehensive backtesting framework
- ✅ Detailed visualizations (6-panel analysis - looks pretty cool)
- ✅ Complete mathematical derivation documentation

## Example Output

When you run `demo.py`, you'll see:

1. **Parameter Estimation Analysis**:
   - Autocorrelation analysis
   - Step-by-step theta calculation (shows the formula and intermediate values)
   - Mu estimation (simple mean calculation)
   - Detailed sigma calculation with all intermediate values
   - Stationary distribution properties

2. **Estimation Method Comparison**:
   - Side-by-side comparison of MLE, Regression, OLS
   - Error analysis against true parameters (so you can see how accurate each is)

3. **Trading Signal Examples**:
   - Sample signals at different price levels
   - Shows the z-score calculations
   - Demonstrates the deviation from mean

4. **Visualizations** (saved to `ou_analysis.png`):
   - Price series with mean levels
   - Trading signals overlay with thresholds
   - Deviation analysis
   - Z-score visualization
   - Backtest performance
   - Autocorrelation function (confirms mean-reverting behavior)

## Mathematical Properties

### Half-Life

Expected time to revert halfway to mean:
```
t_{1/2} = ln(2) / θ
```

This tells you how long it takes for the process to get halfway back to the mean. Useful for understanding the speed of mean reversion!

### Stationary Variance

Long-term variance around the mean:
```
Var_stationary = σ² / (2θ)
```

This is used for signal generation because it represents the long-term distribution of the process. Basically, it's the "typical" deviation from the mean over long periods.

## Documentation

Check out `DERIVATION.md` for the complete mathematical derivation if you want to understand all the formulas in detail. It's got all the math explained step-by-step.

## Quick Start

1. Install: `pip install -r requirements.txt`
2. Run: `python3 demo.py`
3. Profit? (Just kidding, this is for educational purposes lol)

## Troubleshooting

**"ModuleNotFoundError"**: Run `pip install -r requirements.txt`

**"python3: command not found"**: Try `python demo.py` instead

**Visualization not showing**: Check that `ou_analysis.png` was created in the same directory

## Final Notes

This was a fun project to build! The parameter estimation strategy was the main challenge, but once you understand the math, it all clicks together. The trading signals are pretty straightforward - above mean = sell, below mean = buy. Classic mean reversion strategy.

Hope this helps with your presentation! The code is ready to run and demonstrate. Just fire up `python3 demo.py` and you're good to go.

- Josephina Kim (JK) 🚀
