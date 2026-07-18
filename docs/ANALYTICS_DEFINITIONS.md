# Analytics definitions

LedgerLens separates market movement from portfolio cash flows.

## Daily Lens

- **Portfolio value:** confirmed quantities multiplied by the latest available price on the report
  date.
- **Daily observable movement:** quantity held at the previous observable price date multiplied by
  the price change for each ticker. Purchases made after that prior date are not treated as market
  gains or losses.
- **Daily contribution:** each ticker's component of daily observable movement.
- **Unrealized P/L:** current priced value minus purchase cost for positions with prices.
- **Coverage:** invested cost represented by positions with a current price, divided by total
  invested cost.
- Missing prices are never treated as zero movement.

## Weekly Lens

- The current week starts Monday in `America/Santiago` and ends on the report date.
- **Weekly observable movement:** price contribution from positions held at the latest observable
  price before the week to the latest price on the report date.
- **Prior week:** the immediately preceding Monday-to-Sunday interval using observable price dates.
- **Historical baseline:** up to eight prior observable weekly movements; the fixture currently
  provides seven comparable weeks.
- **Distribution shift:** one half of the sum of absolute allocation changes across all tickers,
  expressed in percentage points.
- **Best/worst observable day:** maximum/minimum comparable daily market contribution inside the
  current week.
- Positions purchased during the week and invoice completeness are reported separately.

These definitions describe observable synthetic data. They are not realized returns, market-cause
claims, forecasts, or financial advice.

