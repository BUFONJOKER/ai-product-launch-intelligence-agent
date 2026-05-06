from langchain_openai import ChatOpenAI


def load_model():
    '''
    Loading gpt 5 nano model from openai
    '''


    model = ChatOpenAI(
        model="gpt-5-nano", temperature=0
    )

    return model
