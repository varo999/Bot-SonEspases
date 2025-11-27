from TelegramBot import*
from Llamada_Api import *
from MemoriaConversacional import *

class Controlador:
    def __init__(self, api_key: str, token : str,):
        # 🤖 Inicialización de la clase de la llamada a la API
        self.asistente_gemini = Llamada_Api_Gemini(clave_api=api_key,controlador=self)
        self.asistente_gemini.iniciar_rag( nombre_almacen ="TelegramBotRAGStore")


        self.memoria_conversacional=MemoriaConversacional()

        # 💬 Inicialización de la clase del bot de Telegram 
        self.bot_telegram = TelegramBot(token=token,controlador=self)
        self.bot_telegram .run()
        print("Controlador inicializado con el Asistente Gemini y el Bot de Telegram.")

    
    def hacer_pregunta(self, pregunta: str,user_id: int) -> str:
        ''' Pregunta para el Asistente Gemini '''

        print(f"Controlador: Recibida pregunta para Gemini: '{pregunta}'")
        print(f"Controlador: Procesando pregunta para el Usuario ID: {user_id}")
        historial_cargado = self.memoria_conversacional.cargar_historial(user_id)
        
        respuesta = self.asistente_gemini.hacer_pregunta(
            pregunta=pregunta,
            historial=historial_cargado)
        
        print("enviando pregutna a Gemini")
        if respuesta:
            self.memoria_conversacional.guardar_interaccion(user_id, pregunta, respuesta)
            return respuesta
        else:
            return "Lo siento, no pude obtener una respuesta de Gemini. Verifica la configuración del almacén."
        
    def limpiar_todo(self):
        """ Llama al método de instancia para borrar el almacén. """

        print("Controlador: Solicitando la eliminación del almacén de File Search...")
        
        # Llamar a la funcion eliminar_almacen_busqueda del AsistenteRAGGemini
        self.asistente_gemini.eliminar_almacen_busqueda()
        
        print("✅ Almacén de File Search borrado por el controlador.")