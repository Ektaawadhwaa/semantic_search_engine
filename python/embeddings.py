
import random
def get_embedding(text):
    print(f"[DEV] Fake embedding for: {text}")
    return [random.uniform(-1, 1) for _ in range(384)]
 
    # local dev — return fake embedding for testing
    
 