# File: prompt_validator/validator.py
import os # Import os for path operations.
from typing import List, Dict, Tuple # Import typing hints.
from .rules import ALL_RULES # Import the list of all rule classes.

class PromptValidator: # Main class to manage and run validation.
    def __init__(self): # Initialize the validator.
        self.rules = [Rule() for Rule in ALL_RULES] # Instantiate all available validation rules.

    def validate_file(self, file_path: str) -> Tuple[str, List[Dict]]: # Validate a single prompt file.
        try: # Try to read the file content.
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except IOError as e: # Handle file reading errors.
            return file_path, [{"type": "FILE_ERROR", "message": str(e)}]

        all_issues = [] # Initialize an empty list to aggregate issues.
        for rule in self.rules: # Iterate over each instantiated rule.
            issues = rule.validate(content) # Run the rule's validation method.
            all_issues.extend(issues) # Add any found issues to the aggregate list.
        return content, all_issues # Return the content and all found issues.

    def fix_file(self, file_path: str, content: str, issues: List[Dict]) -> None: # Apply fixes to a file.
        updated_content = content # Start with the original content.
        rule_map = {rule.rule_id: rule for rule in self.rules} # Map rule IDs to rule instances.

        for issue in issues: # Iterate over each issue found.
            rule = rule_map.get(issue['type']) # Find the corresponding rule for the issue.
            if rule: # If a rule is found.
                updated_content = rule.fix(updated_content, issue) # Apply the fix.

        if updated_content != content: # Check if the content was modified.
            try: # Try to write the updated content back to the file.
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            except IOError as e: # Handle file writing errors.
                print(f"Error writing fixes to {file_path}: {e}") # Print an error message.