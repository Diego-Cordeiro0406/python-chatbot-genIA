import google.generativeai as genai
import os
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

initial_prompt = (
    "Você é uma ia generativa capaz de analisar textos e identificar"
    " o sentimento expressado no texto "
    "(positivo, negativo, neutro) e fornecer feedback ao usuário."
)

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=initial_prompt)
chat = model.start_chat()

# bot com suporte a varios tipo de aquivos
# def gradio_wrapper(message, _history):
# Extraia o texto da mensagem
# prompt = [message["text"]]
# uploaded_files = []
# Iterar sobre cada arquivo recebido
# if message["files"]:
# for file_gradio_data in message["files"]:
# Obter o caminho local do arquivo
# file_path = file_gradio_data["path"]
# Fazer upload do arquivo para o Gemini
# uploaded_file_info = genai.upload_file(path=file_path)
# Adicionar o arquivo uploadado à lista
#         uploaded_files.append(uploaded_file_info)
# prompt.extend(uploaded_files)
# Envie o prompt para o chat e obtenha a resposta
# response = chat.send_message(prompt)
# return response.text


# bot analizador de sentimentos
def gradio_wrapper(message, _history):
    # Extraia o texto da mensagem
    user_text = message["text"]
    # Extraia a lista de arquivos
    files = message.get("files", [])
    # Lista para armazenar conteúdos dos arquivos
    file_contents = []
    # Verifique se há arquivos anexados
    if files:
        for file_info in files:
            # Obter o caminho local do arquivo
            file_path = file_info["path"]
            # Ler o conteúdo do arquivo se for um texto
            if file_info["mime_type"] == "text/plain":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                file_contents.append(content)
            else:
                # Ignorar arquivos que não sejam de texto simples
                pass
    # Combinar o texto do usuário com o conteúdo dos arquivos
    combined_text = user_text + "\n\n" + "\n\n".join(file_contents)
    # Criar o prompt para análise de sentimento
    prompt = f"Analise o sentimento do seguinte texto:\n{combined_text}"
    # Envie o prompt para o chat e obtenha a resposta
    response = chat.send_message(prompt)
    return response.text


chat_interface = gr.ChatInterface(fn=gradio_wrapper, multimodal=True)
chat_interface.launch()
