# File: prompt_validator/reporter.py
import json # Import the json module for JSON output.
from typing import Dict, List # Import typing hints.
from rich.console import Console # Import Console for rich text output.
from rich.table import Table # Import Table for creating tables.

def generate_report(results: Dict[str, List[Dict]], report_format: str): # Generate a report of validation results.
    if report_format == 'json': # Check if the requested format is JSON.
        print(json.dumps(results, indent=2)) # Print the results as a formatted JSON string.
    elif report_format == 'table': # Check if the requested format is a table.
        console = Console() # Create a Rich console instance.
        if not any(results.values()): # Check if there are any issues to report.
            console.print("[green]✓ All prompts passed validation.[/green]") # Print a success message.
            return # Exit the function.

        table = Table(title="Prompt Validation Report") # Create a table with a title.
        table.add_column("File Path", style="cyan", no_wrap=True) # Add a column for the file path.
        table.add_column("Issue Type", style="magenta") # Add a column for the issue type.
        table.add_column("Message", style="red") # Add a column for the issue message.
        table.add_column("Suggestion", style="yellow") # Add a column for the suggested fix.

        for file_path, issues in results.items(): # Iterate over each file and its issues.
            if issues: # If there are issues for the file.
                for issue in issues: # Iterate over each issue.
                    table.add_row( # Add a row to the table with issue details.
                        file_path,
                        issue.get('type', 'N/A'),
                        issue.get('message', 'N/A'),
                        issue.get('suggestion', 'N/A')
                    )
        console.print(table) # Print the formatted table to the console.