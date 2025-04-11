def validate_question(input_text):
    """
    Validates if a question is ethically appropriate.
    Returns (is_valid, reason) tuple.
    """
    lower_text = input_text.lower()
    
    red_flags = {
        "racial_slurs": ["n-word", "racial slur", "racist"],
        "personal_attacks": ["you liar", "you fraud", "you're lying"],
        "inappropriate_content": ["sex", "sexual", "intimate"]
    }
    
    for category, phrases in red_flags.items():
        if any(phrase in lower_text for phrase in phrases):
            return False, f"Objection! Questioning contains {category.replace('_', ' ')}."
    
    return True, ""
