from typing import List
import uvicorn
from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Body
from extractor.servicios import registrar_texto, listar_textos, ObjetoTextoAnalizar, RespuestaRegistro, servicio_analizar_texto
from extractor.models import RespuestaRegistro, ObjetoTextoAnalizar, RespuestaAnalisis
from extractor.security import verify_token, SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime, timezone, timedelta

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
    description="Registra un nuevo texto en el sistema para posterior resumen y análisis de entidades. El texto se almacena en memoria con un ID único.",
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
def cargar_texto(texto: str = Body(..., media_type="text/plain")) -> ObjetoTextoAnalizar:
    """
    Registra un nuevo texto en el sistema para análisis.
    
    - **texto**: El texto que se desea analizar posteriormente
    
    Retorna un objeto con el id del texto registrado.
    """
    try:
        print("len: "+str(len(texto)))
        response = registrar_texto(texto)
        return response
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error al procesar el texto: {str(err)}"
        )

@v1_router.post("/document/{texto_id}/analyze",
    response_model=RespuestaAnalisis,
    status_code=status.HTTP_200_OK,
    summary="Análisis de un texto previamente registrado.",
    description="Hace el llamado del LLM con el texto cargado, retorna el resumen y el listado de entidades. Si ya se había analizado, responde lo previamente obtenido, sin llamar al LLM.",
    responses={
        200: {
            "description": "Texto analizado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "resumen": "Acá se presenta el resumen del texto cargado.",
                        "entidades": ["uno","dos","tres"]
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
    })
def post_analizar_texto(texto_id: int) -> RespuestaAnalisis:
    """
    Realiza el análisis.
    
    - **texto_id**: Identificador del texto previamente cargado.
    
    Retorna un objeto con el resumen del texto y las entidades principales extraídas.
    """
    try:
        response = servicio_analizar_texto(texto_id)
        return response
    except IndexError as err:
        print(f"Error en el id consultado {err=}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error al consultar el identificador enviado: {str(err)}"
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error al procesar el texto: {str(err)}"
        )
    
@v1_router.get(
    "/queries",
    response_model=List[ObjetoTextoAnalizar],
    summary="Obtener todos los textos registrados",
    description="Retorna un listado de todos los textos que han sido registrados en el sistema, incluyendo sus análisis y entidades extraídas (si los tiene). Necesita enviar un token válido.",
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
def get_textos(_: None = Depends(verify_token)) -> List[ObjetoTextoAnalizar]:
    """
    Obtiene todos los textos registrados en el sistema.
    
    Retorna una lista completa de todos los textos que han sido registrados,
    incluyendo sus metadatos, resultados de análisis y entidades extraídas.
    """
    try:
        response = listar_textos()
        return response
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Ocurrió una excepción {err=}, {type(err)=}")
    


@v1_router.post("/login",
    status_code=status.HTTP_200_OK,
    summary="Método de inicio de sesión",
    description="Retorna un nuevo token (jwt), si el loggeo fue exitoso.",
    responses={
        200: {
            "description": "Token generado correctamente.",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "abcd1234"
                    }
                }
            }
        }
    })
def login():
    try:
        payload = {
            "sub": "usuario_prueba",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=1)  # el token expira en 1 minuto
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Ocurrió una excepción {err=}, {type(err)=}")
    
app.include_router(v1_router)

if __name__ == "__main__":
    # Run this as a server directly.
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("api_handler:app", host="0.0.0.0", port=port)
