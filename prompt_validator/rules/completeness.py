# File: prompt_validator/rules/completeness.py
import re # Import the regular expressions module.
from typing import List, Dict # Import typing hints.
from .base_rule import ValidationRule # Import the base rule class.

class CompletenessRule(ValidationRule): # Rule to check for required sections in a prompt.
    """Checks if the prompt contains all required sections."""
    rule_id = "COMPLETENESS_CHECK" # Unique identifier for the rule.
    description = "Checks for missing required sections (Task, Success Criteria, Examples)." # Rule description.

    REQUIRED_SECTIONS = ["Task", "Success Criteria", "Examples"] # List of mandatory section titles.

    def validate(self, content: str) -> List[Dict]: # Validate the prompt's content.
        issues = [] # Initialize an empty list to store found issues.
        for section in self.REQUIRED_SECTIONS: # Iterate over each required section.
            # Updated regex: looks for the section as a whole word, followed by optional colon or end of line.
            pattern = fr"^\s*#+\s*{re.escape(section)}(\s*:|\s*$)"
            if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                issues.append({ # Append an issue if a section is missing.
                    "type": self.rule_id,
                    "message": f"Missing required section: '{section}'.",
                    "suggestion": f"Add a '## {section}' section to the prompt.",
                    "details": {"missing_section": section}
                })
        return issues # Return the list of found issues.

    def fix(self, content: str, issue: Dict) -> str: # Apply a fix for a missing section.
        missing_section = issue.get("details", {}).get("missing_section") # Get the missing section name.
        if missing_section: # Check if the missing section name is available.
            # Append a template for the missing section to the content.
            return content.strip() + f"\n\n## {missing_section}:\n- [Add details here]\n"
        return content # Return original content if no section name found.