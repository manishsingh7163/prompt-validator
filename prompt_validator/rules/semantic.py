# File: prompt_validator/rules/semantic.py
from typing import List, Dict # Import typing hints.
from .base_rule import ValidationRule # Import the base rule class.
from ..llm_client import LLMClient # Import the LLM client.

class SemanticRule(ValidationRule): # Base class for rules requiring LLM-based semantic analysis.
    def __init__(self): # Initialize the semantic rule.
        self.llm_client = LLMClient() # Create an instance of the LLM client.

class RedundancyRule(SemanticRule): # Rule to detect redundant instructions.
    """Detects redundant instructions using an LLM."""
    rule_id = "SEMANTIC_REDUNDANCY" # Unique identifier for the rule.
    description = "Detects redundant instructions that add no new value." # Rule description.

    SYSTEM_PROMPT = ( # System prompt for the LLM.
        "You are a helpful assistant. Analyze the following text for redundant sentences or phrases. "
        "A redundant phrase repeats an instruction or idea without adding new information. "
        "List each distinct redundant sentence or phrase you find, one per line. "
        "If there are no redundancies, respond with 'None'."
    )

    def validate(self, content: str) -> List[Dict]: # Validate content for redundancy.
        issues = [] # Initialize list for issues.
        response = self.llm_client.query(self.SYSTEM_PROMPT, content) # Query LLM.
        if response.lower().strip() != 'none' and "error" not in response.lower(): # Check LLM response.
            redundant_phrases = [line.strip() for line in response.split('\n') if line.strip()] # Parse response.
            for phrase in redundant_phrases: # Iterate through found redundant phrases.
                issues.append({ # Append an issue for each phrase.
                    "type": self.rule_id,
                    "message": f"Redundant instruction found: '{phrase}'.",
                    "suggestion": "Remove the redundant phrase to make the prompt clearer.",
                    "details": {"redundant_phrase": phrase}
                })
        return issues # Return issues.

    def fix(self, content: str, issue: Dict) -> str: # Fix by removing the redundant phrase.
        phrase_to_remove = issue.get("details", {}).get("redundant_phrase") # Get phrase to remove.
        if phrase_to_remove: # If phrase exists.
            return content.replace(phrase_to_remove, "", 1) # Remove first occurrence of the phrase.
        return content # Return original content.

class ContradictionRule(SemanticRule): # Rule to detect conflicting instructions.
    """Detects conflicting instructions using an LLM."""
    rule_id = "SEMANTIC_CONFLICT" # Unique identifier for the rule.
    description = "Detects contradictory requirements in the prompt." # Rule description.

    # --- UPDATED SYSTEM PROMPT ---
    SYSTEM_PROMPT = (
        "You are an expert at analyzing instructions. Find contradictory instructions. "
        "A contradiction means two instructions are *impossible* to follow simultaneously (e.g., 'text must be 100 words' and 'text must be 5000 words'; 'be concise' and 'be extremely verbose'). "
        "IMPORTANT: Simple repetition or emphasis (like 'be detailed' and 'be very detailed') is NOT a conflict. "
        "For each conflict you find, return ONLY the two conflicting phrases on separate lines, prefixed with 'PHRASE: '. "
        "If there are no conflicts, respond with 'None'."
    )

    def validate(self, content: str) -> List[Dict]: # Validate content for contradictions.
        issues = [] # Initialize list for issues.
        response = self.llm_client.query(self.SYSTEM_PROMPT, content) # Query LLM.
        if response.lower().strip() != 'none' and "error" not in response.lower(): # Check LLM response.
            phrases = [line.replace("PHRASE: ", "").strip() for line in response.split('\n') if line.startswith("PHRASE: ")] # Parse response.
            if len(phrases) >= 2: # A conflict requires at least two phrases.
                # Take the first pair of conflicting phrases found
                conflict_pair = phrases[0:2]
                issues.append({ # Append the conflict issue.
                    "type": self.rule_id,
                    "message": f"Conflicting instructions found: '{conflict_pair[0]}' and '{conflict_pair[1]}'.",
                    "suggestion": "Resolve the contradiction between the instructions.",
                    "details": {"conflicting_phrases": conflict_pair}
                })
        return issues # Return issues.

    def fix(self, content: str, issue: Dict) -> str: # Cannot auto-fix conflicts, suggest manual review.
        # Auto-fixing contradictions is complex and risky; we'll add a comment instead.
        phrases = issue.get("details", {}).get("conflicting_phrases", []) # Get conflicting phrases.
        if phrases: # If phrases exist.
            comment = f"\n\n# TODO: Resolve conflict identified by validator between: '{phrases[0]}' AND '{phrases[1]}'\n" # Create a comment.
            return content.strip() + comment # Append comment to the content.
        return content # Return original content.