# File: prompt_validator/rules/pii.py
import re # Import the regular expressions module.
from typing import List, Dict # Import typing hints.
from .base_rule import ValidationRule # Import the base rule class.

class PIIRule(ValidationRule): # Rule to detect Personally Identifiable Information (PII).
    """Detects PII and secrets in the prompt."""
    rule_id = "PII_CHECK" # Unique identifier for the rule.
    description = "Checks for prohibited content like PII or secrets." # Rule description.

    # Regex patterns to detect common PII and secret formats.
    PII_PATTERNS = {
        "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "PHONE_NUMBER": r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        "GENERIC_SECRET": r'\b(sk|rk|ghp|xoxp|xoxb|slack|token|key|secret)_[a-zA-Z0-9]{20,}\b',
    }

    def validate(self, content: str) -> List[Dict]: # Validate the content for PII.
        issues = [] # Initialize an empty list to store found issues.
        for pii_type, pattern in self.PII_PATTERNS.items(): # Iterate over each PII pattern.
            matches = re.finditer(pattern, content) # Find all matches for the current pattern.
            for match in matches: # Iterate over each found match.
                issues.append({ # Append an issue for each PII instance found.
                    "type": self.rule_id,
                    "message": f"Potential PII detected: ({pii_type}) '{match.group(0)}'.",
                    "suggestion": "Remove or replace PII with a placeholder like [REDACTED].",
                    "details": {"pii_type": pii_type, "value": match.group(0)}
                })
        return issues # Return the list of found issues.

    def fix(self, content: str, issue: Dict) -> str: # Apply a fix for a detected PII.
        pii_value = issue.get("details", {}).get("value") # Get the PII value from the issue details.
        pii_type = issue.get("details", {}).get("pii_type") # Get the PII type.
        if pii_value: # Check if a PII value is present.
            # Replace the detected PII with a placeholder.
            return content.replace(pii_value, f"[REDACTED_{pii_type}]")
        return content # Return original content if no PII value found.