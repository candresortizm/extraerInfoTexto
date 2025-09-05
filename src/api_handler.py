from typing import List
import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from extractor.extractor import registrar_texto, listar_textos, RegistroTexto, ObjetoTextoAnalizar, RespuestaRegistro

app = FastAPI(
    title="InfoTextExtractor",
    description="API para extraer y analizar información de textos. Permite obtener el resumen y entidades de textos previamente registrados.",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json"
)

v1_router = APIRouter(prefix="/api/v1")

@v1_router.post(
    "/document",
    response_model=RespuestaRegistro,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo texto para análisis",
    description="Registra un nuevo texto en el sistema para posterior análisis de entidades. El texto se almacena en memoria con un ID único.",
    responses={
        201: {
            "description": "Texto registrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1
                    }
                }
            }
        },
        400: {
            "description": "Error en la solicitud",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error al procesar el texto"
                    }
                }
            }
        }
    }
)
def cargar_pagina(texto: RegistroTexto) -> ObjetoTextoAnalizar:
    """
    Registra un nuevo texto en el sistema para análisis.
    
    - **texto**: El texto que se desea analizar posteriormente
    
    Retorna un objeto con el id del texto registrado.
    """
    try:
        response = registrar_texto(texto)
        return response
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error al procesar el texto: {str(err)}"
        )
    
@v1_router.get(
    "/ver_textos",
    response_model=List[ObjetoTextoAnalizar],
    summary="Obtener todos los textos registrados",
    description="Retorna un listado de todos los textos que han sido registrados en el sistema, incluyendo sus análisis y entidades extraídas (si los tiene).",
    responses={
        200: {
            "description": "Lista de textos obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "texto": "Juan Pérez es el CEO de la empresa TechCorp",
                            "id": 1,
                            "resultado": "Análisis completado",
                            "entidades": ["Juan Pérez", "TechCorp", "CEO"]
                        },
                        {
                            "texto": "La empresa está ubicada en Madrid, España",
                            "id": 2,
                            "resultado": "Análisis completado",
                            "entidades": ["Madrid", "España"]
                        }
                    ]
                }
            }
        }
    }
)
def get_tables() -> List[ObjetoTextoAnalizar]:
    """
    Obtiene todos los textos registrados en el sistema.
    
    Retorna una lista completa de todos los textos que han sido registrados,
    incluyendo sus metadatos, resultados de análisis y entidades extraídas.
    """
    response = listar_textos()
    return response
    
app.include_router(v1_router)

if __name__ == "__main__":
    # Run this as a server directly.
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("api_handler:app", host="0.0.0.0", port=port)
