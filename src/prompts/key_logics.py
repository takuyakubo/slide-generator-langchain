def model_key_logic(key):
    if key.startswith("claude-"):
        return "claude"
    elif key.startswith("models/gemini-"):
        return "gemini"
    return key
