import json
import os

# BUG FIX: Old path was a hardcoded Windows absolute path.
# Now uses a relative path — works on any machine.
MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "memory.json"
)


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
