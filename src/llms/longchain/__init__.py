import os

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory

from .._session_store.memory import DEFAULT_SESSION_STORE


class LangchainOllamaGenerator:
    SESSION_STORE = DEFAULT_SESSION_STORE()

    def __init__(self, model_name: str, context: str, base_url: str = "http://localhost:11434"):
        # Load prompt template
        prompt_template_path = os.path.join(os.path.dirname(__file__), "prompt_format.md")
        self.PROMPT_TEMPLATE = open(prompt_template_path, "r", encoding="utf-8").read()

        self.model_name = model_name
        self.context = context
        self.llm = ChatOllama(model=model_name, base_url=base_url)

    def _build_chain(self, memory: ConversationBufferMemory) -> ConversationChain:
        return ConversationChain(
            llm=self.llm,
            memory=memory,
            verbose=False,
        )

    def _get_or_create_memory(self, user_id: str) -> ConversationBufferMemory:
        memory = self.SESSION_STORE.get(user_id)
        if not memory:
            memory = ConversationBufferMemory()
            # Set initial system prompt
            system_prompt = self.PROMPT_TEMPLATE.format(context=self.context, query="")
            memory.chat_memory.add_ai_message(system_prompt)
            self.SESSION_STORE.set(user_id, memory)
        return memory

    def get_response(self, user_id: str, user_input: str) -> str:
        memory = self._get_or_create_memory(user_id)
        chain = self._build_chain(memory)
        return chain.predict(input=user_input)
