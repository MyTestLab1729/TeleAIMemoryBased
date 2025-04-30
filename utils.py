# --- utils.py ---

# Dummy token counter for now

def count_tokens(messages):
    return sum(len(m["content"].split()) for m in messages) * 1.3  # crude estimate

def trim_history(history, max_tokens):
    while count_tokens(history) > max_tokens and len(history) > 2:
        history.pop(0)  # remove oldest
    return history