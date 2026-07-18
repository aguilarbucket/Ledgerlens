import os

from ledgerlens.config import load_project_environment


def test_load_project_environment_preserves_explicit_process_values(tmp_path, monkeypatch) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text(
        "OPENAI_API_KEY=file-key\nLEDGERLENS_DEMO_MODE=true\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENAI_API_KEY", "process-key")
    monkeypatch.delenv("LEDGERLENS_DEMO_MODE", raising=False)

    assert load_project_environment(env_path) is True
    assert os.environ["OPENAI_API_KEY"] == "process-key"
    assert os.environ["LEDGERLENS_DEMO_MODE"] == "true"
