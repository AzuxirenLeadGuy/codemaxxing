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

## General Project Structure

The `codemaxxing` architecture is organized into four main layers: Configuration & CLI, Pipeline Orchestration, Synthetic Token Generation, and the Pluggable Generator Subsystem.

```
codemaxxing/
├── pyproject.toml              # Build & packaging configuration
├── README.md                   # User guide & quick start
├── DOCS.md                     # Contributor & architecture documentation
└── src/
    └── codemaxxing/
        ├── __init__.py         # Package metadata & version
        ├── __main__.py         # CLI argument parser & command dispatcher
        ├── config.py           # GenerationConfig dataclass
        ├── generator.py        # Core generation orchestrator & disk writer
        ├── naming.py           # Synthetic identifier & commit message generator
        ├── comments.py         # Code comments & docstring generator
        ├── stats.py            # Performance metrics & throughput tracker
        └── generators/         # Language generator plugin subsystem
            ├── __init__.py     # Generator registry & lookup mapping
            ├── base.py         # SlopGenerator ABC & GeneratedFile container
            ├── c_slop.py
            ├── cpp_enterprise.py
            ├── csharp_enterprise.py
            ├── enterprise_java.py
            ├── enterprise_python.py
            ├── generic.py
            ├── go_slop.py
            ├── haskell_chaos.py
            ├── javascript.py
            ├── kotlin_enterprise.py
            ├── lua_chaos.py
            ├── php_enterprise.py
            ├── ruby_chaos.py
            ├── rust_enterprise.py
            ├── swift_enterprise.py
            └── zig_enterprise.py
```

### Module Responsibilities

#### 1. CLI & Configuration Layer
- **`src/codemaxxing/__main__.py`**: Contains the `main()` CLI entrypoint. Uses `argparse` to parse command-line arguments (target line count, sanity level, language selection, turbo flag, enterprise mode, batch size, and auto-push frequency) and constructs a `GenerationConfig`. Routes execution to standard generation or turbo commit mode.
- **`src/codemaxxing/config.py`**: Declares `GenerationConfig`, the central runtime configuration dataclass. Clamps the `sanity` parameter to `[0.0, 1.0]` and applies the 10x multiplier to `lines` when `enterprise` mode is enabled.

#### 2. Pipeline Orchestration & Output
- **`src/codemaxxing/generator.py`**: Coordinates the entire generation workflow.
  - `_generator_sequence`: Generates a deterministic round-robin generator sequence to ensure every language is represented before cycling randomly.
  - `generate`: Iteratively calls generator instances until the cumulative line count meets or exceeds `config.lines`.
  - `generate_batch`: Generates a fixed batch of files for a turbo commit step.
  - `write_files`: Writes generated file buffers to disk under the specified output directory, creating subfolders as needed.
  - `_write_manifest`: Generates `codemaxxing_manifest.md` inside the output directory, providing a summary breakdown of total files, lines, and per-language file inventories.

#### 3. Synthetic Syntax & Token Generation
- **`src/codemaxxing/naming.py`**: Provides deterministic, weighted pseudo-random name generators:
  - `_blend`: Chooses between corporate enterprise word banks and chaotic brainrot/hacker dictionaries based on `sanity`.
  - `class_name`: Generates PascalCase class names using corporate prefixes, nouns, and enterprise suffixes or chaotic slang.
  - `method_name` & `var_name`: Generates function and variable identifiers.
  - `java_package` & `go_package`: Synthesizes package hierarchy paths.
  - `commit_message`: Produces enterprise conventional commits or humorous chaotic messages.
- **`src/codemaxxing/comments.py`**: Emits comments and docstrings:
  - `comment`: Selects single-line comments from corporate or chaos pools.
  - `docstring`: Generates component-specific docstrings.
  - `block_comment`: Creates multi-line comment blocks using target-language comment prefixes.

#### 4. Metrics & Telemetry
- **`src/codemaxxing/stats.py`**: Contains `Stats`, which tracks elapsed time, generated line counts, file counts, and git commits. Computes live throughput rates (`lines_per_sec`, `commits_per_min`) and formats real-time carriage-return progress bars and final summary reports.

#### 5. Pluggable Generator Subsystem (`src/codemaxxing/generators/`)
- **`base.py`**:
  - `GeneratedFile`: Data container holding `filename` (relative path including language directory), `content` (source code text), and `line_count`.
  - `SlopGenerator`: Abstract base class defining `name`, `language`, `extension`, and the abstract `generate(sanity: float, file_index: int) -> GeneratedFile` method.
- **`__init__.py`**: Houses the generator registry (`ALL_GENERATORS`), language alias mapping (`LANG_MAP`), and the `get_generators(lang: str) -> list` factory function.
- **Language Implementations (16 generators)**:
  - `c_slop.py`: Procedural C with state enum machines, typedef structs, and memory buffers.
  - `cpp_enterprise.py`: Modern C++ with abstract contract interfaces, RAII containers, and namespaces.
  - `csharp_enterprise.py`: C# with file-scoped namespaces, sealed records, async Task interfaces, and builders.
  - `enterprise_java.py`: Verbose enterprise Java with package hierarchies, Javadoc annotations, getters/setters, and static builders.
  - `enterprise_python.py`: Metaclass-heavy Python with abstract base classes, type annotations, and context managers.
  - `generic.py`: Generic Python demonstrating deep nested if-else ladders, recursive wrapper chains, massive enums, and unittest test cases.
  - `go_slop.py`: Go with interface types, infinite `if err != nil` error handling checks, and goroutine/channel mechanics.
  - `haskell_chaos.py`: Pure functional Haskell with algebraic data types, typeclasses, and Maybe/Either pipelines.
  - `javascript.py`: JavaScript and TypeScript with callback pyramids, chained Promises, and module exports.
  - `kotlin_enterprise.py`: Kotlin with data classes, gateway interfaces, sealed lifecycle enums, and concurrent maps.
  - `lua_chaos.py`: Lua scripts featuring metatable-based pseudo-classes, method chaining, and state tables.
  - `php_enterprise.py`: Modern PSR-compliant PHP with namespaces, interface contracts, traits, and typed properties.
  - `ruby_chaos.py`: Ruby modules with frozen string literals, class definitions, `attr_accessor` symbols, and telemetry arrays.
  - `rust_enterprise.py`: Safe Rust code with inner module documentation, traits, Result/Option handling, and unit tests.
  - `swift_enterprise.py`: Protocol-oriented Swift with payload structs, lifecycle enums, and class extensions.
  - `zig_enterprise.py`: Zig with explicit memory allocator passing, tagged state enums, and struct lifecycles.

### Data Flow and Execution Lifecycle

1. **Invocation**: The user invokes the CLI (e.g. `codemaxxing --lines 10000 --lang all --sanity 80`).
2. **Configuration**: `__main__.py` parses arguments into a `GenerationConfig`, normalizing `sanity` and scaling lines for enterprise mode if requested.
3. **Generator Resolution**: `get_generators()` matches the requested language against `LANG_MAP`.
4. **Generation Loop**: `generate()` runs the generators. If `--lang all` is requested, `_generator_sequence` first invokes every generator once, then randomly selects generators until the target line threshold is met.
5. **Disk Emission & Manifest**: `write_files()` creates language directories under the output folder, writes file contents, and emits an updated `codemaxxing_manifest.md` detailing the file breakdown.


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
