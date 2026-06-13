# Stock Correlation

An equity return analysis tool that computes and visualises the
correlation structure of a stock universe using linear algebra.

Stocks analysed: **NVDA, GOOGL, AMD, META, NFLX** — last 500 trading days.

---

## Project Structure

```
stock Correlation/
├── data.py        # price fetching using yfinance and log return compute
├── matrix.py      # covariance and correlation matrix 
├── visualize.py   # heatmap, cumulative returns, volatility bar chart
├── main.py        # runs the fullpipeline
├── output/        # charts are saved here
└── README.md
```

---

## How to Run

```bash
pip install yfinance numpy pandas matplotlib seaborn
python main.py
```

Charts are saved to `output/`.

---

## Mathematical Foundation

### 1. Price Data

Raw closing prices are collected for N assets over T trading days,
forming a price matrix:

```
P ∈ ℝ^(T × N)
```

Prices are not stationary (they trend and drift), so they are converted
to returns before any analysis.

---

### 2. Log Returns

For each asset i and each day t, the log return is:

```
r_it = ln(P_it / P_i,t-1)
     = ln(P_it) - ln(P_i,t-1)
```

This produces the return matrix:

```
R ∈ ℝ^((T-1) × N)
```

One row is lost computing the first difference, so T−1 rows remain.

**Why log returns and not simple returns?**

Simple return:    R_simple = (P_t - P_{t-1}) / P_{t-1}

Log return:       r = ln(P_t / P_{t-1})

They are related by:   r = ln(1 + R_simple)

Log returns are preferred because:

- **Time-additive.** Multi-period log return = sum of single-period log
  returns. Simple returns must be multiplied, not summed.

  ```
  r_total = r_1 + r_2 + ... + r_T   (log)
  vs
  R_total = (1+R_1)(1+R_2)...(1+R_T) - 1   (simple)
  ```

- **Symmetric.** A +x log return followed by a -x log return returns
  exactly to the starting price. Simple returns are asymmetric
  (+100% then -50% ≠ breakeven).

- **Approximately Gaussian.** Under Geometric Brownian Motion (the
  standard model of stock prices), log returns are normally distributed.
  Simple returns are lognormal. Normal distributions are required for
  the covariance matrix to be well-defined in a linear algebra sense.

- **No lower bound issue.** Simple returns have a hard floor at -100%.
  Log returns have support (-∞, +∞) hence are unbound.

---

### 3. Demeaning

Before computing the covariance matrix, each column of R is demeaned
(its sample mean is subtracted):

```
R̃_ti = R_ti - r̄_i

where r̄_i = (1/T) Σ_t R_ti   is the sample mean return of asset i
```

This centres each asset's return series around zero. The demeaned
matrix R̃ has the same shape as R.

---

### 4. Covariance Matrix

The sample covariance matrix is:

```
Σ = (1 / (T-1)) · R̃ᵀ R̃        ∈ ℝ^(N × N)
```

The (i, j) entry of Σ is:

```
Σ_ij = (1 / (T-1)) Σ_t R̃_ti · R̃_tj
```

which is the sample covariance between asset i and asset j.

**Key properties of Σ:**

- **Symmetric:** Σ_ij = Σ_ji always, because Cov(X,Y) = Cov(Y,X).
  The upper and lower triangles are mirror images.

- **Diagonal = variances:** Σ_ii = Var(r_i), always ≥ 0.

- **Off-diagonal = covariances:** Σ_ij for i ≠ j can be positive,
  negative, or zero.

- **Positive semi-definite (PSD):** For any portfolio weight vector
  w ∈ ℝᴺ:

  ```
  wᵀ Σ w ≥ 0
  ```

  This must hold because wᵀΣw = Var(wᵀr) = portfolio variance,
  which is a squared quantity and can never be negative.

  Equivalently: wᵀΣw = ‖R̃w‖² / (T-1) ≥ 0 (a squared norm).

- **All eigenvalues ≥ 0** — a direct consequence of PSD.

**Financial meaning of covariance:**

```
Σ_ij > 0   assets i and j tend to move in the same direction
Σ_ij < 0   assets i and j tend to move in opposite directions
Σ_ij = 0   no linear relationship between assets i and j
```

---

### 5. Correlation Matrix

Covariance values depend on the scale of each asset's returns. A highly
volatile asset will have large covariance entries simply because its
returns are large — not necessarily because it is strongly related to
others. Correlation normalises this problem.

Let D be the diagonal matrix of standard deviations:

```
D = diag(σ_1, σ_2, ..., σ_N)    where σ_i = √Σ_ii
```

The correlation matrix is:

```
C = D⁻¹ Σ D⁻¹
```

Entry-wise:

```
C_ij = Σ_ij / (σ_i · σ_j)
```

**Properties of C:**

- Diagonal is all 1s: C_ii = Σ_ii / (σ_i · σ_i) = 1
- All entries bounded: -1 ≤ C_ij ≤ 1
- C_ij = +1  → perfect positive co-movement
- C_ij = -1  → perfect negative co-movement (moves exactly opposite)
- C_ij =  0  → no linear relationship

---

### 6. Portfolio Variance (why Σ matters)

For a portfolio with weight vector w ∈ ℝᴺ (weights sum to 1):

```
Portfolio return:    r_p = wᵀ μ
Portfolio variance:  σ_p² = wᵀ Σ w
```

Expanding for two assets:

```
σ_p² = w_1² σ_1² + 2 w_1 w_2 σ_12 + w_2² σ_2²
```

---

### 7. Annualised Volatility

Daily standard deviation is scaled to annual by the square-root-of-time rule:

```
σ_annual = σ_daily · √252
```

252 is the number of trading days in a year.
standard deviation scales with root of time hence 252 here.
---

## Outputs

| File | Description |
|---|---|
| `output/correlation_heatmap.png` | Lower-triangle heatmap of pairwise correlations |
| `output/cumulative_returns.png` | Growth of $1 invested in each stock |
| `output/volatility.png` | Annualised volatility per stock |

---
