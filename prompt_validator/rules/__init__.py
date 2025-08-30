# File: prompt_validator/rules/__init__.py
from .completeness import CompletenessRule # Import CompletenessRule.
from .pii import PIIRule # Import PIIRule.
from .semantic import RedundancyRule, ContradictionRule # Import semantic rules.

# List of all available rule classes for easy import and instantiation.
ALL_RULES = [
    CompletenessRule,
    PIIRule,
    RedundancyRule,
    ContradictionRule,
]