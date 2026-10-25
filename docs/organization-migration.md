# PTJ Works ownership transition

The public repository transferred to `ptjworks/NebulaLab-Plugins` on
2026-10-25. Repository ID `1210416222` identifies the same repository before
and after transfer; its name, history, `plugins` release and assets are preserved.
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
Before transfer it checks the legacy routes. Under `ptjworks` it automatically
checks both owners. To repeat the post-transfer check explicitly, run:

```sh
gh workflow run marketplace-compatibility.yml --repo ptjworks/NebulaLab-Plugins -f include_destination=true
```

The probe checks both old and new index routes and actual plugin ZIP routes.
For icons it checks reachability and equality of downloaded byte digests across
the two owners; it does not decode images or assess their appearance. It rejects
mismatching indexes or asset contents. This is network/package acceptance, not
a substitute for complete desktop/Tauri installation acceptance.
