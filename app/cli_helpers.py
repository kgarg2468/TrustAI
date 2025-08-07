# app/cli_helpers.py

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def transform_query(query: str) -> str:
    return query.strip().lower()

def display_results(results: list, summarizer=None):
    table = Table(title="📚 Top Research Article Matches", box=box.SIMPLE_HEAVY)
    table.add_column("🔖 Title", style="bold cyan", no_wrap=True)
    table.add_column("📊 Score", justify="right", style="green")
    table.add_column("✨ Highlights", style="dim")
    if summarizer:
        table.add_column("📝 Summary", style="white")

    for item in results[:8]:
        highlights = "• " + "\n• ".join(item['highlights'])
        summary = summarizer(item['title']) if summarizer else ""
        table.add_row(item['title'], f"{item['similarity']:.3f}", highlights, summary)

    console.print(table)
    console.rule("[bold]End of Results")