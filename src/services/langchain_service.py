import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from src.core import settings

os.environ["LANGSMITH_TRACING"] = settings.LANGSMITH_TRACING
os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

class LangChainService:
    def __init__(self):
        self.model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

    def translate_from_portuguese_to_english(self, text: str) -> str:
        messages: list[BaseMessage] = [
            SystemMessage("Translate the following from Portuguese into English"),
            HumanMessage(text),
        ]

        result: BaseMessage = self.model.invoke(input=messages)
        return str(result.content)
    
    def translate(
            self, 
            text: str, 
            from_language: str = "Portuguese",
            to_language: str = "English"
        ) -> str:
        """
        Translate text from one language to another using a chat model.

        Args:
            text (str): The text to translate.
            from_language (str): The language to translate from.
            to_language (str): The language to translate to.

        Returns:
            str: The translated text.
        """

        system_template = """
            Translate the following from {from_language} into {to_language}
        """

        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )

        prompt = prompt_template.invoke(
            {
                "from_language": from_language, 
                "to_language": to_language,
                "text": text
            }
        )

        return str(self.model.invoke(prompt).content)
