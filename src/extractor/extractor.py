import json
import os
from pathlib import Path
from pydantic import BaseModel
import sqlite3
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
    resultado: str
    entidades: List[str]

class RegistroTexto(BaseModel):
    """
    Modelo para la entrada de texto que se desea analizar.
    
    Este modelo se utiliza para recibir el texto que el usuario desea
    registrar en el sistema para posterior análisis.
    """
    texto: str

class RespuestaRegistro(BaseModel):
    """
    Modelo que se responde al realizar el registro de un nuevo texto.
    
    Contiene el identificador creado para el texto enviado.
    """
    id: int

textos = []

# Crea un objeto para el nuevo texto a analizar, le pone un id y lo guarda en memoria en el arreglo textos
# parámetros:
#         - objeto de tipo RegistroTexto, el cual contiene un solo campo llamado texto con el string a registrar.
# respuesta: 
#         - objeto de tipo RespuestaRegistro, el cual contieneun solo campo llamado id con el identificador del texto cargado.
def registrar_texto(objeto_texto: RegistroTexto) -> RespuestaRegistro:
    try:
        global textos
        id=len(textos)+1
        texto = ObjetoTextoAnalizar(texto=objeto_texto.texto,id=id,resultado="...",entidades=[])
        textos.append(texto)
        return RespuestaRegistro(id=texto.id)
    except ValueError as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

# Lista los elementos del arreglo de textos
# parámetros:
#         - NINGUNO.
# respuesta: 
#         - Listado de objetos del tipo ObjetoTextoAnalizar, que contiene toda la información de un registro.
def listar_textos() -> List[ObjetoTextoAnalizar]:
    try:
        global textos
        return textos
    except ValueError as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
