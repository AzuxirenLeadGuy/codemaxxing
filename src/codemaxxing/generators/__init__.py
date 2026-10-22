"""Abstract interfaces shared by all slop generators.

This module defines the base types used by the generator registry and the file
writer pipeline.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GeneratedFile:
    """Describe one generated output artifact.

    Attributes:
        filename: Relative file path within the output directory.
        content: Rendered source code string.
        line_count: Number of newline-delimited lines in the output file.
    """

    filename: str
    content: str
    line_count: int


class SlopGenerator(ABC):
    """Abstract base class that all language generators implement."""

    name: str
    language: str
    extension: str

    @abstractmethod
    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Render one generated file for the selected language and style."""
        ...
