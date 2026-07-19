from pathlib import Path

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_demo_runtime_has_no_telegram_dependency() -> None:
    runtime_files = [PROJECT_ROOT / "app.py", *sorted((PROJECT_ROOT / "ledgerlens").rglob("*.py"))]

    for runtime_file in runtime_files:
        assert "telegram" not in runtime_file.read_text(encoding="utf-8").lower()


def test_demo_app_does_not_instantiate_live_market_provider() -> None:
    app_source = (PROJECT_ROOT / "app.py").read_text(encoding="utf-8")

    assert "YFinanceMarketDataProvider" not in app_source
    assert "FixtureMarketDataProvider" in app_source


def test_docker_context_excludes_local_credentials_and_runtime_data() -> None:
    patterns = (PROJECT_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()

    assert ".env" in patterns
    assert ".env.*" in patterns
    assert ".venv/" in patterns
    assert "/runtime/" in patterns
    assert "/invoices/" in patterns
    assert "invoices/" not in patterns
    assert "*.db" in patterns
    assert "/LedgerLens_brand_pack_v2.zip" in patterns
    assert "/LedgerLens_brand_pack_v2/" in patterns


def test_gitignore_does_not_hide_invoice_source_package() -> None:
    patterns = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    assert "/invoices/" in patterns
    assert "invoices/" not in patterns


def test_curated_brand_assets_are_valid_pngs() -> None:
    asset_dir = PROJECT_ROOT / "assets" / "branding"
    expected_dimensions = {
        "ledgerlens-app-icon-192.png": (192, 192),
        "ledgerlens-avatar-512.png": (512, 512),
        "ledgerlens-brand-board.png": (1600, 1000),
        "ledgerlens-header-lockup.png": (583, 160),
        "ledgerlens-lockup-navy.png": (1370, 380),
    }

    for filename, dimensions in expected_dimensions.items():
        with Image.open(asset_dir / filename) as image:
            assert image.format == "PNG"
            assert image.size == dimensions
