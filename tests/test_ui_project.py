from ledgerlens.ui.project import project_flow_html


def test_project_flow_explains_the_human_verified_sequence() -> None:
    html = project_flow_html()

    assert 'aria-label="LedgerLens workflow"' in html
    assert html.count('class="ll-project-step"') == 4
    assert "Upload" in html
    assert "AI extraction" in html
    assert "Human review" in html
    assert "Unified portfolio" in html
