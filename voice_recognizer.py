import pyaudio
import numpy as np
import speech_recognition as sr


#Duración y tasa de muestreo
duracion = 5
tasa_muestreo = 44100

print("Capturando audio...")

#Crear objeto PyAudio
p = pyaudio.PyAudio()

#Almacenar fragmentos de audio
fragmentos_audio = []

#Capturar audio en tiempo real
def capturar_audio(datos_entrada, cantidad_frames, info_tiempo, estado):
    fragmentos_audio.append(np.frombuffer(datos_entrada, dtype=np.int16))
    if len(fragmentos_audio) >= int(tasa_muestreo * duracion / 1024):
        return (datos_entrada, pyaudio.paComplete)  
    return (datos_entrada, pyaudio.paContinue)

#Configurar los parámetros del stream
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=tasa_muestreo,
                input=True,
                frames_per_buffer=1024,
                stream_callback=capturar_audio)

#Empezar a capturar audio en tiempo real
stream.start_stream()

#Esperar hasta que se haya capturado suficiente audio
while stream.is_active():
    pass

#Detener la captura y cerrar el stream
stream.stop_stream()
stream.close()
p.terminate()

#Concatenar fragmentos de audio
datos_audio = np.concatenate(fragmentos_audio)

#Configurar el reconocimiento de voz
reconocedor = sr.Recognizer()

#Convertir los datos de audio a un objeto AudioData
objeto_audio = sr.AudioData(datos_audio.tobytes(), sample_rate=tasa_muestreo, sample_width=2)

#Realizar el reconocimiento de voz
texto_reconocido = ""
try:
    texto_reconocido = reconocedor.recognize_google(objeto_audio, language="es-ES")
    print("Texto reconocido:", texto_reconocido)
except sr.UnknownValueError:
    print("No se pudo reconocer el audio")