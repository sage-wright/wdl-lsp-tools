# wdl-lsp-tools

wdl-lsp-tools provides two small language servers for WDL (Workflow Description Language) files. They were written for the [Zed WDL extension](https://github.com/sage-wright/zed-wdl), which downloads them automatically, but they speak plain LSP (Language Server Protocol) over stdin/stdout and can be used with any editor. Both use only the Python standard library and need Python 3.8 or newer.

## `wdl-command-lint`

`wdl-command-lint` runs [ShellCheck](https://github.com/koalaman/shellcheck) on the bash in each WDL `command` block and [Ruff](https://github.com/astral-sh/ruff) on the Python heredocs inside them, and reports the results as diagnostics on the WDL file. WDL placeholders (`~{...}`) are replaced with code of the same length before linting, so positions map straight back onto the WDL file without placeholder false positives.

It is configured with environment variables:

| Variable | Description |
|---|---|
| `SHELLCHECK_BIN` | Path to `shellcheck`. Unset turns ShellCheck off. |
| `SHELLCHECK_EXCLUDE` | Comma-separated ShellCheck codes to ignore, e.g. `SC2086,SC2034`. |
| `SHELLCHECK_SEVERITY` | Minimum severity: `error`, `warning`, `info`, or `style`. |
| `RUFF_BIN` | Path to `ruff`. Unset turns Ruff off. |
| `RUFF_IGNORE` | Comma-separated Ruff rules to ignore. |

With neither tool set, the server starts but reports nothing.

## `sprocket-filtered`

`sprocket-filtered` runs [Sprocket](https://github.com/stjude-rust-labs/sprocket) as a language server and drops diagnostics whose message matches a regular expression (by default, Sprocket's `type mismatch: ...` errors). All arguments are passed to Sprocket unchanged, e.g. `sprocket-filtered analyzer --stdio`. It also sends pull-diagnostic requests to Sprocket one at a time, because Sprocket (0.28 through 0.32 at least) stops answering requests once more are in flight than the machine has CPU cores.

| Variable | Description |
|---|---|
| `SPROCKET_BIN` | Path to `sprocket` (default: `sprocket` on `PATH`). |
| `SPROCKET_HIDE_DIAGNOSTICS` | Regular expression for the messages to drop (default: `^type mismatch`). |

## Installation

Install from [PyPI](https://pypi.org/project/wdl-lsp-tools/) with `uv tool install wdl-lsp-tools` or `pipx install wdl-lsp-tools`, which puts both commands on your `PATH`. Each [GitHub release](https://github.com/sage-wright/wdl-lsp-tools/releases) also includes `wdl-lsp-tools.pyz`, a single-file zipapp that runs either command without installing anything:

```bash
python3 wdl-lsp-tools.pyz wdl-command-lint
python3 wdl-lsp-tools.pyz sprocket-filtered analyzer --stdio
```

## Releasing

Releases are built and published by GitHub Actions when a version tag is pushed. Update `__version__` in `src/wdl_lsp_tools/__init__.py`, then either push a tag with the same version (e.g. `v0.1.0`) or create a release with that tag on GitHub. The workflow publishes to PyPI and attaches the wheel, sdist, and `wdl-lsp-tools.pyz` to the release, creating the release if it doesn't exist yet.

## License

BSD-3-Clause. See [LICENSE](LICENSE).
