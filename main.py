"""
Grid07 Cognitive Engine — Unified Demo Runner
==============================================
One-click execution of all three phases with professional console output.

Usage:
    python main.py          # Run all phases
    python main.py --phase1 # Run only Phase 1
    python main.py --phase2 # Run only Phase 2
    python main.py --phase3 # Run only Phase 3
"""

import sys
import time

from rich.panel import Panel
from rich import box

from utils.logging_config import console, print_success, print_error, print_info
from phase1_router import run_phase1_demo
from phase2_content_engine import run_phase2_demo
from phase3_combat_engine import run_phase3_demo


def print_banner():
    """Print the Grid07 Cognitive Engine banner."""
    banner = """
 ██████╗ ██████╗ ██╗██████╗  ██████╗ ███████╗
██╔════╝ ██╔══██╗██║██╔══██╗██╔═████╗╚════██║
██║  ███╗██████╔╝██║██║  ██║██║██╔██║    ██╔╝
██║   ██║██╔══██╗██║██║  ██║████╔╝██║   ██╔╝ 
╚██████╔╝██║  ██║██║██████╔╝╚█████╔╝   ██║  
 ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝  ╚════╝    ╚═╝  
    C O G N I T I V E   E N G I N E
"""
    console.print(Panel(
        f"[bold cyan]{banner}[/bold cyan]\n"
        f"  [dim]Vector Routing • LangGraph Orchestration • RAG Combat Engine[/dim]\n"
        f"  [dim]Built with LangChain, ChromaDB, and Groq (Llama 3.3 70B)[/dim]",
        border_style="cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 2),
    ))


def main():
    """Main entry point — runs selected or all phases."""
    print_banner()

    # Parse simple CLI flags
    args = set(sys.argv[1:])
    run_all = not args or args == {"--all"}
    run_p1 = run_all or "--phase1" in args
    run_p2 = run_all or "--phase2" in args
    run_p3 = run_all or "--phase3" in args

    results = {}
    start_time = time.time()

    # ─── Phase 1: Vector-Based Persona Matching ─────────────
    if run_p1:
        try:
            results["Phase 1"] = run_phase1_demo()
        except Exception as e:
            print_error(f"Phase 1 failed: {e}")
            console.print_exception()
            results["Phase 1"] = False

    # ─── Phase 2: Autonomous Content Engine ─────────────────
    if run_p2:
        try:
            results["Phase 2"] = run_phase2_demo()
        except Exception as e:
            print_error(f"Phase 2 failed: {e}")
            console.print_exception()
            results["Phase 2"] = False

    # ─── Phase 3: Combat Engine ─────────────────────────────
    if run_p3:
        try:
            results["Phase 3"] = run_phase3_demo()
        except Exception as e:
            print_error(f"Phase 3 failed: {e}")
            console.print_exception()
            results["Phase 3"] = False

    # ─── Summary ────────────────────────────────────────────
    elapsed = time.time() - start_time
    console.print()
    console.print(Panel(
        "\n".join(
            f"  {'[bold green]✓[/bold green]' if v else '[bold red]✗[/bold red]'} {k}: "
            f"{'PASSED' if v else 'FAILED'}"
            for k, v in results.items()
        ) + f"\n\n  [dim]Total execution time: {elapsed:.1f}s[/dim]",
        title="[bold white]═══ EXECUTION SUMMARY ═══[/bold white]",
        border_style="white",
        box=box.DOUBLE_EDGE,
        padding=(1, 2),
    ))
    console.print()


if __name__ == "__main__":
    main()
