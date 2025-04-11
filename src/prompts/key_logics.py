def model_key_logic(key):
    if key.startswith("claude-"):
        return "claude"
    elif key.startswith("models/gemini-"):
        return "gemini"
    elif key.startswith("gpt-"):
        return "gpt"
    return key
