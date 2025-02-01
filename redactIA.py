import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer

# Ruta absoluta al modelo de idioma en español descargado y descomprimido
model_path = "D:\Proyectos\PROTOTIPO REDACT IA/vosk-model-es-0.42"

# Verificar si la ruta del modelo es correcta
if not os.path.isdir(model_path):
    raise Exception(f"La ruta del modelo no es correcta: {model_path}")

# Crear el modelo de Vosk
model = Model(model_path)

# Ruta relativa al archivo de audio que quieres transcribir
audio_file_path = "./TEST3.m4a"
converted_audio_file_path = "./TEST-m4a-convertido.wav"

# Convertir M4A a WAV usando FFmpeg
subprocess.run(['ffmpeg', '-i', audio_file_path, '-ar', '16000', '-ac', '1', converted_audio_file_path], check=True)
# Crear el reconocedor de Vosk con una frecuencia de muestreo de 16000 Hz
rec = KaldiRecognizer(model, 16000)

# Abrir el archivo de audio WAV convertido
with wave.open(converted_audio_file_path, "rb") as wf:
    # Verificar que el archivo de audio tenga una frecuencia de muestreo de 16000 Hz y un solo canal (mono)
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        print("El archivo de audio debe ser WAV con 16000 Hz, 16 bits y mono")
        exit(1)
    
    # Leer los frames de audio y procesarlos con Vosk
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(json.loads(result)['text'])

    # Obtener el resultado final
    final_result = rec.FinalResult()
    print(json.loads(final_result)['text'])

# Opcional: Eliminar el archivo WAV convertido después de la transcripción
os.remove(converted_audio_file_path)
    
    
    
    