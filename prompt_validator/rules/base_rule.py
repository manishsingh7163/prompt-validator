# File: prompt_validator/rules/base_rule.py
from abc import ABC, abstractmethod # Import Abstract Base Class components.
from typing import List, Dict, Optional # Import typing hints.

class ValidationRule(ABC): # Define the abstract base class for all validation rules.
    """Abstract base class for a validation rule."""

    @property
    @abstractmethod
    def rule_id(self) -> str: # Unique identifier for the rule.
        pass

    @property
    @abstractmethod
    def description(self) -> str: # Human-readable description of the rule.
        pass

    @abstractmethod
    def validate(self, content: str) -> List[Dict]: # Abstract method to perform validation.
        pass

    @abstractmethod
    def fix(self, content: str, issue: Dict) -> str: # Abstract method to apply a fix.
        pass