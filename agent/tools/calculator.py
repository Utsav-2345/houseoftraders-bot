
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b