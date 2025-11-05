"""
Run OU Strategy Backtest on Real Market Data
By Josephina Kim (JK)

This script fetches real market data and runs the OU strategy backtest.
"""

from polygon_data import PolygonDataFetcher
from trading_strategy import MeanReversionStrategy
from ou_estimator import OUEstimator
import numpy as np


def run_backtest(ticker="AAPL", days=500, threshold_sigma=1.5, stop_loss_pct=0.20, exit_at_mean=True):
    """
    Run OU strategy backtest on real market data.
    
    Parameters to tweak:
    - ticker: Stock/crypto symbol (e.g., "AAPL", "MSFT", "X:BTCUSD")
    - days: Number of days of historical data to fetch
    - threshold_sigma: Signal threshold (2.0 = 2 standard deviations)
    
    Returns:
    - prices: Price data
    - strategy: Fitted strategy
    - backtest_results: Backtest performance metrics
    """
    api_key = "phX3UGTSILWy8uHUdxQauDRZF578YwRL"
    fetcher = PolygonDataFetcher(api_key)
    
    print("="*70)
    print(f"OU STRATEGY BACKTEST - {ticker}")
    print("="*70)
    print()
    
    try:
        # Fetch data
        print(f"Fetching {ticker} data ({days} days)...")
        if ticker.startswith("X:"):
            prices = fetcher.get_crypto_data(ticker, days=days)
        else:
            prices = fetcher.get_stock_data(ticker, days=days)
        
        print(f"✓ Fetched {len(prices)} data points")
        print(f"  Price range: ${prices.min():.2f} - ${prices.max():.2f}")
        print(f"  Mean price: ${prices.mean():.2f}")
        print()
        
        # Estimate OU parameters
        print("Estimating OU parameters...")
        strategy = MeanReversionStrategy(threshold_sigma=threshold_sigma)
        strategy.fit(prices, dt=1.0)
        
        params = strategy.get_parameters()
        print(f"  θ (mean reversion speed): {params['theta']:.4f}")
        print(f"  μ (long-term mean): ${params['mu']:.2f}")
        print(f"  σ (volatility): ${params['sigma']:.2f}")
        print(f"  Half-life: {params['half_life']:.2f} days")
        print()
        
        # Run backtest
        print("Running backtest...")
        backtest_results = strategy.backtest(prices, dt=1.0, allow_short=True, exit_at_mean=True)
        
        print(f"  Total return: {backtest_results['total_return']*100:.2f}%")
        print(f"  Sharpe ratio: {backtest_results['sharpe_ratio']:.4f}")
        print(f"  Max drawdown: {backtest_results['max_drawdown']*100:.2f}%")
        print()
        
        # Current signal
        current_price = prices[-1]
        signal, signal_type = strategy.generate_signal(current_price)
        deviation = current_price - params['mu']
        stationary_std = np.sqrt(params['stationary_variance'])
        z_score = deviation / stationary_std
        
        print("Current Signal:")
        print(f"  Current price: ${current_price:.2f}")
        print(f"  Mean: ${params['mu']:.2f}")
        print(f"  Deviation: ${deviation:+.2f}")
        print(f"  Z-score: {z_score:.2f}")
        print(f"  Signal: {signal_type}")
        print()
        
        print("="*70)
        print("BACKTEST COMPLETE")
        print("="*70)
        
        return prices, strategy, backtest_results
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


if __name__ == "__main__":
    # Change these parameters to test different assets
    TICKER = "VIXY"           # Stock ticker or crypto (e.g., "AAPL", "MSFT", "X:BTCUSD")
    DAYS = 500                # Number of days of historical data
    THRESHOLD_SIGMA = 2.0      # Signal threshold (2.0 = 2 standard deviations)
    
    run_backtest(TICKER, DAYS, THRESHOLD_SIGMA)
