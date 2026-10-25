# NebulaLab-Plugins

[中文](#中文) | [English](#english)

---

<a name="中文"></a>

## 简介

这是 [Nebula Lab](https://nebulalab.app/) 的插件与主题市场仓库，包含官方插件源码、插件和主题市场索引、插件开发 SDK、插件模板和开发文档。

Nebula Lab 直接读取本仓库 `main` 分支根目录下的 `plugins-index.json` 和 `themes-index.json`；官方插件的 zip 包发布在本仓库的 [`plugins` Release](https://github.com/ptjworks/NebulaLab-Plugins/releases/tag/plugins)。

本仓库已迁至 [PTJ Works](https://github.com/ptjworks/NebulaLab-Plugins)，兼容安排见[组织迁移说明](./docs/organization-migration.md)。现有插件索引、版本、校验值和作者身份保持不变。

## 安装插件和主题（用户）

直接在 Nebula Lab 里操作，无需访问本仓库：

- **社区 → 插件广场**：浏览并安装插件（需联网）
- **社区 → 主题广场**：浏览并安装主题（需联网）
- **设置 → 插件 → 从本地安装**：安装本地插件 `.zip`
- **设置 → 外观 → 自定义主题 → 从本地安装**：安装本地主题 `.zip`

## 开发插件

| 文档 | 说明 |
|------|------|
| [快速开始](./docs/getting_started.md) | 从环境搭建到第一个插件 |
| [SDK API 参考](./docs/api_reference.md) | `@op` 装饰器、`OperationContext` 详解（英文） |
| [插件工作区管理](./docs/workspace_management.md) | 官方插件源码、市场索引、Release 与换电脑恢复流程 |
| [Claude Code Skill](./skills/nebula-plugin-dev.md) | AI 辅助开发插件，含面板消息桥与市场发布字段 |

新插件可以从 [`templates/plugin_template/`](./templates/plugin_template/) 模板开始。

## 开发主题

| 文档 | 说明 |
|------|------|
| [Claude Code Skill](./skills/nebula-theme-dev.md) | AI 辅助设计主题，含市场元数据与完整 CSS 变量参考表 |
| [贡献指南 · 主题部分](./docs/contributing.md#提交主题到主题市场) | 主题打包与发布流程 |

## 提交到插件市场

流程详见 [贡献指南](./docs/contributing.md)。核心步骤：

1. 在自己的仓库发布插件 Release（zip 包）。zip 根目录（或唯一的顶层文件夹）里要有 `plugin.json`，其 `id`、`version` 与索引条目一致，并至少声明 `operations`、`importers` 或 `panel` 之一：声明了 `operations` / `importers` 时要包含 `__init__.py`，声明了 `panel` 时要包含对应的 `.html` 文件
2. 计算 zip 的 sha256 校验值
3. 可选提供插件徽标 `logo_url`，用于市场卡片展示
4. 提供项目主页 `homepage`；社区插件还必须提供源码仓库地址 `source_url`
5. Fork 本仓库，在 `plugins-index.json` 添加条目；PR 只修改这一个文件
6. 提交 PR — CI 校验索引格式，下载你声明的 release zip，校验 sha256、包结构和基础危险模式；CI 通过后，还需维护者审核批准才会合并

索引条目中 CI 强制校验的字段：`id`（只允许小写字母、数字、`-`、`_`）、`name`、`version`（`x.y.z`）、`source`（`official` 或 `community`）、`download_url`、`homepage`、`sha256`（64 位十六进制）；社区插件另需 `source_url`，官方插件另需 `author_github` 和 `author_url`（`https://github.com/<author_github>`）。所有链接都必须以 `https://` 开头。其余字段按贡献指南的示例填写。

## 提交到主题市场

1. 在自己的仓库发布主题 Release（zip 包）。zip 根目录（或唯一的顶层文件夹）里要有 `theme.json`，其 `id`、`version`、`color_scheme`、`background_image_url` 与索引条目一致（索引条目不写 `background_image_url` 时，`theme.json` 里也不能有）
2. 计算 zip 的 sha256 校验值
3. 准备索引条目必填字段：`id`、`name`、`version`、`author`、`source`、`description`、`color_scheme`（`light` 或 `dark`）、`download_url`、`sha256`、`homepage`、`preview_image_url`、`min_app_version`、`tags`、`accessibility_notes`；`background_image_url` 可选
4. Fork 本仓库，在 `themes-index.json` 添加条目；PR 只能修改这一个文件，否则主题校验直接失败
5. 提交 PR — CI 校验索引格式，下载你声明的 release zip，校验 sha256 和 `theme.json`；CI 通过后，还需维护者审核批准才会合并

## 发布官方插件（维护者）

1. 修改 `plugins/official/<插件目录>/`，并升级 `plugin.json` 的 `version`。PR 改动插件源码时，CI 会检查每个 `plugin.json`（`id`、`name`、`version` 必填，官方插件还需 `author_github` 和对应的 `author_url`）、扫描危险调用并运行 `tests/` 下的测试。
2. 打包并更新索引（生成 `dist/plugins/<id>-<version>.zip`，输出 sha256 和上传命令；`--update-index` 只改写索引中已有条目的 `version`、`download_url` 和 `sha256`，新插件要先手动添加条目）：

   ```sh
   python scripts/package_official_plugin.py <插件目录或 id> --repo ptjworks/NebulaLab-Plugins --update-index
   ```

3. 先把 zip 上传到 `plugins` Release，再提交索引更新：

   ```sh
   gh release upload plugins dist/plugins/<id>-<version>.zip --repo ptjworks/NebulaLab-Plugins
   ```

   zip 文件名带版本号。改了源码却不升级版本，会打出 sha256 不同的同名 zip；覆盖上传后，现有索引条目的校验值就对不上了。所以上传因同名资产已存在而失败时，不要加 `--clobber` 覆盖，应升级版本后重新打包。

打包脚本的 `--repo` 默认值仍是迁移前的地址，新发布的包要显式指定 `--repo ptjworks/NebulaLab-Plugins`，原因见[组织迁移说明](./docs/organization-migration.md)。

## 安全说明

- 市场 CI 会核对索引声明与实际上传的 zip 包是否一致（sha256、清单中的 `id` 和版本）。
- 这只是自动化完整性校验与基础启发式扫描，不等于人工安全审计。
- 安装社区插件前，仍建议先查看主页、源码仓库和 release 内容。

## 仓库结构

```
NebulaLab-Plugins/
├── plugins-index.json          # 插件市场索引（应用直接读取）
├── themes-index.json           # 主题市场索引（应用直接读取）
├── NebulaLab.code-workspace    # 主应用 + 插件仓库的本地多根工作区
├── LICENSE                     # MIT 许可证
├── plugins/official/           # 官方插件源码
├── assets/icons/               # 官方插件的市场图标
├── nebula_sdk/                 # 插件开发 SDK（Python 包）
├── templates/plugin_template/  # 插件开发模板
├── scripts/                    # 官方插件打包、市场端点核对脚本
├── tests/                      # 官方插件与校验脚本的测试
├── docs/                       # 开发文档
│   ├── getting_started.md      # 插件入门指南
│   ├── api_reference.md        # SDK API 参考
│   ├── workspace_management.md # 本地仓库编排与换机恢复
│   ├── contributing.md         # 贡献指南（插件 + 主题）
│   └── organization-migration.md # 迁至 PTJ Works 的兼容安排
├── skills/                     # AI 辅助开发 skill
│   ├── nebula-plugin-dev.md    # 插件开发 skill
│   └── nebula-theme-dev.md     # 主题开发 skill
└── .github/
    ├── scripts/                # CI 校验脚本
    └── workflows/              # CI：PR 时校验索引、release 资产与插件源码
```

---

<a name="english"></a>

## Overview

This is the plugin and theme marketplace repository for [Nebula Lab](https://nebulalab.app/). It contains the official plugin sources, the plugin and theme marketplace indexes, the plugin development SDK, a plugin template, and documentation.

Nebula Lab reads `plugins-index.json` and `themes-index.json` directly from the root of this repository's `main` branch. Official plugin zips are published as assets of this repository's [`plugins` release](https://github.com/ptjworks/NebulaLab-Plugins/releases/tag/plugins).

This repository has moved to [PTJ Works](https://github.com/ptjworks/NebulaLab-Plugins); see the [organization migration notes](./docs/organization-migration.md) for the compatibility arrangements. Existing index entries, versions, checksums and author identities are unchanged.

Most documents linked below are in Chinese; the SDK API reference and the migration notes are in English.

## Installing Plugins and Themes (Users)

Install directly in Nebula Lab — no need to visit this repository:

- **Community → Plugin Store**: browse and install plugins (online)
- **Community → Theme Store**: browse and install themes (online)
- **Settings → Plugins → Install from Local**: install a plugin `.zip`
- **Settings → Appearance → Custom themes → Install from Local**: install a theme `.zip`

## Developing Plugins

| Document | Description |
|----------|-------------|
| [Getting Started](./docs/getting_started.md) | From setup to your first plugin |
| [SDK API Reference](./docs/api_reference.md) | `@op` decorator, `OperationContext` details |
| [Plugin Workspace Management](./docs/workspace_management.md) | Official plugin sources, marketplace index, releases and setting up a new machine |
| [Claude Code Skill](./skills/nebula-plugin-dev.md) | AI-assisted plugin development, including the panel message bridge and marketplace fields |

New plugins can start from the [`templates/plugin_template/`](./templates/plugin_template/) template.

## Developing Themes

| Document | Description |
|----------|-------------|
| [Claude Code Skill](./skills/nebula-theme-dev.md) | AI-assisted theme design with marketplace metadata and the full CSS variable reference |
| [Contributing Guide · Themes](./docs/contributing.md#提交主题到主题市场) | Theme packaging and publishing |

## Submitting to the Marketplace

See the [Contributing Guide](./docs/contributing.md) for full details.

**Plugins:** publish a release zip whose root (or single top-level folder) contains a `plugin.json` matching the index entry's `id` and `version` and declaring `operations`, `importers` or `panel` (`__init__.py` is required for operations/importers, the `.html` file for a panel) → add an entry to `plugins-index.json`, changing no other file → open a PR. CI checks the index format, downloads the referenced zip, and verifies its sha256, package structure and basic risk patterns. Required index fields: `id` (lowercase letters, digits, `-`, `_`), `name`, `version` (`x.y.z`), `source` (`official` or `community`), `download_url`, `homepage`, `sha256` (64 hex characters), plus `source_url` for community plugins and `author_github` with `author_url` (`https://github.com/<author_github>`) for official ones; `logo_url` is optional. All URLs must use `https://`.

**Themes:** publish a release zip whose root (or single top-level folder) contains a `theme.json` matching the index entry's `id`, `version`, `color_scheme` and `background_image_url` (if the index entry omits `background_image_url`, `theme.json` must omit it too) → add an entry to `themes-index.json`, changing no other file (otherwise theme validation fails) → open a PR. CI checks the index format, downloads the referenced zip, and verifies its sha256 and `theme.json`. Required index fields: `id`, `name`, `version`, `author`, `source`, `description`, `color_scheme` (`light` or `dark`), `download_url`, `sha256`, `homepage`, `preview_image_url`, `min_app_version`, `tags`, `accessibility_notes`; `background_image_url` is optional.

After CI passes, a maintainer must approve the PR before it is merged.

## Publishing Official Plugins (Maintainers)

Edit `plugins/official/<plugin-folder>/` and bump `version` in its `plugin.json`; on PRs that change plugin sources, CI validates each `plugin.json`, scans for dangerous calls and runs the tests under `tests/`. Then package the plugin and update its index entry (`--update-index` only rewrites `version`, `download_url` and `sha256` of an existing entry; add the entry by hand for a new plugin), upload the zip to the `plugins` release, and commit the index change:

```sh
python scripts/package_official_plugin.py <plugin-folder-or-id> --repo ptjworks/NebulaLab-Plugins --update-index
gh release upload plugins dist/plugins/<id>-<version>.zip --repo ptjworks/NebulaLab-Plugins
```

The zip name includes the version. Changing the sources without a version bump produces a same-named zip with a different sha256, and overwriting the uploaded asset breaks the existing index entry's checksum. If the upload fails because an asset with that name already exists, bump the version and repackage rather than overwriting it with `--clobber`.

The packager's `--repo` default still points at the pre-migration location, so pass `--repo ptjworks/NebulaLab-Plugins` explicitly for new packages; see the [organization migration notes](./docs/organization-migration.md).

## Security Notes

- Marketplace CI checks that the index entries match the zips actually uploaded (sha256, manifest `id` and version).
- This is automated integrity checking plus basic heuristic scanning, not a manual security audit.
- Before installing a community plugin, review its homepage, source repository and release contents.

## Repository Structure

```
NebulaLab-Plugins/
├── plugins-index.json          # Plugin marketplace index (read by the app)
├── themes-index.json           # Theme marketplace index (read by the app)
├── NebulaLab.code-workspace    # Local multi-root workspace: app + plugins
├── LICENSE                     # MIT License
├── plugins/official/           # Official plugin sources
├── assets/icons/               # Marketplace icons for official plugins
├── nebula_sdk/                 # Plugin development SDK (Python package)
├── templates/plugin_template/  # Plugin template
├── scripts/                    # Official plugin packaging, marketplace endpoint checks
├── tests/                      # Tests for official plugins and validators
├── docs/                       # Documentation
│   ├── getting_started.md      # Getting started guide
│   ├── api_reference.md        # SDK API reference
│   ├── workspace_management.md # Local repository layout and machine setup
│   ├── contributing.md         # Contributing guide (plugins + themes)
│   └── organization-migration.md # Compatibility arrangements for the PTJ Works move
├── skills/                     # AI-assisted development skills
│   ├── nebula-plugin-dev.md    # Plugin development skill
│   └── nebula-theme-dev.md     # Theme development skill
└── .github/
    ├── scripts/                # CI validation scripts
    └── workflows/              # CI: validate indexes, release assets and plugin sources on PRs
```
