"""Runtime configuration for generated slop output.

This module defines the centralized configuration object used by the generator
pipeline and the CLI entry point.
"""

from dataclasses import dataclass


@dataclass
class GenerationConfig:
    """Describe how a generated slop session should behave.

    Attributes:
        lines: Target total number of lines to generate.
        sanity: Ratio between 0.0 and 1.0 controlling corporate vs chaotic tone.
        lang: Language identifier or `all`.
        output_dir: Directory where generated files are written.
        turbo: Whether to run the turbo generation loop.
        enterprise: Whether to scale generation by 10x.
        batch_size: Number of files per turbo batch.
        push_every: Automatically push every N commits.
        forever: Keep generating until interrupted.
        branch: Existing branch to use when running in CI or projection mode.
    """

    lines: int = 10000
    sanity: float = 0.5  # 0.0 = full chaos, 1.0 = corporate cringe
    lang: str = "all"
    output_dir: str = "./output"
    turbo: bool = False
    enterprise: bool = False
    batch_size: int = 15
    push_every: int = 0  # auto-push every N commits (0 = never)
    forever: bool = False  # run indefinitely
    branch: str = ""  # use existing branch instead of creating new one

    def __post_init__(self):
        """Clamp the sanity level and apply enterprise scaling."""
        self.sanity = max(0.0, min(1.0, self.sanity))
        if self.enterprise:
            self.lines *= 10
