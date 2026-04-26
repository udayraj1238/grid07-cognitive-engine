"""
Grid07 Cognitive Engine — Logging Configuration
================================================
Rich console logging utilities for beautiful, color-coded output.
Used across all phases for consistent, professional console output.
"""

import sys
import io

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# Force UTF-8 output on Windows to handle Unicode characters.
# Skip this when running under pytest (pytest replaces stdout with its own capture).
if sys.platform == "win32" and "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Global console instance — force_terminal enables ANSI colors even in non-TTY
console = Console(width=100, force_terminal=True)


def print_phase_header(phase_num: int, title: str, description: str):
    """Print a prominent phase header with panel styling."""
    console.print()
    console.print(Panel(
        f"[bold white]{description}[/bold white]",
        title=f"[bold cyan]⚡ PHASE {phase_num}: {title}[/bold cyan]",
        border_style="cyan",
        box=box.DOUBLE_EDGE,
        padding=(1, 2),
    ))
    console.print()


def print_success(message: str):
    """Print a success message with green checkmark."""
    console.print(f"  [bold green]✓[/bold green] {message}")


def print_warning(message: str):
    """Print a warning message with yellow indicator."""
    console.print(f"  [bold yellow]⚠[/bold yellow] {message}")


def print_error(message: str):
    """Print an error message with red indicator."""
    console.print(f"  [bold red]✗[/bold red] {message}")


def print_info(message: str):
    """Print an info message with blue indicator."""
    console.print(f"  [bold blue]ℹ[/bold blue] {message}")


def print_subheader(text: str):
    """Print a styled subheader."""
    console.print(f"\n  [bold magenta]{'─' * 60}[/bold magenta]")
    console.print(f"  [bold magenta]▸ {text}[/bold magenta]")
    console.print(f"  [bold magenta]{'─' * 60}[/bold magenta]")


def create_similarity_table(matches: list[dict], threshold: float) -> Table:
    """
    Create a Rich table showing similarity scores for all bots.

    Args:
        matches: List of match dicts from vector_store.query_similar_bots()
        threshold: The cosine similarity threshold used for filtering

    Returns:
        Rich Table object ready for printing
    """
    table = Table(
        title=f"Cosine Similarity Scores (threshold: {threshold})",
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold white",
        header_style="bold cyan",
    )
    table.add_column("Bot", style="bold", width=20)
    table.add_column("Archetype", width=20)
    table.add_column("Similarity", justify="center", width=12)
    table.add_column("Distance", justify="center", width=12)
    table.add_column("Routed?", justify="center", width=10)

    for match in matches:
        passed = match["cosine_similarity"] >= threshold
        routed_text = "[bold green]✓ YES[/bold green]" if passed else "[dim red]✗ NO[/dim red]"
        sim_style = "bold green" if passed else "dim"

        table.add_row(
            f"{match['emoji']} {match['name']}",
            match["archetype"],
            f"[{sim_style}]{match['cosine_similarity']:.4f}[/{sim_style}]",
            f"{match['cosine_distance']:.4f}",
            routed_text,
        )

    return table
