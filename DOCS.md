# codemaxxing Developer Documentation

## Overview

`codemaxxing` is a Python package that generates large volumes of synthetic source code. The project is intentionally absurd: it creates code that looks convincingly enterprise-grade or unmistakably chaotic, while focusing on code volume, naming patterns, and repository churn.

The package is designed around a small set of runtime configuration values, a generator registry, and per-language implementations that emit code to disk in a predictable layout.

## Repository layout

- `README.md` — project overview and quick-start instructions
- `DOCS.md` — contributor-facing developer documentation
- `pyproject.toml` — packaging metadata and CLI entry points
- `src/codemaxxing/` — Python package root
- `src/codemaxxing/generators/` — language-specific code generation implementations

## Package responsibilities

### `src/codemaxxing/__init__.py`

Defines package metadata and exposes the package version.

### `src/codemaxxing/__main__.py`

Parses CLI arguments and routes execution into either standard generation mode or turbo mode.

### `src/codemaxxing/config.py`

Contains `GenerationConfig`, the dataclass that controls the runtime behavior of a generation run.

Important fields include:

- `lines`: target line count
- `sanity`: 0.0–1.0 scale controlling chaos vs enterprise styling
- `lang`: target language or `all`
- `output_dir`: directory for generated files
- `turbo`: whether to run turbo generation
- `enterprise`: multiplies line count by 10
- `batch_size`: file count for turbo batches
- `push_every`: auto-push frequency
- `forever`: continuous mode
- `branch`: branch used during generation

### `src/codemaxxing/generator.py`

Coordinates the generation process.

Responsibilities:

- select generators based on the requested language
- rotate generators for `all` mode
- create output manifests
- write generated files to disk

### `src/codemaxxing/comments.py`

Provides random corporate or chaotic comments and docstrings. These are used to make generated files feel authentic while keeping the output intentionally noisy.

### `src/codemaxxing/naming.py`

Generates names for classes, methods, package namespaces, variables, and commit messages. The naming module intentionally blends corporate terminology with chaotic slang.

### `src/codemaxxing/stats.py`

Tracks runtime statistics such as elapsed time, generated lines, files, and commit throughput. These values are used in turbo output and session summaries.

## Generator system

The generator registry lives in `src/codemaxxing/generators/__init__.py`. Each implementation subclasses `SlopGenerator` from `src/codemaxxing/generators/base.py`.

The base interface is intentionally minimal:

```python
class SlopGenerator(ABC):
    @abstractmethod
    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        ...
```

Each generator writes a `GeneratedFile` object with:

- `filename`
- `content`
- `line_count`

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

This project is deliberately synthetic. The code generation pipeline is the real product. Documentation here is meant to help future developers navigate the structure without needing to reverse-engineer the generator design from output files alone.
