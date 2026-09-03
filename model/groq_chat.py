from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import config.settings as settings
import model.test as test
from retrieval.chunk_retrieval import Retrieval

class ChatBot:
    def __init__(self):
        self.API_KEY = settings.GROQ_API_KEY
        self.model = settings.chat_model
        self.temperature = settings.temperature
        self.max_retires = settings.max_retries

    def createModel(self):
        self.model = ChatGroq(
            model = self.model,
            temperature = self.temperature,
            max_retries = self.max_retires,
            api_key = self.API_KEY
        )
        return self.model

    def createPromptTemplate(self):
        self.hub_chain = test.langsimthPrompt()
        self.hub_prompt = self.hub_chain.first
        self.system_text = self.hub_prompt.messages[0].prompt.template # pulls out the raw string
        self.template = ChatPromptTemplate(
            [
                ("system", self.system_text),
                ("user", "{input}"),
                ("user", "{chunks}")
            ]
        )
        return self.template

    def createChain(self):
        self.model = self.createModel()
        self.prompt = self.createPromptTemplate()

        self.base_chain = self.prompt | self.model

        return self.base_chain

    def chat(self):
        self.chain = self.createChain()
        while True:
            try:
                self.user_input = input("You: ").strip()
            except KeyboardInterrupt:
                print("\nend")
                break

            try:
                self.obj = Retrieval()
                self.chunk = self.obj.retrieval(self.user_input)
                self.response = self.chain.invoke({"chunks": self.chunk, "input": self.user_input})
                print(self.response.content)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    test_chat = ChatBot()
    test_chat.chat()