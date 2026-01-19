from typing import Any
from langchain_ollama import ChatOllama

def get_llm(model: str = "llama3.1:8b", temperature: float = 0.1, **kwargs: Any) -> ChatOllama:
    """
    Get Ollama LLM instance
    
    Args:
        model: Ollama model name (llama3.1:8b, qwen2.5-coder:3b, etc.)
        temperature: Response randomness (0-1)
        **kwargs: Additional ChatOllama arguments
    
    Returns:
        ChatOllama instance
    """
    return ChatOllama(
        model=model,
        temperature=temperature,
        **kwargs
    )
