"""Performance tracking and session telemetry for codemaxxing.

Maintains running counters for lines generated, files written, and git commits executed,
calculating throughput rates such as lines per second and commits per minute.
"""

import time


class Stats:
    """Runtime telemetry tracker for generation sessions and turbo loops.

    Attributes:
        start_time: Monotonic unix timestamp recording when tracking began.
        total_lines: Cumulative count of code lines produced across all files.
        total_commits: Cumulative count of git commits executed in turbo mode.
        total_files: Cumulative count of distinct files written to disk.
    """

    def __init__(self) -> None:
        """Initialize timing markers and reset volume counters to zero."""
        self.start_time = time.time()
        self.total_lines = 0
        self.total_commits = 0
        self.total_files = 0

    def add(self, lines: int, files: int, commits: int = 0) -> None:
        """Increment running line, file, and commit counters.

        Args:
            lines: Number of lines generated in the latest batch.
            files: Number of files produced in the latest batch.
            commits: Number of git commits made in the latest batch (default: 0).
        """
        self.total_lines += lines
        self.total_files += files
        self.total_commits += commits

    @property
    def elapsed(self) -> float:
        """Return elapsed duration in seconds since session creation."""
        return time.time() - self.start_time

    @property
    def elapsed_str(self) -> str:
        """Return formatted elapsed duration as an HH:MM:SS string."""
        e = int(self.elapsed)
        h, m, s = e // 3600, (e % 3600) // 60, e % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @property
    def lines_per_sec(self) -> float:
        """Calculate the average code generation throughput in lines per second."""
        e = self.elapsed
        return self.total_lines / e if e > 0 else 0

    @property
    def commits_per_min(self) -> float:
        """Calculate commit frequency throughput in commits per minute."""
        e = self.elapsed / 60
        return self.total_commits / e if e > 0 else 0

    def display(self, mode: str = "TURBO") -> str:
        """Format an in-progress status line for carriage-return terminal updates.

        Args:
            mode: Operational mode label to show in the status bar (e.g. 'TURBO').

        Returns:
            A single formatted string with line, commit, file, throughput, and elapsed stats.
        """
        return (
            f"\r[{mode}] {self.total_lines:,} lines | "
            f"{self.total_commits:,} commits | "
            f"{self.total_files:,} files | "
            f"{self.lines_per_sec:,.0f} lines/sec | "
            f"{self.commits_per_min:.1f} commits/min | "
            f"{self.elapsed_str} elapsed"
        )

    def summary(self) -> str:
        """Format a multi-line final summary report banner.

        Returns:
            A formatted multi-line ASCII banner detailing all final session metrics.
        """
        return (
            f"\n{'='*60}\n"
            f"  CODEMAXXING SESSION COMPLETE\n"
            f"{'='*60}\n"
            f"  Total lines:   {self.total_lines:>12,}\n"
            f"  Total files:   {self.total_files:>12,}\n"
            f"  Total commits: {self.total_commits:>12,}\n"
            f"  Duration:      {self.elapsed_str:>12}\n"
            f"  Lines/sec:     {self.lines_per_sec:>12,.0f}\n"
            f"  Commits/min:   {self.commits_per_min:>12.1f}\n"
            f"{'='*60}\n"
        )
