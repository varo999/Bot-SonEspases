import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes,
    PicklePersistence
)
import sys

tokens=["8545696064:AAFIX_bmizeaLIxlOEYXwIbAkf-f3kXQW9U"
"8384733305:AAFCdE9VFb4gC4Cook7AKuEnkNJVy-JvSPc"
"8269103613:AAG8jYrgULoz2_CKxtbAzgtM8_8afQE7C8E"
"7762332336:AAEMfzF_0WiZjcQ10ELlsEKVBC06wJgMNGU"
"8517231263:AAGOpOetMn_eVB24N89ye0IJhfLERx0XJ8w"]

class TelegramBot:
    def __init__(self, token: str, controlador):
        persistence = PicklePersistence(filepath="user_data.pkl")
        
        self.app = (
            ApplicationBuilder()
            .token(token)
            .persistence(persistence)
            .build()
        )
        self._add_handlers()
        self.controlador = controlador

    def _add_handlers(self):
        """Método privado para agregar todos los handlers y el handler de errores."""
        
        self.app.add_handler(CommandHandler("start", self.start))
        
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.responder_a_pregunta)
        )
        
        self.app.add_error_handler(self.error_handler)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Maneja el comando /start y da la bienvenida."""
        saludo = f'¡Hola, {update.effective_user.first_name}! Soy tu asistente RAG de Gemini. Hazme una pregunta sobre los documentos que he indexado.'
        await update.message.reply_text(saludo)

    async def responder_a_pregunta(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Captura el mensaje de texto, lo envía al Controlador para la lógica RAG 
        y responde al usuario con la respuesta de Gemini.
        """
        user_text = update.message.text
        
        user_id = update.message.from_user.id

        await update.message.reply_text("🔎 Buscando y generando respuesta con Gemini...")
        
        try:
            respuesta_gemini = await asyncio.to_thread(
                self.controlador.hacer_pregunta, 
                user_text,
                user_id
)
            await update.message.reply_text(respuesta_gemini)
            
        except Exception as e:
            error_msg = f"❌ Ocurrió un error al procesar tu pregunta con Gemini: {e}"
            print(error_msg, file=sys.stderr)
            await update.message.reply_text(error_msg)
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler que registra los errores causados por los Updates."""
        print(f"Update '{update}' causó error: {context.error}", file=sys.stderr)

    def run(self):
        """Método para iniciar el bot."""
        print("Bot iniciado (clase TelegramBot), esperando mensajes...")
        self.app.run_polling()