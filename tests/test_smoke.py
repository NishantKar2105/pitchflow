from pitchflow.config import Settings


def test_settings_dsn(monkeypatch):
    monkeypatch.setenv("PITCHFLOW_DB_PASSWORD", "x")
    s = Settings()
    assert "pitchflow" in s.db_dsn
