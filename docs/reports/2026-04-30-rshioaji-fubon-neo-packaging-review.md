# rshioaji vs Fubon Neo SDK packaging review

Date: 2026-04-30

## Scope

Compare packaging details for:

- `rshioaji==1.5.7` from PyPI
- Fubon Neo SDK `fubon_neo==2.2.8` downloaded from official Fubon SDK URLs

Inputs inspected:

- PyPI JSON metadata for `rshioaji==1.5.7`
- Fubon download index: `https://www.fbs.com.tw/TradeAPI/docs/download/download-sdk.txt`
- Downloaded Linux/Windows/macOS wheels and extracted contents
- Extracted Node.js and Go SDK packages from Fubon download index
- Local artifacts under `/root/.openclaw/workspace/.state/neoapi-rshioaji-analysis/artifacts/`

## Verdict

Both packages use the same broad architecture: **native Rust-like compiled core + thin Python wrapper using CPython `abi3` wheels**.

They optimize for different product goals:

- `rshioaji` packages a large self-contained Python product: native core, Python compatibility modules, a standalone CLI/server binary, type stubs, and SBOM.
- `fubon_neo` packages a smaller broker SDK core: native extension plus thin Python wrappers, and delegates market-data REST/WebSocket surfaces to `fugle-marketdata>=2.4.1`.

For agent-assisted development, `rshioaji` is easier to inspect because it ships `_core.pyi`, richer metadata, and CycloneDX SBOM. `fubon_neo` is much smaller and cleaner at runtime, but less self-describing: no `.pyi` stub, no SBOM, minimal wheel metadata, and most API surface is hidden inside the native extension.

## Artifact summary

### rshioaji 1.5.7

Linux wheel inspected:

- Wheel: `rshioaji-1.5.7-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`
- Package size: about 36 MB
- Native Python core: `shioaji/_core.abi3.so`, about 48 MB
- CLI/server binary: `rshioaji-1.5.7.data/scripts/shioaji`, about 49 MB
- Python files: 12
- Stub files: 2, including `shioaji/_core.pyi` about 83 KB
- RECORD entries: 20
- SBOM: `rshioaji-1.5.7.dist-info/sboms/shioaji-python.cyclonedx.json`, about 740 KB, 572 components in earlier inspection
- Metadata summary: `Summary: Rust implementation of Shioaji trading API for Taiwan financial markets`
- Requires-Python: `>=3.7`
- Requires-Dist: optional `uvloop` extra for speed; test extras only otherwise

Observed Linux dynamic dependencies:

- `_core.abi3.so`: `libm`, `libc`, `ld-linux`, `libpthread`, `libdl`, `librt`
- CLI binary: `libgcc_s`, `libm`, `libc`

### Fubon Neo 2.2.8 Python SDK

Linux wheel inspected:

- Official zip: `fubon_neo-2.2.8-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.zip`
- Inner wheel: `fubon_neo-2.2.8-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`
- Zip size: about 4.8 MB
- Wheel size: about 4.9 MB
- Native Python core: `fubon_neo/_fubon_neo.abi3.so`, about 12.4 MB
- Python wrapper files: 7
- Stub files: 0
- RECORD entries: 11
- SBOM: not found in inspected wheel
- Requires-Python: `>=3.7`
- Requires-Dist: `fugle-marketdata>=2.4.1`
- Classifiers include Rust and CPython/PyPy

Observed Linux dynamic dependencies:

- `_fubon_neo.abi3.so`: `libpthread`, `libc`, `libdl`, `ld-linux`

### Fubon multi-language SDKs

From official download index:

- Python wheels: Linux, Windows, macOS x86_64, macOS arm64
- Node.js package: `fubon-neo-2.2.8.tgz`, about 19 MB after zip extraction
- Go SDK package: `fubon-go-sdk-2.2.8.tar.gz`, about 13.4 MB
- C# nupkg zip
- C++ SDK package

Node package contains platform-specific native `.node` binaries for Linux/macOS/Windows plus JS/TS wrappers and `.d.ts` files.

Go package contains Go wrapper code plus platform-specific native shared libraries (`libfubon-x64.so`, dylibs, DLL) and headers.

## Layout comparison

| Dimension | rshioaji | Fubon Neo |
|---|---|---|
| Python distribution | PyPI wheels | Official website zip wrapping wheels |
| Source distribution | No sdist found in PyPI inspection | No source distribution in official download inspection |
| Native core | `shioaji/_core.abi3.so` / `.pyd` | `fubon_neo/_fubon_neo.abi3.so` / `.pyd` |
| ABI | `cp37-abi3` | `cp37-abi3` |
| Linux tag | manylinux2014 / manylinux_2_17 | manylinux2014 / manylinux_2_17 |
| Python wrapper depth | Moderate wrapper modules + compatibility shims | Very thin wrappers around native core |
| Type information | Full `_core.pyi` | No `.pyi` found |
| CLI/server | Bundled standalone `shioaji` binary | No equivalent Python wheel CLI found |
| SBOM | CycloneDX SBOM included | No SBOM found |
| External dependency posture | Mostly self-contained; optional extras | Depends on `fugle-marketdata>=2.4.1` for market data client |
| Multi-language packaging | HTTP server/CLI enables multi-language clients | Separate SDK packages for Node/Go/C#/C++ |

## Strengths and tradeoffs

### rshioaji strengths

- Very self-describing package: `_core.pyi` exposes the API surface to IDEs, type checkers, and agents.
- SBOM improves supply-chain visibility.
- CLI/server binary makes REST/SSE and non-Python integration first-class.
- PyPI distribution simplifies installation and pinning.
- Rich Python metadata and docs lower migration/debugging cost.

### rshioaji tradeoffs

- Wheels are large because the package includes both Python native module and standalone CLI/server binary.
- More bundled surface means more supply-chain and runtime attack surface to audit.
- No source distribution was found, so core Rust implementation remains opaque from PyPI alone.

### Fubon Neo strengths

- Smaller Python wheel and simpler wheel layout.
- Clean separation: trading SDK core in `fubon_neo`; market data surfaces delegated to `fugle-marketdata`.
- Official download page provides multiple platform/language SDKs.
- `abi3` wheel strategy is good for broad Python version support.
- Thin Python wrapper may reduce Python-level compatibility burden.

### Fubon Neo tradeoffs

- No `.pyi` stub in inspected wheel; agents and IDEs cannot discover native API signatures from package files.
- Minimal wheel metadata; no package summary and no project URLs observed in `METADATA`.
- No SBOM found, reducing dependency/security transparency.
- Official website zip distribution is less standard than PyPI for Python dependency management.
- Multi-language SDKs are separate downloads rather than one HTTP/CLI integration surface, which increases documentation and release synchronization burden.

## Packaging improvement recommendations for NeoAPI

### Must-fix / high ROI

1. **Ship `.pyi` stubs for `fubon_neo._fubon_neo` and public wrappers.**
   - This is the biggest improvement for agent-assisted coding and migration.
   - It lets users inspect method signatures without reverse engineering native binaries.

2. **Publish or mirror Python wheels through a standard package index.**
   - Even if official website remains canonical, a package-index-compatible path improves pinning, install reproducibility, and CI.

3. **Add CycloneDX SBOM to wheel `dist-info/sboms/`.**
   - rshioaji already does this; Neo should match or exceed it.

4. **Add richer `METADATA`.**
   - Include summary, license, homepage, docs URL, download URL, and project URLs.

5. **Document binary/source boundary explicitly.**
   - State that source is not bundled in wheel and which APIs are public/stable.

### Should-fix

1. Add a `console_scripts` diagnostic command, even if not a full server:
   - e.g. version, environment check, cert path validation, endpoint mode check.
2. Add a lightweight package inventory/checksum manifest to official download index.
3. Keep Node/Go/Python version numbers synchronized and machine-readable in the download index.
4. Add `py.typed` if Python-visible wrapper types become annotated.
5. Publish platform support matrix in package metadata/docs, not only in a web page.

## Agent-use implications

For Shioaji migration work, agents can inspect rshioaji's `_core.pyi` and infer exact callable surfaces. For NeoAPI, agents must rely on official docs, `llms-full.txt`, wrapper files, and empirical tests because native method signatures are hidden.

Therefore, Neo skill docs should compensate by being more explicit than normal docs:

- include verified call signatures,
- include response-shape examples,
- mark version-specific behavior,
- and cite official source anchors for every mapping row.

## Evidence artifacts

Local analysis artifacts:

- `/root/.openclaw/workspace/.state/neoapi-rshioaji-analysis/artifacts/package_metadata_summary.json`
- `/root/.openclaw/workspace/.state/neoapi-rshioaji-analysis/artifacts/dynamic_deps.txt`
- `/root/.openclaw/workspace/.state/neoapi-rshioaji-analysis/artifacts/all_extract_inventory_after_nested.txt`
- `/root/.openclaw/workspace/.state/neoapi-rshioaji-analysis/artifacts/fubon_download_sdk.txt`
- `/root/.openclaw/workspace/.state/neoapi-rshioaji-analysis/artifacts/binary_strings_selected.txt`

## Limits

- This is packaging analysis, not binary reverse engineering.
- No source distribution was found for either core implementation in the inspected channels.
- Native symbols/strings were inspected only for packaging-level clues, not for implementation correctness.
