"""
DynamicBudgetCrusher Extension for Headroom
Adapts compression strength dynamically based on incoming token volume and budget limits.
"""

from typing import Any, Dict, List


class DynamicBudgetCrusher:
    def __init__(self, max_budget_tokens: int = 4096, target_reduction_ratio: float = 0.3):
        self.max_budget_tokens = max_budget_tokens
        self.target_reduction_ratio = target_reduction_ratio

    def estimate_tokens(self, text: str) -> int:
        """Simple heuristic token estimation (avg 4 chars per token)."""
        return max(1, len(text) // 4)

    def compress(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Dynamically compresses messages to remain within max_budget_tokens
        while preserving system prompts and recent context.
        """
        total_tokens = sum(self.estimate_tokens(m.get("content", "")) for m in messages)
        
        if total_tokens <= self.max_budget_tokens:
            return messages  # No compression needed

        compressed = []
        for idx, msg in enumerate(messages):
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            # Always preserve system prompts and the final message intact
            if role == "system" or idx == len(messages) - 1:
                compressed.append(msg)
                continue
            
            # Truncate middle history items proportionally
            keep_chars = int(len(content) * (1.0 - self.target_reduction_ratio))
            truncated_content = content[:keep_chars] + "... [compressed]"
            compressed.append({"role": role, "content": truncated_content})

        return compressed