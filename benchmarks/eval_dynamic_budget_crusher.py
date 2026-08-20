"""
Benchmark Evaluation Script for DynamicBudgetCrusher.
Measures token savings, execution time, and system prompt / latest message preservation.
"""

import time
from headroom.transforms.dynamic_budget_crusher import DynamicBudgetCrusher


def run_benchmark():
    # Setup test conversations with varying turn counts and token loads
    sample_system_prompt = "You are an expert AI software engineer providing precise code solutions."
    
    # Generate mock conversation history of 20 turns (~6000 estimated tokens)
    large_conversation = [{"role": "system", "content": sample_system_prompt}]
    for i in range(10):
        large_conversation.append({
            "role": "user", 
            "content": f"Turn {i+1}: Here is a lengthy context block explaining architectural requirements, " + ("data " * 150)
        })
        large_conversation.append({
            "role": "assistant", 
            "content": f"Turn {i+1} Response: Here is the suggested code implementation details, " + ("code " * 150)
        })
    large_conversation.append({"role": "user", "content": "What is the final summary of changes needed?"})

    crusher = DynamicBudgetCrusher(max_budget_tokens=2000, target_reduction_ratio=0.4)

    # Calculate pre-compression token count
    input_tokens = sum(crusher.estimate_tokens(m["content"]) for m in large_conversation)

    start_time = time.perf_counter()
    compressed_messages = crusher.compress(large_conversation)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    # Calculate post-compression token count
    output_tokens = sum(crusher.estimate_tokens(m["content"]) for m in compressed_messages)
    reduction_pct = ((input_tokens - output_tokens) / input_tokens) * 100

    # Verification checks
    system_preserved = compressed_messages[0]["content"] == sample_system_prompt
    latest_preserved = compressed_messages[-1]["content"] == "What is the final summary of changes needed?"

    print("\n" + "=" * 50)
    print("      DYNAMIC BUDGET CRUSHER BENCHMARK RESULTS     ")
    print("=" * 50)
    print(f"Total Input Messages   : {len(large_conversation)}")
    print(f"Pre-Compression Tokens : {input_tokens}")
    print(f"Post-Compression Tokens: {output_tokens}")
    print(f"Tokens Saved           : {input_tokens - output_tokens} ({reduction_pct:.2f}%)")
    print(f"Latency Overhead       : {elapsed_ms:.3f} ms")
    print(f"System Prompt Intact   : {system_preserved}")
    print(f"Latest Query Intact    : {latest_preserved}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_benchmark()