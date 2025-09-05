from typing import List
from langchain.prompts import ChatPromptTemplate
from extractor.get_model import get_model_llm
from langchain_core.runnables import RunnableLambda

PROMPT_TEMPLATE = """
Por favor escribe un resumen del texto que se porporciona más adelante, además extrae hasta tres (3) entidades principales del mismo. 
La respuesta está dividida en dos partesm en la primera, envía el resumen del texto y en la segunda (separado por una barra | ) envía el listado de las entidades, por ejemplo: 
 'Acá va el texto del resumen | ["listado","entidades","principales"] '
El texto es: {text}.
Por favor verifica que tu respuesta esté acorde con la estructura, ten muy presente la barra | que separa el resumen de las entidades,
si no logras extraer entidades, entonces responde un arreglo vacío así [] en el lado de las entidades.
Respuesta:
"""

def analizar_texto(texto: str):
    model = get_model_llm() #obtención del modelo
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", PROMPT_TEMPLATE), ("user", "{text}")]
    ) # Plantilla del prompt
    prompt = prompt_template.invoke({"text": texto}) # Prompt con formato

    # Invoke chain
    response = model.invoke(prompt) #invocación del modelo
    return response