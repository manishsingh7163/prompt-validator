# File: prompt_validator/cli.py
import os # Import os for operating system functionalities.
import click # Import click for creating the command-line interface.
from .validator import PromptValidator # Import the main validator class.
from .reporter import generate_report # Import the report generation function.

@click.command() # Decorator to create a CLI command.
@click.argument('directory', type=click.Path(exists=True, file_okay=False)) # Argument for the directory path.
@click.option('--fix', is_flag=True, help='Automatically apply suggested fixes.') # Option to enable auto-fixing.
@click.option('--report-format', type=click.Choice(['table', 'json']), default='table', help='Output format.') # Option for report format.
def main(directory, fix, report_format): # The main function for the CLI.
    """Validates all .txt prompt files in a given directory."""
    validator = PromptValidator() # Instantiate the validator.
    results = {} # Dictionary to store results per file.
    file_contents = {} # Dictionary to store original file contents.

    click.echo(f"Scanning directory: {directory}") # Inform the user about the scan.
    for filename in os.listdir(directory): # Iterate through files in the directory.
        if filename.endswith(".txt"): # Process only .txt files.
            file_path = os.path.join(directory, filename) # Get the full file path.
            content, issues = validator.validate_file(file_path) # Validate the file.
            if issues: # If issues are found.
                results[file_path] = issues # Store the issues.
                file_contents[file_path] = content # Store the content for potential fixing.

    generate_report(results, report_format) # Generate and display the report.

    if fix and results: # If the --fix flag is set and there are issues.
        if click.confirm('Do you want to apply the suggested fixes?'): # Ask for user confirmation.
            for file_path, issues in results.items(): # Iterate through files with issues.
                validator.fix_file(file_path, file_contents[file_path], issues) # Apply fixes.
                click.echo(f"Applied fixes to {file_path}") # Confirm fixing action.
            click.echo("Fixing process complete.") # Announce completion.
        else:
            click.echo("Fixing process cancelled.") # Announce cancellation.

if __name__ == '__main__': # Standard entry point check.
    main() # Run the main CLI function.