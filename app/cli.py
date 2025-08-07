import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sys
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.search_api import search
from app.cli_helpers import transform_query, display_results

from rich.console import Console
from rich.prompt import Prompt

console = Console()

def generate_summary_ollama(text: str, model="openchat"):
    prompt = f"Summarize the following in one sentence:\n\n{text.strip()}\n\nSummary:"
    
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[summary error: {e}]"

def main():
    console.print("[bold magenta]🔍 TrustAI: Terminal Research Recommender[/bold magenta]")

    while True:
        query = Prompt.ask("\n[bold yellow]Enter a research topic (or 'q' to quit)[/bold yellow]")
        if query.lower() in ['q', 'quit', 'exit']:
            console.print("\n[bold red]Goodbye![/bold red]")
            break

        transformed_query = transform_query(query)
        console.print(f"\n[cyan]Transformed Query:[/cyan] {transformed_query}")
        console.print("[green]Searching...[/green]\n")

        result = search(transformed_query)

        if result["results"]:
            display_results(result["results"], summarizer=generate_summary_ollama)
        else:
            console.print("[red]No results found.[/red]")

if __name__ == "__main__":
    main()