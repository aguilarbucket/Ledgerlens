from __future__ import annotations

from pathlib import Path

import streamlit as st

from ledgerlens.ui.components import render_section_header


def project_flow_html() -> str:
    steps = (
        ("01", "Upload", "Validate a brokerage PDF before any extraction begins."),
        ("02", "AI extraction", "Create a typed draft with confidence and warnings."),
        ("03", "Human review", "Edit the fields and explicitly confirm what enters the ledger."),
        ("04", "Unified portfolio", "Calculate one deterministic view across brokers."),
    )
    content = "".join(
        (
            '<div class="ll-project-step">'
            f"<span>{number}</span><strong>{title}</strong><p>{description}</p>"
            "</div>"
        )
        for number, title, description in steps
    )
    return f'<div class="ll-project-flow" aria-label="LedgerLens workflow">{content}</div>'


def render_project_page(*, logo_path: str | Path) -> None:
    st.image(str(logo_path), width=350)
    st.markdown("### Many sources. One verified view.")
    st.caption("OpenAI Build Week 2026 · Personal finance · Human-verified AI")

    with st.container(border=True):
        render_section_header(
            "Why LedgerLens",
            "A personal tracking problem shaped into a focused multi-broker workflow.",
        )
        st.markdown(
            """
            As an amateur investor, I manage positions through different brokerages. Each broker
            has its own dashboard, vocabulary, and transaction history, which makes it harder to
            maintain one simple view of what I own and how my portfolio is changing. More advanced
            market platforms can be useful, but sometimes add complexity when the immediate need is
            clarity. LedgerLens consolidates brokerage evidence into one reviewable ledger. If that
            simpler workflow is useful for my own tracking, it may also help other retail investors
            facing the same fragmentation.
            """
        )

    st.write("")
    render_section_header(
        "How it works",
        "AI assists with interpretation; people and deterministic code remain in control.",
    )
    st.markdown(project_flow_html(), unsafe_allow_html=True)

    trust_column, boundary_column = st.columns(2)
    with trust_column:
        with st.container(border=True):
            render_section_header("Trust controls")
            st.markdown(
                """
                - Uploaded PDFs are processed in memory and are not retained.
                - A person reviews and confirms every extracted purchase.
                - SQLite stores the confirmed record and document SHA-256 for traceability.
                - Corrections are reversible and preserve their audit reason.
                - AI requests are explicit, bounded, and configured with `store=False`.
                """
            )
    with boundary_column:
        with st.container(border=True):
            render_section_header("Clear responsibility boundary")
            st.markdown(
                """
                **Python calculates** weighted cost, current value, allocation, price coverage,
                unrealized P/L, contribution, concentration, and data quality.

                **OpenAI assists** with typed invoice extraction and concise narratives derived
                from supplied deterministic facts. It does not calculate portfolio truth, decide
                what to save, recommend trades, predict prices, or invent market causes.
                """
            )

    st.write("")
    with st.container(border=True):
        render_section_header("Current scope and limits")
        scope, limits = st.columns(2)
        with scope:
            st.markdown(
                """
                **Current demonstration**

                - Chilean equity purchases denominated in CLP
                - Multiple fictional brokers and synthetic invoices
                - Offline fixture path plus optional GPT-5.6 path
                - Persistent, auditable local SQLite ledger
                """
            )
        with limits:
            st.markdown(
                """
                **Deliberate limitations**

                - Purchases only; sales are not yet modeled
                - No realized P/L, tax accounting, or trade execution
                - No recommendations or price predictions
                - Demonstration data is entirely fictional
                """
            )

    st.warning(
        "LedgerLens is descriptive demonstration software. It is not financial, investment, "
        "tax, or legal advice."
    )

    source_link, container_link = st.columns(2)
    with source_link:
        st.link_button(
            "View source on GitHub",
            "https://github.com/aguilarbucket/Ledgerlens",
            use_container_width=True,
        )
    with container_link:
        st.link_button(
            "Open Docker Hub image",
            "https://hub.docker.com/r/alejandroromeroa/ledgerlens",
            use_container_width=True,
        )
