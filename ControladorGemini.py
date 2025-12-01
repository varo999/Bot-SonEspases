from typing import List, Optional
from ConexionGemini import *
from AlmacenGemini import *
from ServicioGemini import *
import os

CLAVE_API = os.getenv("Clave_Api_Gemini")
class ControladorGemini:
    
    def __init__(self, clave_api: str):
        """Inicializa las tres capas de la aplicación."""

        self.conexion: ConexionGemini = ConexionGemini(clave_api=clave_api)
        self.cliente_gemini = self.conexion.obtener_cliente()
        
        self.repositorio: AlmacenGemini= AlmacenGemini(cliente=self.cliente_gemini)
        self.repositorio.iniciar_rag(nombre_almacen="MiAlmacenDeConsulta", ruta_carpeta="./Documentos")
        id_almacen_para_servicio = self.repositorio.obtener_almacen_activo_id()
        

        self.servicio: ServicioGemini = ServicioGemini(cliente=self.cliente_gemini,almacen_archivos=id_almacen_para_servicio,chequeo_cliente_func=self.obtener_cliente_gemini)
        
        print("Controlador Gemini listo. Capas inicializadas.")
        
    def obtener_cliente_gemini(self):
        """
        Devuelve el cliente de Gemini. 
        Si es None, intenta recuperarlo delegando a la capa de Conexión.
        """
        self.cliente_gemini = self.conexion.obtener_cliente()
        
        return self.cliente_gemini

    def eliminar_almacen_busqueda(self):
        self.repositorio.eliminar_almacen_busqueda()

    def hacer_pregunta(self, pregunta: str, historial: List[Tuple[str, str]]) -> Optional[str]:
        """
        Delega la pregunta a la capa de Servicio para la ejecución de la lógica RAG.
        """
        respuesta = self.servicio.hacer_pregunta(
            pregunta=pregunta, 
            historial=historial
        )
        
        # 2. Devolvemos el resultado al código que llamó al Controlador.
        return respuesta