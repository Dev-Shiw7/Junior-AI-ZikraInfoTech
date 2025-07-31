# from langchain_community.chat_models import ChatOllama
# from langchain_core.language_models.chat_models import BaseChatModel

# def get_llm() -> BaseChatModel:
#     return ChatOllama(model="mistral")


from langchain_ollama import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel

def get_llm() -> BaseChatModel:
    """
    Returns an instance of the ChatOllama LLM configured for agents.
    Using temperature=0 for more deterministic behavior for a reviewer/agent.
    """
    return ChatOllama(model="mistral", temperature=0)