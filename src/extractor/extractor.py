from typing import List
from langchain.prompts import ChatPromptTemplate
from extractor.get_model import get_model_llm


PROMPT_TEMPLATE = """
Por favor escribe un resumen del texto que se porporciona más adelante, además extrae 3 entidades del mismo. 
El formato de la respuesta sea: 
-INICIO RESUMEN- Acá va el texto del resumen -FIN RESUMEN- | ["listado","de","entidades","separadas","por","comas","y","con","comillas"] 
El texto es: {text}.
Pro favor verifica que tu respuesta esté acoerde con la estructura.
Respuesta:
"""

def analizar_texto(texto: str):
    model = get_model_llm()
    prompt_template = ChatPromptTemplate.from_messages(
    [("system", PROMPT_TEMPLATE), ("user", "{text}")]
)
    prompt = prompt_template.invoke({"text": texto})

    # Invoke chain
    response = model.invoke(prompt)
    return response