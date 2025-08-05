# PCAGitHub.py — Asistente de voz con ChatGPT, TTS y STT en español.

import os
import sys
import json
import time
import signal
import threading
import keyboard
import winsound
import asyncio
import speech_recognition as sr
from openai import OpenAI
from playsound import playsound
from PIL import Image, ImageDraw
import edge_tts
import pyttsx3
import pystray

# Cargar API Key desde variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("No se encontró la clave API de OpenAI. Configúrala como variable de entorno 'OPENAI_API_KEY'.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

HISTORIAL_PATH = "chatHistorial.json"
if os.path.exists(HISTORIAL_PATH) and os.stat(HISTORIAL_PATH).st_size > 0:
    with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
        chatHistorial = json.load(f)
    print("Historial anterior cargado.")
else:
    chatHistorial = []
    print("ℹIniciando nuevo historial.")

def guardar_historial():
    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(chatHistorial, f, ensure_ascii=False, indent=4)
    print("Historial guardado.")

def signal_handler(sig, frame):
    print("\n⚠️ Cerrando programa...")
    guardar_historial()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def run_tray():
    icon = pystray.Icon("PCA")
    icon.icon = Image.new('RGB', (64, 64), color='white')
    icon.menu = pystray.Menu(pystray.MenuItem("Salir", lambda icon, item: sys.exit(0)))
    icon.run()

threading.Thread(target=run_tray, daemon=True).start()

def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language="es-ES")
        except Exception as e:
            print(f"Error: {e}")
            return None

def speak(text, rate="+20%"):
    try:
        async def run():
            output_file = "respuesta.mp3"
            communicate = edge_tts.Communicate(text=text, voice="es-MX-DaliaNeural", rate=rate)
            await communicate.save(output_file)
            playsound(output_file)
            os.remove(output_file)
        asyncio.run(run())
    except Exception as e:
        print(f"Error de TTS: {e}")

def generate_response(prompt, max_tokens=100):
    messages = [
        {
            "role": "system",
            "content": "Responde con claridad en menos de 80 palabras. Sé amigable y evita repetir ideas.",
        }
    ] + chatHistorial + [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("Presiona 'K' para hablar con el asistente.")
    try:
        while True:
            if keyboard.is_pressed('k'):
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    winsound.Beep(300, 100)
                    print("Escuchando...")
                    audio_data = []
                    while keyboard.is_pressed('k'):
                        try:
                            chunk = recognizer.listen(source, timeout=1, phrase_time_limit=2)
                            audio_data.append(chunk)
                        except sr.WaitTimeoutError:
                            pass
                    winsound.Beep(300, 100)

                    if audio_data:
                        audio = sr.AudioData(b"".join([c.get_raw_data() for c in audio_data]), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                        with open("input.wav", "wb") as f:
                            f.write(audio.get_wav_data())
                        text = audio_to_text("input.wav")
                        if text:
                            print(f"Tú: {text}")
                            if "terminar operacion" in text.lower():
                                break
                            response = generate_response(text)
                            if response:
                                print(f"🧠 Asistente: {response}")
                                speak(response)
                                chatHistorial.append({"role": "user", "content": text})
                                chatHistorial.append({"role": "assistant", "content": response})
    finally:
        guardar_historial()

if __name__ == "__main__":
    main()

