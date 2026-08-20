import pytest
from headroom.transforms.dynamic_budget_crusher import DynamicBudgetCrusher


def test_dynamic_budget_crusher_no_compression_under_budget():
    crusher = DynamicBudgetCrusher(max_budget_tokens=100)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello world!"},
    ]
    compressed = crusher.compress(messages)
    assert compressed == messages


def test_dynamic_budget_crusher_compresses_over_budget():
    crusher = DynamicBudgetCrusher(max_budget_tokens=10, target_reduction_ratio=0.5)
    long_text = "This is a very long string that will exceed the budget limit."
    messages = [
        {"role": "system", "content": "System prompt preserved."},
        {"role": "user", "content": long_text},
        {"role": "user", "content": "Latest user query."},
    ]
    compressed = crusher.compress(messages)
    
    # System prompt remains unchanged
    assert compressed[0]["content"] == "System prompt preserved."
    # Middle message is compressed
    assert "[compressed]" in compressed[1]["content"]
    # Final message is preserved intact
    assert compressed[2]["content"] == "Latest user query."