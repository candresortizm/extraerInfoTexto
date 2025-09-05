import json
import os
from pathlib import Path
from extractor.models import RespuestaRegistro, ObjetoTextoAnalizar, RespuestaAnalisis
import sqlite3
from typing import List
from extractor.extractor import analizar_texto

textos = []

# Crea un objeto para el nuevo texto a analizar, le pone un id y lo guarda en memoria en el arreglo textos
# parámetros:
#         - objeto de tipo RegistroTexto, el cual contiene un solo campo llamado texto con el string a registrar.
# respuesta: 
#         - objeto de tipo RespuestaRegistro, el cual contieneun solo campo llamado id con el identificador del texto cargado.
def registrar_texto(objeto_texto: str) -> RespuestaRegistro:
    try:
        global textos
        id=len(textos)+1
        texto = ObjetoTextoAnalizar(texto=objeto_texto,id=id,resumen="",entidades=[])
        textos.append(texto.model_dump())
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

# Servicio para analizar texto
# parámetros:
#         - id: identificador del texto.
# respuesta: 
#         - objeto con el resumen y el listado de entidades extraídas.
def servicio_analizar_texto(registro_id: int) -> RespuestaAnalisis:
    try:
        global textos
        elemento_texto = [item for item in textos if item["id"] == registro_id][0]
        if elemento_texto["resumen"]=="": #Si no se ha hecho el análisis del texto, se hace y se guarda en el elemento.
            resumen , entidades = analizar_texto(elemento_texto["texto"]).content.split("|")
            elemento_texto["resumen"]=resumen
            elemento_texto["entidades"]=json.loads(entidades)
        return RespuestaAnalisis(resumen=elemento_texto["resumen"],entidades=elemento_texto["entidades"])
    except IndexError as err:
        print(f"Error en el id consultado {err=}")
        raise
    except ValueError as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
