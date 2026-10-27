"""Base abstractions and data structures for code generators.

Defines the `GeneratedFile` output container and the `SlopGenerator` abstract base class
that all language-specific code generators implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GeneratedFile:
    """Container holding synthesized code file metadata and payload.

    Attributes:
        filename: Relative file path for disk output, including subfolder and extension.
        content: Full text source code content of the generated file.
        line_count: Total line count of `content`.
    """

    filename: str
    content: str
    line_count: int


class SlopGenerator(ABC):
    """Abstract base class defining the generator contract for synthetic code output.

    Attributes:
        name: Short identifier for the generator (e.g. 'c_slop', 'enterprise_java').
        language: Programming language category (e.g. 'c', 'java', 'rust').
        extension: Source file extension including leading period (e.g. '.c', '.java').
    """

    name: str
    language: str
    extension: str

    @abstractmethod
    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Synthesize a complete source file adhering to the generator's language paradigms.

        Args:
            sanity: Floating-point value in [0.0, 1.0] controlling chaos versus enterprise style.
            file_index: Monotonically increasing index used to disambiguate generated file names.

        Returns:
            A `GeneratedFile` instance with filename, code content, and calculated line count.
        """
        ...
