from langchain.chat_models import init_chat_model

def load_model():
    
    model = init_chat_model(model="gpt-5-nano", model_provider="openai", temperature=0)

    return model