"""Session statistics for generated output reports.

The Stats class tracks elapsed time and volume metrics so that the CLI can show
friendly progress and summary information during generation or turbo loops.
"""

import time


class Stats:
    """Track runtime metrics for a generation session."""

    def __init__(self):
        """Initialize timing and volume counters."""
        self.start_time = time.time()
        self.total_lines = 0
        self.total_commits = 0
        self.total_files = 0

    def add(self, lines: int, files: int, commits: int = 0):
        """Add new output totals to the running session counters."""
        self.total_lines += lines
        self.total_files += files
        self.total_commits += commits

    @property
    def elapsed(self) -> float:
        """Return the total number of seconds since session start."""
        return time.time() - self.start_time

    @property
    def elapsed_str(self) -> str:
        """Return elapsed time as an HH:MM:SS string."""
        e = int(self.elapsed)
        h, m, s = e // 3600, (e % 3600) // 60, e % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @property
    def lines_per_sec(self) -> float:
        """Return the current output rate in lines per second."""
        e = self.elapsed
        return self.total_lines / e if e > 0 else 0

    @property
    def commits_per_min(self) -> float:
        """Return commit throughput in commits per minute."""
        e = self.elapsed / 60
        return self.total_commits / e if e > 0 else 0

    def display(self, mode: str = "TURBO") -> str:
        """Return a compact progress string for terminal dashboards."""
        return (
            f"\r[{mode}] {self.total_lines:,} lines | "
            f"{self.total_commits:,} commits | "
            f"{self.total_files:,} files | "
            f"{self.lines_per_sec:,.0f} lines/sec | "
            f"{self.commits_per_min:.1f} commits/min | "
            f"{self.elapsed_str} elapsed"
        )

    def summary(self) -> str:
        """Return a final session summary string."""
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
