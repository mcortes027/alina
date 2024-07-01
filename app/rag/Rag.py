import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from ollama import Client
from ollama import AsyncClient  # Para hacer el cliente asíncrono
from storage.ChromaVectorStore import ChromaVectorStore
import ollama, logging, os
from gtts import gTTS
from moviepy.editor import AudioFileClip
import os
import pyttsx3
from pydub import AudioSegment
class Rag:
    
    def __init__(self, host_ollama='172.18.0.3', port=11434, model="llama3", chroma_host='172.18.0.2', asincrono=False):
        self._inicia_logs()
        
        self.ChromaDB = ChromaVectorStore(host=chroma_host, host_Ollama=host_ollama)
        
        self.model = model
        url_ollama = f"http://{host_ollama}:{port}"
        
        if asincrono:
            self.clientOllama = AsyncClient(host=url_ollama)
        else:
            self.clientOllama = Client(host=url_ollama)
        
        
    def queryllm(self, query):
        """
        Realiza una consulta al modelo de lenguaje.
        
        Args:
            query (str): La consulta que se le hará al modelo de lenguaje.
            
        Returns:
            str: La respuesta del modelo de lenguaje.
        """
        #try:
        #    contexto = self.ChromaDB.get_documents(query)
        #    self.logger.info("Contexto recuperado de la base de datos Chroma.")
        #except Exception as e:
        #    self.logger.error(f"Error al recuperar contexto de la base de datos Chroma: {e}")
        #    return f"Lo siento, por problemas técnicos no puedo responder a tu pregunta en este momento.\nInténtelo más tarde.\n\nGracias.\n\n Error al recuperar contexto de la base de datos Chroma \\n {e}"
        
        #prompt = f"Pregunta: {query}\n\nContexto (responde solo sobre el contenido del texto entregado): {contexto}\n\nLa Respuesta siempre en Español"
        
        
        prompt = (
            f"Pregunta: {query}\n\n"
        #    f"Contexto (Responde solo utilizando la informacion del texto proporcionado): {contexto}\n\n"
        #    "Instrucciones:\n"
        #    "1. Responde basandote en la informacion proporcionada en el contexto.\n"
        #    "2. Puedes añadir informacion inventada que este relacionada con el contexto.\n"
            "3. Responde sin olvidar que eres Alina de la Capilla Lunar una joven de veintidos años cerrada, vacilona e irónica.\n"
            "4. No respondas más de diez líneas\n"
            "5. La respuesta debe estar completamente en español.\n"
            "6. Debes responder con lenguaje medieval simple, no te presentes cada vez\n\n"
        )        

        try:
            respuestalln = self.clientOllama.chat(model="llama3", 
                                    messages=[{"role": "system", "content": prompt}],
                                    options={"temperature": 0})
            self.logger.info("Respuesta obtenida del modelo de lenguaje.")
            
            return respuestalln['message']['content']
        except Exception as e:
            self.logger.error(f"Error al obtener respuesta del modelo de lenguaje: {e}")
            return f"Lo siento, por problemas técnicos no puedo responder a tu pregunta en este momento.\nInténtelo más tarde.\n\nGracias. \n\nError al obtener respuesta del modelo de lenguaje.{e}"
    
    def info_llm(self):
        return ollama.show('llama3')
    
    def _inicia_logs(self):
        """
        Inicializa los registros de log.

        Crea un directorio de registros llamado "Log_System" si no existe.
        Configura el registro de eventos en un archivo llamado "system.log" dentro del directorio de registros.
        Establece el nivel de registro en INFO.
        Utiliza el formato de registro: '%(asctime)s %(levelname)s %(name)s %(message)s'.
        Utiliza el formato de fecha: '%m/%d/%Y %I:%M:%S %p'.
        """
        log_dir = "Log_System"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename=os.path.join(log_dir, 'system.log'), 
                            level=logging.INFO, 
                            format='%(asctime)s %(levelname)s %(name)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        
        self.logger = logging.getLogger(__name__)

    def to_audio(self, response_text, output_filename):
        """
        Converts the given response text into an audio file with a female voice.

        Args:
            response_text (str): The text to convert to audio.
            output_filename (str): The base filename for the output without extension.

        Returns:
            str: The path to the generated MP4 audio file.
        """
        # Convert text to speech and save as MP3
        tts = gTTS(text=response_text, lang='es', slow=False)
        mp3_filename = f"{output_filename}.mp3"
        tts.save(mp3_filename)
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_filename)

        # Export the audio to WAV
        wav_filename = f"{output_filename}.wav"
        audio.export(wav_filename, format="wav")

        # Clean up the MP3 file
        #os.remove(mp3_filename)

        return mp3_filename

    def convert_mp3_to_wav(mp3_file_path, wav_file_path):
        """
        Converts an MP3 file to WAV format.

        Args:
        mp3_file_path (str): The file path of the source MP3 file.
        wav_file_path (str): The file path for the output WAV file.
        """
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_file_path)

        # Export the audio to WAV
        audio.export(wav_file_path, format="wav")

# Ejemplo de uso Asincrono:
# async def main():
#      llm = Rag(asincrono=True)
#      query = "Crea un resumen con los requisitos de las ayudas al transporte de los alumnos que hacen FP"

#      async for respuesta in llm.queryllm_stream(query):
#          print(respuesta)

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())

#Ejemplo de uso NO Asincrono:
if __name__ == '__main__':
    llm = Rag()
    query = "¿Cuanto quieres a Manolo?"
    respuesta = llm.queryllm(query)
    audio = llm.to_audio(respuesta, "/audio/response_audio")
    print(respuesta)
