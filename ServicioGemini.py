from typing import List, Tuple, Callable, Dict, Any, Optional
from google import genai
from google.genai import types

class ServicioGemini:

    def __init__(self, cliente: genai.Client, almacen_archivos: Optional[str] = None,chequeo_cliente_func: Callable[[], genai.Client] = None):
        
        self.cliente = cliente
        self.chequeo_cliente = chequeo_cliente_func
        self.almacen_archivos = almacen_archivos

    def hacer_pregunta(self, pregunta: str, historial: List[Tuple[str, str]], modelo: str = "gemini-2.5-flash", top_k: int = 3):
        """
        Realiza una pregunta a Gemini, utilizando el historial de conversación 
        y la herramienta FileSearch para RAG, restringiendo la respuesta solo a los documentos.
        """
        if self.chequeo_cliente:
            try:
                # Llama a la función inyectada. Si tiene éxito, devuelve un cliente.
                # Este cliente puede ser el mismo o uno nuevo y restaurado.
                self.cliente = self.chequeo_cliente()
            except RuntimeError as e:
                # Si la conexión falla permanentemente (ej. clave API caducada)
                print(f"❌ Error Fatal: No se pudo asegurar ni restaurar la conexión: {e}")
                return None

        if not self.almacen_archivos:
            print("❌ Error: No hay FileSearchStore configurado para hacer preguntas.")
            return None

        nombre_almacen = self.almacen_archivos
        
       
        print(f"\n[DEBUG 1] Historial recibido (Tipo: {type(historial)}, Longitud: {len(historial)}):")
        print(historial)
        
        contents = self._crear_estructura_conversacion(historial, pregunta)
        
       
        print(f"[DEBUG 2] Contenido a enviar a Gemini (Longitud: {len(contents)}):")
        if contents:
            
            try:
                print(f"  Último Rol: {contents[-1].role}, Texto: {contents[-1].parts[0].text[:80]}...") 
            except Exception:
                print("  El formato del objeto Content puede ser incorrecto o estar vacío.")
        else:
            print("  ❌ La lista 'contents' está vacía. ¡Revisa _crear_estructura_conversacion!")
       
        system_instruction = (
            "Eres un asistente de búsqueda de documentos. Tu única fuente de información "
            "para responder a las preguntas es el contenido que se te proporciona "
            "a través de la herramienta File Search. Si no puedes encontrar la respuesta "
            "en los documentos, debes responder claramente: 'No pude encontrar la respuesta "
            "en los documentos proporcionados'."
        )
        # ---------------------------------------------
        
        try:
            response = self.cliente.models.generate_content(
                model=f"models/{modelo}",
                contents=contents, 
                config=types.GenerateContentConfig(
                    # Agregamos la instrucción del sistema
                    system_instruction=system_instruction, 
                    tools=[
                        types.Tool(
                            file_search=types.FileSearch(
                                file_search_store_names=[nombre_almacen],
                                top_k=top_k
                            )
                        )
                    ]
                )
            )

            answer = response.text
            print("\n💬 Respuesta de Gemini:")
            print(answer)
            return answer

        except Exception as e:
            # --- DEBUG 3: Captura de Error de la API (IMPORTANTE) ---
            print(f"❌ Error al hacer la pregunta (API): {e}")
            # --------------------------------------------------------
            return None

    def _crear_estructura_conversacion(self, historial: List[Tuple[str, str]], nueva_pregunta: str) -> List[types.Content]:
        """
        Convierte el historial de tuplas (pregunta, respuesta) en el formato
        List[Content] que espera la API de Gemini (alternando 'user' y 'model'),
        usando la sintaxis del constructor directo para evitar errores.
        """
        conversacion = []
        
        # 1. Añadir el historial previo
        for pregunta, respuesta in historial:
            # Turno del usuario
            conversacion.append(
                types.Content(role="user", parts=[types.Part(text=pregunta)]) # <--- ¡CAMBIO AQUÍ!
            )
            # Turno del modelo (respuesta previa)
            conversacion.append(
                types.Content(role="model", parts=[types.Part(text=respuesta)])  # <--- ¡CAMBIO AQUÍ!
            )
            
        # 2. Añadir la pregunta actual del usuario
        conversacion.append(
            types.Content(role="user", parts=[types.Part(text=nueva_pregunta)]) # <--- ¡CAMBIO AQUÍ!
        )
        
        return conversacion