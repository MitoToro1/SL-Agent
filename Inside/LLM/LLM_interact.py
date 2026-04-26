# Funcs: (* - optional)
# user and model question-answer, question my be modified
# use RAG.py and modify question
# use DB_script.py for saving conversation context

#we will get way of having conversation with LLM
#conversation will have locally saved context
#context can be choosen via spaces


from langchain_gigachat.chat_models import GigaChat
from langchain_gigachat.embeddings import GigaChatEmbeddings

#
credentials_universal = "MDE5Yzk0ZGEtMzU0My03NWU2LThmN2QtYzg4ZWNlNjQ2M2NmOmNkMjRhZGY0LWM4MGEtNDM5ZS1iNWQyLTYxZDZjZWFmZTYyNg=="
#


giga = GigaChat(
    credentials = credentials_universal, #api key
    verify_ssl_certs=False 
)

#scope - Версия API, к которой будет выполнен запрос. По умолчанию запросы передаются в версию для физических лиц.
#model - необязательный параметр, в котором можно явно задать модель GigaChat. Вы можете посмотреть список доступных моделей с помощью метода get_models(), который выполняет запрос GET /models.
#base_url - Адрес API. По умолчанию запросы отправляются по адресу https://gigachat.devices.sberbank.ru/api/v1/, но если вы хотите использовать модели в раннем доступе, укажите адрес https://gigachat-preview.devices.sberbank.ru/api/v1

embeddings = GigaChatEmbeddings(
    credentials=credentials_universal,
    verify_ssl_certs=False
)

# result = embeddings.embed_documents(texts=['hi!']) - create embedding
#giga.invoke(request) - ask 

def GIGA_Ask(question:str, additional_data:str="Нет доп. данных", instructions:str="Ты - дружелюбный ассистент, который очень рад помогать пользователю."):
    '''
    Returns answer to the question with given instructions (optional)

    question | str(additional_data) | str(instructions)
    '''
    try:
        return giga.invoke(f"Следуй следующим инструкциям: {instructions}\n\n Используй только данные тебе данные:{additional_data}\n\n Ответь на вопрос пользователя: {question}")
    except Exception as e:
        print(f"-[!]- You've got no internet! \nError:{e}")
        return "No LLM answer, No internet :("


