# PTJ Works ownership transition

The destination is `ptjworks/NebulaLab-Plugins`. The existing repository is
transferred with its name, history, `plugins` release and assets preserved.
No private application repository is part of this change.

## Existing clients and indexes

Keep `plugins-index.json` and `themes-index.json` at their existing root paths.
Existing plugin entries intentionally retain their `TshyGO` download, homepage
and logo URLs during this transition: they work before transfer and continue
through GitHub's legacy routes afterwards. Do not recreate a repository or fork
at `TshyGO/NebulaLab-Plugins`, because doing so destroys those redirects.

Do not change plugin IDs, versions, SHA-256 digests or author GitHub identities
just because the repository owner changes. Community plugin URLs remain owned
by their authors. The empty theme index remains empty; no theme installation is
claimed by validating an empty index.

For new official releases after transfer, select the canonical destination
explicitly with the existing packager option:

```sh
python scripts/package_official_plugin.py baseline-als --repo ptjworks/NebulaLab-Plugins --update-index
```

Upload the generated ZIP before publishing its index entry. Keep the legacy
packager default for existing automation; `gh` follows the repository API
redirect. Replace old index URLs during a real package update, after its new
asset and digest have been verified, rather than before the destination exists.

## CI and acceptance

The AI review caller remains pinned to `TshyGO/ci-central`, with identical full
SHAs in `uses` and `central_workflow_sha`. The reviewed central configuration
registers both repository identities with unchanged policy and credential slots.
The caller keeps the existing hosted runner tier; no self-hosted or private
repository runner is exposed to public pull requests.

`Marketplace Compatibility` validates index schemas and the migration probe,
then downloads actual published ZIPs and checks digest, archive safety, manifest
identity/version and required files through the existing asset validators.
Before transfer it checks the legacy routes. After transfer run:

```sh
gh workflow run marketplace-compatibility.yml --repo ptjworks/NebulaLab-Plugins -f include_destination=true
```

The probe checks both old and new index routes, actual plugin ZIP routes and
icons, and rejects mismatching indexes or contents. This is network/package
acceptance, not a substitute for complete desktop/Tauri installation acceptance.
