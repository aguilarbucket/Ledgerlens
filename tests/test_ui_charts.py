from ledgerlens.ui.charts import (
    allocation_color_map,
    allocation_donut,
    portfolio_history_chart,
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
