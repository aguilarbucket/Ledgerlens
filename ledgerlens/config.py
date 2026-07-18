from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_project_environment(env_path: Path | None = None) -> bool:
    """Load local configuration without replacing explicit process variables."""
    return load_dotenv(dotenv_path=env_path or PROJECT_ROOT / ".env", override=False)
