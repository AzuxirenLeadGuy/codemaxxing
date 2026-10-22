"""Core generation pipeline for codemaxxing.

This module selects the active generator strategy, creates files until the
requested line target is reached, and writes generated output to disk.
"""

import os
import random

from collections import defaultdict

from codemaxxing.config import GenerationConfig
from codemaxxing.generators import get_generators
from codemaxxing.generators.base import GeneratedFile
from codemaxxing.generators.base import SlopGenerator


def _generator_sequence(
    generators: list[SlopGenerator],
    count: int,
    start_offset: int = 0,
) -> list[SlopGenerator]:
    """Build a deterministic sequence of generators with rotation support.

    Args:
        generators: The active generator set.
        count: Desired number of generators in the sequence.
        start_offset: Offset used to rotate the starting position.

    Returns:
        A rotated list of generator instances.
    """
    if not generators or count <= 0:
        return []

    sequence: list[SlopGenerator] = []
    ordered = generators[:]
    rotation = start_offset % len(ordered)
    ordered = ordered[rotation:] + ordered[:rotation]

    while len(sequence) < count:
        if len(sequence) < len(ordered):
            sequence.append(ordered[len(sequence)])
        else:
            sequence.append(random.choice(generators))

    return sequence


def generate(config: GenerationConfig) -> list[GeneratedFile]:
    """Generate a list of files that meets the requested line target.

    Args:
        config: Runtime generation configuration.

    Returns:
        A list of generated file descriptors ready to be written to disk.
    """
    generators = get_generators(config.lang)
    files: list[GeneratedFile] = []
    total_lines = 0
    file_index = 0

    if config.lang == "all":
        guaranteed = _generator_sequence(generators, len(generators))
        for gen in guaranteed:
            result = gen.generate(config.sanity, file_index)
            files.append(result)
            total_lines += result.line_count
            file_index += 1

    while total_lines < config.lines:
        gen = random.choice(generators)
        result = gen.generate(config.sanity, file_index)
        files.append(result)
        total_lines += result.line_count
        file_index += 1

    return files


def generate_batch(config: GenerationConfig, batch_size: int, start_index: int) -> list[GeneratedFile]:
    """Generate a compact batch of files for turbo mode.

    Args:
        config: Runtime generation configuration.
        batch_size: Number of files to emit in this batch.
        start_index: Starting file index to use for naming.

    Returns:
        A list of generated file descriptors.
    """
    generators = get_generators(config.lang)
    files: list[GeneratedFile] = []
    sequence: list[SlopGenerator] = []

    if config.lang == "all":
        sequence = _generator_sequence(generators, batch_size, start_index)

    for i in range(batch_size):
        gen = random.choice(generators)
        if sequence:
            gen = sequence[i]
        result = gen.generate(config.sanity, start_index + i)
        files.append(result)

    return files


def _write_manifest(files: list[GeneratedFile], output_dir: str, total_lines: int) -> None:
    """Write a summary manifest describing generated files and line counts."""
    by_language: dict[str, dict[str, int]] = defaultdict(lambda: {"files": 0, "lines": 0})
    for generated in files:
        language = generated.filename.split("/", 1)[0]
        by_language[language]["files"] += 1
        by_language[language]["lines"] += generated.line_count

    manifest_lines = [
        "# codemaxxing manifest",
        "",
        f"total files: {len(files)}",
        f"total lines: {total_lines}",
        "",
        "## language breakdown",
        "",
    ]
    for language in sorted(by_language):
        entry = by_language[language]
        manifest_lines.append(
            f"- {language}: {entry['files']} files / {entry['lines']} lines"
        )

    manifest_lines.extend([
        "",
        "## generated files",
        "",
    ])
    for generated in files:
        manifest_lines.append(f"- {generated.filename} ({generated.line_count} lines)")

    manifest_path = os.path.join(output_dir, "codemaxxing_manifest.md")
    with open(manifest_path, "w") as manifest:
        manifest.write("\n".join(manifest_lines) + "\n")


def write_files(files: list[GeneratedFile], output_dir: str) -> int:
    """Persist generated file objects to disk and return their total size.

    Args:
        files: Generated file descriptors to write.
        output_dir: Destination folder for the generated output.

    Returns:
        The cumulative number of lines written.
    """
    total_lines = 0
    for f in files:
        path = os.path.join(output_dir, f.filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(f.content)
        total_lines += f.line_count

    _write_manifest(files, output_dir, total_lines)
    return total_lines
