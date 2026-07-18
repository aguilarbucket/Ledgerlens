from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from ledgerlens.analytics.portfolio_metrics import calculate_portfolio_metrics
from ledgerlens.domain.models import MarketPrice, PortfolioMetrics, Purchase

ZERO = Decimal("0")
HUNDRED = Decimal("100")


@dataclass(frozen=True, slots=True)
class TickerContribution:
    ticker: str
    amount_clp: Decimal


@dataclass(frozen=True, slots=True)
class DayMovement:
    movement_date: date
    amount_clp: Decimal


@dataclass(frozen=True, slots=True)
class PortfolioSnapshot:
    snapshot_date: date
    metrics: PortfolioMetrics
    allocations: dict[str, Decimal]


@dataclass(frozen=True, slots=True)
class DailyContext:
    report_date: date
    previous_price_date: date | None
    current_value_clp: Decimal | None
    daily_change_clp: Decimal | None
    daily_change_pct: Decimal | None
    unrealized_pnl_clp: Decimal | None
    contributions: tuple[TickerContribution, ...]
    top_positive: TickerContribution | None
    top_negative: TickerContribution | None
    top_three_concentration_pct: Decimal | None
    purchases_today: int
    invoices_today: int
    price_coverage_pct: Decimal
    missing_price_tickers: tuple[str, ...]
    stale_price_tickers: tuple[str, ...]
    context_quality: str


@dataclass(frozen=True, slots=True)
class WeeklyContext:
    report_date: date
    week_start: date
    current_week_change_clp: Decimal | None
    current_week_change_pct: Decimal | None
    previous_week_change_clp: Decimal | None
    difference_vs_previous_week_clp: Decimal | None
    baseline_average_change_clp: Decimal | None
    baseline_weeks: int
    contributions: tuple[TickerContribution, ...]
    top_positive: TickerContribution | None
    top_negative: TickerContribution | None
    concentration_change_pct_points: Decimal | None
    distribution_change_pct_points: Decimal | None
    best_day: DayMovement | None
    worst_day: DayMovement | None
    positions_added: tuple[str, ...]
    missing_invoices: int
    incomplete_records: int
    price_coverage_pct: Decimal
    missing_price_tickers: tuple[str, ...]
    stale_price_tickers: tuple[str, ...]
    context_quality: str


def _percent(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    if denominator == ZERO:
        return None
    return (numerator / denominator * HUNDRED).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _latest_date_on_or_before(available: list[date], boundary: date) -> date | None:
    matches = [item for item in available if item <= boundary]
    return max(matches) if matches else None


def _snapshot(
    purchases: list[Purchase],
    prices_by_date: dict[date, dict[str, MarketPrice]],
    snapshot_date: date,
) -> PortfolioSnapshot:
    eligible = [purchase for purchase in purchases if purchase.purchase_date <= snapshot_date]
    metrics = calculate_portfolio_metrics(eligible, prices_by_date.get(snapshot_date, {}))
    allocations = {
        position.ticker: position.allocation_pct
        for position in metrics.positions
        if position.allocation_pct is not None
    }
    return PortfolioSnapshot(snapshot_date, metrics, allocations)


def _period_movement(
    purchases: list[Purchase],
    prices_by_date: dict[date, dict[str, MarketPrice]],
    start_date: date,
    end_date: date,
) -> tuple[tuple[TickerContribution, ...], Decimal | None, Decimal | None]:
    quantities: dict[str, Decimal] = {}
    for purchase in purchases:
        if purchase.purchase_date <= start_date:
            quantities[purchase.ticker] = quantities.get(purchase.ticker, ZERO) + purchase.quantity

    start_prices = prices_by_date.get(start_date, {})
    end_prices = prices_by_date.get(end_date, {})
    contributions: list[TickerContribution] = []
    start_value = ZERO
    for ticker, quantity in quantities.items():
        start = start_prices.get(ticker)
        end = end_prices.get(ticker)
        if start is None or end is None:
            continue
        start_value += quantity * start.price_clp
        contributions.append(
            TickerContribution(ticker, quantity * (end.price_clp - start.price_clp))
        )

    if not contributions:
        return (), None, None
    total = sum((item.amount_clp for item in contributions), ZERO)
    return (
        tuple(sorted(contributions, key=lambda item: item.ticker)),
        total,
        _percent(total, start_value),
    )


def _extreme_contributors(
    contributions: tuple[TickerContribution, ...],
) -> tuple[TickerContribution | None, TickerContribution | None]:
    positive = [item for item in contributions if item.amount_clp > ZERO]
    negative = [item for item in contributions if item.amount_clp < ZERO]
    return (
        max(positive, key=lambda item: item.amount_clp) if positive else None,
        min(negative, key=lambda item: item.amount_clp) if negative else None,
    )


def _top_three_concentration(metrics: PortfolioMetrics) -> Decimal | None:
    allocations = sorted(
        (
            position.allocation_pct
            for position in metrics.positions
            if position.allocation_pct is not None
        ),
        reverse=True,
    )
    return sum(allocations[:3], ZERO) if allocations else None


def _stale_tickers(
    prices: dict[str, MarketPrice], as_of: datetime, stale_after_hours: int
) -> tuple[str, ...]:
    threshold = as_of - timedelta(hours=stale_after_hours)
    return tuple(sorted(ticker for ticker, price in prices.items() if price.as_of < threshold))


def _quality(
    *, coverage: Decimal, comparable: bool, stale: tuple[str, ...], baseline_weeks: int = 0
) -> str:
    if not comparable or coverage < Decimal("80"):
        return "insufficient"
    if stale or coverage < HUNDRED or (baseline_weeks and baseline_weeks < 4):
        return "partial"
    return "good"


def build_daily_context(
    purchases: list[Purchase],
    prices_by_date: dict[date, dict[str, MarketPrice]],
    *,
    report_date: date,
    as_of: datetime,
    stale_after_hours: int = 36,
) -> DailyContext:
    available = sorted(prices_by_date)
    current_price_date = _latest_date_on_or_before(available, report_date)
    if current_price_date is None:
        current_prices: dict[str, MarketPrice] = {}
        snapshot = _snapshot(purchases, {}, report_date)
    else:
        current_prices = prices_by_date[current_price_date]
        snapshot = _snapshot(purchases, prices_by_date, current_price_date)

    previous_candidates = [
        item for item in available if current_price_date and item < current_price_date
    ]
    previous_date = max(previous_candidates) if previous_candidates else None
    if current_price_date is not None and previous_date is not None:
        contributions, change, change_pct = _period_movement(
            purchases, prices_by_date, previous_date, current_price_date
        )
    else:
        contributions, change, change_pct = (), None, None

    top_positive, top_negative = _extreme_contributors(contributions)
    stale = _stale_tickers(current_prices, as_of, stale_after_hours)
    purchases_today = [purchase for purchase in purchases if purchase.purchase_date == report_date]
    quality = _quality(
        coverage=snapshot.metrics.price_coverage_pct,
        comparable=bool(contributions),
        stale=stale,
    )
    return DailyContext(
        report_date=report_date,
        previous_price_date=previous_date,
        current_value_clp=snapshot.metrics.current_value_clp,
        daily_change_clp=change,
        daily_change_pct=change_pct,
        unrealized_pnl_clp=snapshot.metrics.unrealized_pnl_clp,
        contributions=contributions,
        top_positive=top_positive,
        top_negative=top_negative,
        top_three_concentration_pct=_top_three_concentration(snapshot.metrics),
        purchases_today=len(purchases_today),
        invoices_today=sum(
            1 for purchase in purchases_today if purchase.document_reference is not None
        ),
        price_coverage_pct=snapshot.metrics.price_coverage_pct,
        missing_price_tickers=snapshot.metrics.missing_price_tickers,
        stale_price_tickers=stale,
        context_quality=quality,
    )


def _distribution_shift(start: dict[str, Decimal], end: dict[str, Decimal]) -> Decimal | None:
    tickers = set(start) | set(end)
    if not tickers:
        return None
    total = sum((abs(end.get(ticker, ZERO) - start.get(ticker, ZERO)) for ticker in tickers), ZERO)
    return (total / Decimal("2")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _incomplete_purchase(purchase: Purchase) -> bool:
    return bool(
        not purchase.company.strip()
        or not purchase.ticker.strip()
        or purchase.quantity <= ZERO
        or purchase.unit_price_clp <= ZERO
        or purchase.currency != "CLP"
    )


def build_weekly_context(
    purchases: list[Purchase],
    prices_by_date: dict[date, dict[str, MarketPrice]],
    *,
    report_date: date,
    as_of: datetime,
    baseline_limit: int = 8,
    stale_after_hours: int = 36,
) -> WeeklyContext:
    available = sorted(prices_by_date)
    week_start = report_date - timedelta(days=report_date.weekday())
    current_start_date = _latest_date_on_or_before(available, week_start - timedelta(days=1))
    current_end_date = _latest_date_on_or_before(available, report_date)
    previous_start_boundary = week_start - timedelta(days=8)
    previous_start_date = _latest_date_on_or_before(available, previous_start_boundary)
    previous_end_date = current_start_date

    if current_start_date and current_end_date:
        contributions, current_change, current_change_pct = _period_movement(
            purchases, prices_by_date, current_start_date, current_end_date
        )
        start_snapshot = _snapshot(purchases, prices_by_date, current_start_date)
        end_snapshot = _snapshot(purchases, prices_by_date, current_end_date)
    else:
        contributions, current_change, current_change_pct = (), None, None
        start_snapshot = _snapshot(purchases, {}, week_start)
        end_snapshot = _snapshot(purchases, {}, report_date)

    if previous_start_date and previous_end_date:
        _, previous_change, _ = _period_movement(
            purchases, prices_by_date, previous_start_date, previous_end_date
        )
    else:
        previous_change = None

    baseline_changes: list[Decimal] = []
    for offset in range(1, baseline_limit + 1):
        end_boundary = week_start - timedelta(days=1 + 7 * (offset - 1))
        start_boundary = end_boundary - timedelta(days=7)
        baseline_start = _latest_date_on_or_before(available, start_boundary)
        baseline_end = _latest_date_on_or_before(available, end_boundary)
        if baseline_start is None or baseline_end is None or baseline_start == baseline_end:
            continue
        _, baseline_change, _ = _period_movement(
            purchases, prices_by_date, baseline_start, baseline_end
        )
        if baseline_change is not None:
            baseline_changes.append(baseline_change)

    baseline_average = (
        sum(baseline_changes, ZERO) / Decimal(len(baseline_changes)) if baseline_changes else None
    )
    difference = (
        current_change - previous_change
        if current_change is not None and previous_change is not None
        else None
    )
    top_positive, top_negative = _extreme_contributors(contributions)

    start_concentration = _top_three_concentration(start_snapshot.metrics)
    end_concentration = _top_three_concentration(end_snapshot.metrics)
    concentration_change = (
        end_concentration - start_concentration
        if end_concentration is not None and start_concentration is not None
        else None
    )

    daily_movements: list[DayMovement] = []
    relevant_dates = [
        item
        for item in available
        if current_start_date and current_start_date <= item <= report_date
    ]
    for start_date, end_date in zip(relevant_dates, relevant_dates[1:], strict=False):
        if end_date < week_start:
            continue
        _, movement, _ = _period_movement(purchases, prices_by_date, start_date, end_date)
        if movement is not None:
            daily_movements.append(DayMovement(end_date, movement))

    held_before_week = {
        purchase.ticker for purchase in purchases if purchase.purchase_date < week_start
    }
    current_week_purchases = [
        purchase for purchase in purchases if week_start <= purchase.purchase_date <= report_date
    ]
    positions_added = tuple(
        sorted({purchase.ticker for purchase in current_week_purchases} - held_before_week)
    )
    current_prices = prices_by_date.get(current_end_date, {}) if current_end_date else {}
    stale = _stale_tickers(current_prices, as_of, stale_after_hours)
    quality = _quality(
        coverage=end_snapshot.metrics.price_coverage_pct,
        comparable=bool(contributions),
        stale=stale,
        baseline_weeks=len(baseline_changes),
    )
    if not baseline_changes:
        quality = "insufficient"
    elif len(baseline_changes) < 4 and quality == "good":
        quality = "partial"

    return WeeklyContext(
        report_date=report_date,
        week_start=week_start,
        current_week_change_clp=current_change,
        current_week_change_pct=current_change_pct,
        previous_week_change_clp=previous_change,
        difference_vs_previous_week_clp=difference,
        baseline_average_change_clp=baseline_average,
        baseline_weeks=len(baseline_changes),
        contributions=contributions,
        top_positive=top_positive,
        top_negative=top_negative,
        concentration_change_pct_points=concentration_change,
        distribution_change_pct_points=_distribution_shift(
            start_snapshot.allocations, end_snapshot.allocations
        ),
        best_day=max(daily_movements, key=lambda item: item.amount_clp)
        if daily_movements
        else None,
        worst_day=min(daily_movements, key=lambda item: item.amount_clp)
        if daily_movements
        else None,
        positions_added=positions_added,
        missing_invoices=sum(
            1 for purchase in current_week_purchases if not purchase.document_reference
        ),
        incomplete_records=sum(1 for purchase in purchases if _incomplete_purchase(purchase)),
        price_coverage_pct=end_snapshot.metrics.price_coverage_pct,
        missing_price_tickers=end_snapshot.metrics.missing_price_tickers,
        stale_price_tickers=stale,
        context_quality=quality,
    )
