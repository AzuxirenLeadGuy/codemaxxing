# codemaxxing Developer Documentation

## Overview

`codemaxxing` is a Python package that generates large volumes of synthetic source code. The project creates code that looks convincingly enterprise-grade or unmistakably chaotic, while focusing on code volume, naming patterns, and repository churn.

The package is designed around a small set of runtime configuration values, a generator registry, and per-language implementations that emit code to disk in a predictable layout.

## Repository layout

- `README.md` — project overview and quick-start instructions
- `DOCS.md` — contributor-facing developer documentation
- `pyproject.toml` — packaging metadata and CLI entry points
- `src/codemaxxing/` — Python package root
- `src/codemaxxing/generators/` — language-specific code generation implementations

## Supported output families

The project currently includes generator implementations for:

- Java
- Python
- JavaScript / TypeScript
- Go
- Generic Python slop
- C
- C#
- C++
- Haskell
- Kotlin
- Lua
- PHP
- Ruby
- Rust
- Swift
- Zig

## Typical commands

```bash
# standard generation
codemaxxing --lines 10000 --sanity 50

# full chaos
codemaxxing --lines 10000 --sanity 0

# enterprise mode
codemaxxing --lines 10000 --enterprise

# language-specific slop
codemaxxing --lines 5000 --lang java --sanity 80
codemaxxing --lines 8000 --lang rust --sanity 73
codemaxxing --lines 12000 --lang kotlin --sanity 67
```

## Extending the project

When contributing, the usual work is one of the following:

- improve random naming fidelity
- add a new language generator
- tune generation volume or layout
- improve docs and contributor onboarding
- make generated output more realistic while preserving the repository’s tone

## Notes

Documentation here is meant to help future developers navigate the structure without needing to reverse-engineer the generator design from output files alone.
