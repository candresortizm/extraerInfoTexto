from pydantic import BaseModel
from typing import List

class ObjetoTextoAnalizar(BaseModel):
    """
    Modelo que representa un texto registrado.
    
    Este modelo contiene toda la información relacionada con un texto que ha sido
    registrado en el sistema, incluyendo el texto original, su identificador único,
    el resultado del análisis (si tiene) y las entidades extraídas (si tiene).
    """
    texto: str
    id: int
    resumen: str
    entidades: List[str]

class RespuestaRegistro(BaseModel):
    """
    Modelo que se responde al realizar el registro de un nuevo texto.
    
    Contiene el identificador creado para el texto enviado.
    """
    id: int

class RespuestaAnalisis(BaseModel):
    """
    Modelo que se responde al realizar el registro de un nuevo texto.
    
    Contiene el identificador creado para el texto enviado.
    """
    resumen: str
    entidades: List[str]
