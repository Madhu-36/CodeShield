import os
import json
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI

class RiskTier(Enum):
    TIER_1 = 1  # Safe / Read-Only
    TIER_2 = 2  # Non-Destructive Write
    TIER_3 = 3  # Potentially Destructive

class IntentAction(BaseModel):
    action: str
    target: str
    tier: RiskTier
    reasoning: str

class PolicyGate:
    """
    Evaluates Natural Language intents and proposed actions,
    assigning a Risk Tier to govern execution using an LLM.
    """
    
    DESTRUCTIVE_KEYWORDS = ["rm", "delete", "drop", "push", "force", "kill"]
    WRITE_KEYWORDS = ["patch", "write", "generate", "pytest", "touch", "mkdir"]
    
    @classmethod
    def classify_action(cls, proposed_command: str) -> IntentAction:
        """
        Classifies an action using an LLM if configured, otherwise falls back to heuristics.
        """
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL")
        
        if api_key:
            return cls._llm_classify(proposed_command, api_key, base_url)
        else:
            return cls._heuristic_classify(proposed_command)
            
    @classmethod
    def _llm_classify(cls, command: str, api_key: str, base_url: Optional[str]) -> IntentAction:
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        system_prompt = """
        You are a Security Policy Gate for a developer assistant.
        Classify the following proposed shell command into a Risk Tier.
        
        Tiers:
        1: Safe / Read-Only (e.g., ls, cat, AST inspection, echo)
        2: Non-Destructive Write (e.g., local test generation, creating a file, running a linter)
        3: Potentially Destructive (e.g., git push, rm, DB drop, modifying sensitive files)
        
        Respond ONLY with a valid JSON object matching this schema:
        {
          "action": "the command",
          "target": "target file or system",
          "tier": <integer 1, 2, or 3>,
          "reasoning": "short explanation of the risk"
        }
        """
        
        try:
            response = client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            data = json.loads(response.choices[0].message.content)
            tier_val = data.get("tier", 3)
            # Map integer back to RiskTier enum
            tier_enum = RiskTier(tier_val)
            
            return IntentAction(
                action=data.get("action", command),
                target=data.get("target", "system"),
                tier=tier_enum,
                reasoning=data.get("reasoning", "LLM classified action.")
            )
        except Exception as e:
            # Fallback on failure
            return cls._heuristic_classify(command, f"LLM error: {str(e)}. Fallback reasoning: ")
            
    @classmethod
    def _heuristic_classify(cls, proposed_command: str, prefix: str = "") -> IntentAction:
        import re
        command_lower = proposed_command.lower()
        
        for keyword in cls.DESTRUCTIVE_KEYWORDS:
            # Use word boundaries to avoid matching "rm" inside "Normal"
            if re.search(rf'\b{keyword}\b', command_lower):
                return IntentAction(
                    action=proposed_command,
                    target="system",
                    tier=RiskTier.TIER_3,
                    reasoning=f"{prefix}Contains potentially destructive keyword: '{keyword}'"
                )
                
        for keyword in cls.WRITE_KEYWORDS:
            if re.search(rf'\b{keyword}\b', command_lower):
                return IntentAction(
                    action=proposed_command,
                    target="system",
                    tier=RiskTier.TIER_2,
                    reasoning=f"{prefix}Contains state-modifying keyword: '{keyword}'"
                )
                
        return IntentAction(
            action=proposed_command,
            target="system",
            tier=RiskTier.TIER_1,
            reasoning=f"{prefix}Action appears to be safe and read-only."
        )
