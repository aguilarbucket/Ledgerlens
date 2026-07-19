from ledgerlens.ui.charts import (
    allocation_color_map,
    allocation_donut,
    contribution_chart,
    portfolio_history_chart,
    weekly_comparison_chart,
)


def test_allocation_chart_keeps_fintech_palette_and_tooltips() -> None:
    chart = allocation_donut(
        [{"ticker": "DEMO.SN", "value_clp": 1000.0, "allocation_pct": 100.0}]
    ).to_dict()

    assert chart["mark"]["type"] == "arc"
    assert chart["encoding"]["color"]["scale"]["range"][0] == "#4F8CFF"
    assert chart["encoding"]["color"]["legend"] is None
    assert chart["description"] == "Current portfolio allocation by ticker"


def test_history_chart_distinguishes_invested_and_current_value() -> None:
    chart = portfolio_history_chart(
        [
            {"date": "2026-07-18", "series": "Current value", "value_clp": 1100.0},
            {"date": "2026-07-18", "series": "Invested value", "value_clp": 1000.0},
        ]
    ).to_dict()

    assert len(chart["layer"]) == 2
    assert chart["description"] == (
        "Observable current and invested portfolio value over time"
    )


def test_allocation_color_map_is_stable_by_ticker() -> None:
    colors = allocation_color_map(
        [
            {"ticker": "Z.SN", "value_clp": 1.0, "allocation_pct": 50.0},
            {"ticker": "A.SN", "value_clp": 1.0, "allocation_pct": 50.0},
        ]
    )

    assert colors == {"A.SN": "#4F8CFF", "Z.SN": "#2DD4BF"}


def test_contribution_chart_has_semantic_direction_scale() -> None:
    chart = contribution_chart(
        [
            {"ticker": "GAIN.SN", "amount_clp": 50.0, "direction": "Positive"},
            {"ticker": "LOSS.SN", "amount_clp": -25.0, "direction": "Negative"},
        ],
        description="Daily contribution",
    ).to_dict()

    color = chart["layer"][0]["encoding"]["color"]["scale"]
    assert color["domain"] == ["Positive", "Negative", "Neutral"]
    assert color["range"][:2] == ["#22C55E", "#F87171"]
    assert chart["description"] == "Daily contribution"


def test_weekly_comparison_chart_names_all_periods() -> None:
    chart = weekly_comparison_chart(
        [
            {"period": "Current week", "amount_clp": 100.0},
            {"period": "Prior week", "amount_clp": 80.0},
            {"period": "Baseline average", "amount_clp": 90.0},
        ]
    ).to_dict()

    assert chart["description"] == "Weekly movement comparison"
    assert chart["encoding"]["color"]["scale"]["domain"] == [
        "Current week",
        "Prior week",
        "Baseline average",
    ]
