# codemaxxing

The world's first artisanally handcrafted, enterprise-grade slop generation CLI tool for maximizing your GitHub contribution graph. Because quantity is quality.

## Developer documentation

See [DOCS.md](DOCS.md) for an architecture overview, file-by-file walkthrough, and contributor onboarding notes.

## Installation

```bash
git clone https://github.com/jshchnz/codemaxxing.git
cd codemaxxing
pip install .
```

## Quick Start

```bash
# Generate 10,000 lines of corporate enterprise slop
codemaxxing --lines 10000 --sanity 100

# Generate 10,000 lines of pure unhinged chaos
codemaxxing --lines 10000 --sanity 0

# TURBO MODE: auto-generate and auto-commit in a tight loop
codemaxxing --lines 100000 --turbo --sanity 50

# Enterprise mode (10x multiplier because enterprise)
codemaxxing --lines 10000 --enterprise

# Target specific languages
codemaxxing --lines 5000 --lang java --sanity 80
codemaxxing --lines 8000 --lang rust --sanity 73
codemaxxing --lines 12000 --lang csharp --sanity 91
```

## Features

### `--sanity` (0-100)

Controls the chaos level of generated code.

### `--turbo`

Generates files, stages them, and commits in a loop.

### `--enterprise`

Multiplies your target line count by 10x.

## Contributing

This repository intentionally produces noisy, synthetic code. Developer documentation is focused on understanding the generation pipeline, file layout, and how to evolve or extend the generators responsibly.

## License

MIT SSL (Special Slop License).
