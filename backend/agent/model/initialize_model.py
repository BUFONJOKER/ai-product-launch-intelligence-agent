from langchain_openai import ChatOpenAI


def load_model():
    """Instantiate and return the language model used by the agents.

    The function centralizes creation of the ChatOpenAI model instance
    configured for this project. It accepts no parameters and returns
    a configured model object ready for synchronous or asynchronous
    invocation by higher-level workflow code.

    Returns:
        ChatOpenAI: A configured language model instance (currently
            using the "gpt-5-nano" model with temperature set to 0).
    """

    model = ChatOpenAI(model="gpt-5-nano", temperature=0, streaming=True)

    return model
