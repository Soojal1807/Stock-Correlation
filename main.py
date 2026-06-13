import os
import numpy as np
from data import fetch_prices, compute_log_returns
from matrix import compute_covariance, compute_correlation
from visualize import plot_correlation_heatmap, plot_cumulative_returns, plot_volatility_bar

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)



#printing Function
def printSummary(returns, cov, corr):
    print("\n── Log Return Summary (daily) ─────────────────────")
    print(f"  Observations : {len(returns)} trading days")
    print(f"  Assets       : {list(returns.columns)}\n")


    print("  Mean daily return:")
    for col in returns.columns:
        print(f"    {col:<6}  {returns[col].mean()*100:+.4f}%")


    print("\n  Annualised volatility:")
    for col in returns.columns:
        print(f"    {col:<6}  {returns[col].std() * (252**0.5) * 100:.2f}%")


    print("\n── Correlation Matrix ─────────────────────────────")
    print(corr.round(3).to_string())



    print("\n── Strongest Pairs ────────────────────────────────")
    pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            pairs.append((cols[i], cols[j], corr.iloc[i, j]))
    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    for a, b, r in pairs:
        print(f"    {a:<6} — {b:<6}  ρ = {r:.3f}")




#main function to recall all above functions
def main():
    print("Fetching price data...")
    prices = fetch_prices(days=500)
    returns = compute_log_returns(prices)

    cov  = compute_covariance(returns)
    corr = compute_correlation(cov)

    printSummary(returns, cov, corr)

    print("\nGenerating charts...")
    plot_correlation_heatmap(corr,  save_path=f"{OUT}/correlation_heatmap.png")
    plot_cumulative_returns(returns, save_path=f"{OUT}/cumulative_returns.png")
    plot_volatility_bar(returns,     save_path=f"{OUT}/volatility.png")
    print(f"Saved to {OUT}/")

if __name__ == "__main__":
    main()
