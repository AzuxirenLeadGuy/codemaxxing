"""Configuration models for synthetic code generation runs.

Defines the runtime parameters governing generated volume, language selection,
chaos vs corporate styling balance, output destinations, and turbo git options.
"""

from dataclasses import dataclass


@dataclass
class GenerationConfig:
    """Runtime configuration settings for code generation sessions.

    Attributes:
        lines: Target number of code lines to generate across all output files.
        sanity: Floating-point value between 0.0 and 1.0 controlling code tone.
            0.0 produces unhinged chaos and brainrot slang, while 1.0 produces
            strict enterprise design patterns, boilerplate, and corporate jargon.
        lang: Target programming language or 'all' to cycle through all supported generators.
        output_dir: Destination directory path on the local filesystem for generated files.
        turbo: Flag indicating whether to run in turbo mode (generate, git add, git commit loop).
        enterprise: Multiplies target line count by 10 to simulate enterprise codebases.
        batch_size: Number of files generated per commit batch in turbo mode.
        push_every: Number of commits between automatic git pushes (0 disables auto-push).
        forever: Flag indicating whether turbo generation should run continuously until interrupted.
        branch: Target git branch name to checkout/commit to instead of a temporary branch.
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

    def __post_init__(self) -> None:
        """Validate and adjust configuration attributes post-initialization.

        Clamps the sanity parameter to the [0.0, 1.0] interval and applies
        the enterprise 10x volume multiplier to lines if enterprise mode is enabled.
        """
        self.sanity = max(0.0, min(1.0, self.sanity))
        if self.enterprise:
            self.lines *= 10
