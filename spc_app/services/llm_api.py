import random

def evaluate_prompt(defense_prompt, attack_prompt):
    """
    Simulate LLM evaluation:
    Returns a dictionary with a simulated response and evaluation outcome.
    """
    # For simulation, we'll randomly decide success/failure.
    success = random.choice([True, False])
    response = "access granted" if success else "access denied"
    
    # Log the prompt interaction if needed (later integrated with PromptLog model)
    return {
        "successful": success,
        "response": response
    }
