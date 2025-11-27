from typing import Dict, List, Tuple

class MemoriaConversacional:
    """
    Gestiona el historial de conversación (Pregunta, Respuesta) para múltiples usuarios.
    
    El historial se almacena en un diccionario en memoria, donde la clave es el 
    ID de usuario (int) y el valor es una lista de tuplas (pregunta, respuesta).
    """

    def __init__(self):
        
        self.historial: Dict[int, List[Tuple[str, str]]] = {}

    def cargar_historial(self, user_id: int) -> List[Tuple[str, str]]:
        """
        Carga el historial de conversación para un usuario específico.
        """
        if user_id not in self.historial:
            self.historial[user_id] = []
        return self.historial.get(user_id, [])

    def guardar_interaccion(self, user_id: int, pregunta: str, respuesta: str):
        """
        Guarda el último par (pregunta, respuesta) en el historial del usuario.
        """
        if user_id not in self.historial:
            self.historial[user_id] = []
        self.historial[user_id].append((pregunta, respuesta))
    