from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("marketplace_migration", ROOT / "scripts" / "verify_marketplace_endpoints.py")
assert spec is not None and spec.loader is not None
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)


@pytest.mark.parametrize("host", ["github.com", "raw.githubusercontent.com"])
@pytest.mark.parametrize("owner", ["TshyGO", "ptjworks"])
def test_owned_download_paths_support_both_owners(host, owner):
    url = f"https://{host}/{owner}/NebulaLab-Plugins/releases/download/plugins/example.zip"
    assert migration.repository_url(url, migration.DESTINATION) == (
        f"https://{host}/ptjworks/NebulaLab-Plugins/releases/download/plugins/example.zip"
    )


@pytest.mark.parametrize("url", [
    "https://github.com/community/plugin/releases/download/v1/plugin.zip",
    "https://example.org/TshyGO/NebulaLab-Plugins/plugin.zip",
    "https://github.com.evil.test/TshyGO/NebulaLab-Plugins/plugin.zip",
    "https://github.com/TshyGO/NebulaLab-Plugins-other/plugin.zip",
    "https://user:password@github.com/TshyGO/NebulaLab-Plugins/plugin.zip",
    "http://github.com/TshyGO/NebulaLab-Plugins/plugin.zip",
])
def test_unrelated_or_noncanonical_urls_are_not_rewritten(url):
    assert migration.repository_url(url, migration.DESTINATION) == url


def test_network_acceptance_checks_both_asset_routes_and_detects_index_drift(monkeypatch):
    payload = {"plugins": [{"id": "example", "download_url": "https://github.com/TshyGO/NebulaLab-Plugins/releases/download/plugins/example.zip"}]}
    calls = []
    monkeypatch.setattr(migration, "read_bytes", lambda url: json.dumps(payload if url.endswith("plugins-index.json") else {"themes": []}).encode())
    monkeypatch.setattr(migration, "load_validator", lambda name: SimpleNamespace(
        validate_plugin_asset=lambda entry: calls.append(entry["download_url"]),
        validate_theme_asset=lambda entry: None,
    ))
    result = migration.verify([migration.LEGACY, migration.DESTINATION])
    assert list(result) == [migration.LEGACY, migration.DESTINATION]
    assert calls == [payload["plugins"][0]["download_url"], payload["plugins"][0]["download_url"].replace("TshyGO/", "ptjworks/")]
    monkeypatch.setattr(migration, "read_bytes", lambda url: json.dumps(
        {"plugins": []} if "ptjworks/" in url and url.endswith("plugins-index.json")
        else payload if url.endswith("plugins-index.json") else {"themes": []}
    ).encode())
    with pytest.raises(ValueError, match="indexes differ"):
        migration.verify([migration.LEGACY, migration.DESTINATION])
