"""Read-only network acceptance for the public marketplace ownership transition."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
LEGACY = "TshyGO/NebulaLab-Plugins"
DESTINATION = "ptjworks/NebulaLab-Plugins"


def read_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "NebulaLab-Market-Migration/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def repository_url(url: str, repository: str) -> str:
    """Repoint only this marketplace's own public GitHub/raw URLs."""
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc not in {"github.com", "raw.githubusercontent.com"}:
        return url
    for source in (LEGACY, DESTINATION):
        prefix = f"/{source}/"
        if parsed.path.startswith(prefix):
            return urlunsplit(parsed._replace(path=f"/{repository}/{parsed.path[len(prefix):]}"))
    return url


def load_validator(filename: str):
    spec = importlib.util.spec_from_file_location(filename.replace(".", "_"), ROOT / ".github" / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(repositories: list[str]) -> dict:
    baseline = None
    summary = {}
    plugin_validator = load_validator("validate_plugin_release_assets.py")
    theme_validator = load_validator("validate_theme_release_assets.py")
    for repository in repositories:
        indexes = {}
        for name in ("plugins", "themes"):
            url = f"https://raw.githubusercontent.com/{repository}/main/{name}-index.json"
            payload = json.loads(read_bytes(url))
            if not isinstance(payload, dict) or not isinstance(payload.get(name), list):
                raise ValueError(f"{repository}: invalid {name} index")
            indexes[name] = payload
        if baseline is None:
            baseline = indexes
        elif indexes != baseline:
            raise ValueError("Legacy and destination indexes differ; retry only after investigating concurrent publication")

        icon_digests = {}
        for name, validator, method in (
            ("plugins", plugin_validator, "validate_plugin_asset"),
            ("themes", theme_validator, "validate_theme_asset"),
        ):
            for original in indexes[name][name]:
                entry = copy.deepcopy(original)
                entry["download_url"] = repository_url(entry["download_url"], repository)
                # Existing validators check actual ZIP bytes, digest, safe paths,
                # manifest ID/version, required files and plugin risk patterns.
                getattr(validator, method)(entry)
                if original.get("logo_url"):
                    icon_url = repository_url(original["logo_url"], repository)
                    icon_digests[original["id"]] = hashlib.sha256(read_bytes(icon_url)).hexdigest()
        summary[repository] = {
            "plugins": len(indexes["plugins"]["plugins"]),
            "themes": len(indexes["themes"]["themes"]),
            "icon_sha256": icon_digests,
        }
    if len(summary) > 1:
        first = next(iter(summary.values()))
        if any(row != first for row in summary.values()):
            raise ValueError("Legacy and destination asset summaries differ")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-destination", action="store_true", help="Probe the destination too, only after transfer.")
    args = parser.parse_args()
    repositories = [LEGACY]
    if args.include_destination or os.environ.get("GITHUB_REPOSITORY") == DESTINATION:
        repositories.append(DESTINATION)
    print(json.dumps(verify(repositories), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
