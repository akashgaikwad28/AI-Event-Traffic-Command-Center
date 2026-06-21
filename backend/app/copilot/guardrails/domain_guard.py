import re

class GuardrailViolationError(Exception):
    """Exception raised for violations of domain or safety guardrails."""
    pass

class DomainGuard:
    """
    Implements strict Domain Restriction Guardrails and Prompt Injection Defenses
    for the Operational Copilot.
    """
    def __init__(self):
        # Patterns for detecting prompt injection attempts
        self.injection_patterns = [
            r"(?i)\bignore\s+(all\s+)?(previous\s+)?instructions\b",
            r"(?i)\bforget\s+(all\s+)?(previous\s+)?instructions\b",
            r"(?i)\byou\s+are\s+now\b",
            r"(?i)\bact\s+as\b",
            r"(?i)\bsystem\s+prompt\b",
            r"(?i)\bbypass\b",
        ]
        
        # Patterns for restricted topics (politics, coding, unrelated)
        self.restricted_topics = [
            # Politics
            r"(?i)\b(election|democrat|republican|president|congress|politics|political|vote|voting)\b",
            # Coding
            r"(?i)\b(write\s+code|python|javascript|java|c\+\+|html|css|sql|function|def\s+|class\s+|import\s+)\b",
            # General unrelated
            r"(?i)\b(recipe|sports|movie|weather|celebrity|joke)\b"
        ]
        
        # Patterns that indicate the query is within the valid operational domain
        self.allowed_domains = [
            r"(?i)\b(traffic|event|events|command\s+center|operational|copilot|grid|dispatch|route|map|schedule|incident|accident|road|closure)\b"
        ]

    def check_query(self, query: str) -> bool:
        """
        Validates the query against prompt injection and domain restrictions.
        
        Args:
            query (str): The user input to check.
            
        Returns:
            bool: True if the query is valid and authorized.
            
        Raises:
            GuardrailViolationError: If the query violates any guardrail.
        """
        if not query or not query.strip():
            raise GuardrailViolationError("Query cannot be empty.")

        # 1. Check for prompt injection
        for pattern in self.injection_patterns:
            if re.search(pattern, query):
                raise GuardrailViolationError("Prompt injection detected.")
                
        # 2. Check for restricted topics
        for pattern in self.restricted_topics:
            if re.search(pattern, query):
                raise GuardrailViolationError("Query contains restricted topics (politics, coding, etc.).")
                
        # 3. Check for domain relevance
        is_relevant = False
        for pattern in self.allowed_domains:
            if re.search(pattern, query):
                is_relevant = True
                break
                
        if not is_relevant:
            raise GuardrailViolationError("Query is not related to the operational domain.")
            
        return True
