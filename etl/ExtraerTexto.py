import os
import math
import json
from pydub import AudioSegment
import speech_recognition as sr
from dask import delayed, compute
from dask.distributed import Client
import time

def split_audio(file_path, segment_directory, segment_duration=60):
    """
    Divide un archivo de audio en segmentos más pequeños.
    :param file_path: Ruta del archivo de audio.
    :param segment_directory: Directorio para guardar los segmentos.
    :param segment_duration: Duración de cada segmento en segundos.
    :return: Lista de rutas de los segmentos generados.
    """
    segments = []
    try:
        audio = AudioSegment.from_wav(file_path)
        total_duration = math.ceil(audio.duration_seconds)

        for i in range(0, total_duration, segment_duration):
            segment = audio[i * 1000:(i + segment_duration) * 1000]
            segment_name = os.path.join(segment_directory, f"{os.path.basename(file_path)}_part{i}.wav")
            segment.export(segment_name, format="wav")
            segments.append(segment_name)
            print(f"Segmento creado: {segment_name}")
    except Exception as e:
        print(f"Error al dividir el audio {file_path}: {str(e)}")
    return segments

def process_audio_segment(file_path):
    """
    Transcribe un segmento de audio.
    :param file_path: Ruta del segmento de audio.
    :return: Transcripción del segmento.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="es-CO").lower()
    except Exception as e:
        text = f"Error processing {file_path}: {str(e)}"
    return text

def process_audio(file_path, segment_directory):
    """
    Procesa un archivo de audio completo, dividiéndolo en segmentos y transcribiendo.
    :param file_path: Ruta del archivo de audio.
    :param segment_directory: Directorio para guardar los segmentos.
    :return: Diccionario con metadatos y texto transcrito.
    """
    base_name = os.path.basename(file_path)
    providencia = os.path.splitext(base_name)[0]
    tipo = (
        "Constitucionalidad" if providencia.startswith("C") else
        "Auto" if providencia.startswith("A") else
        "Tutela" if providencia.startswith("T") else "Desconocido"
    )
    anio = "20" + providencia.split("-")[-1]

    segments = split_audio(file_path, segment_directory)
    full_text = ""
    for segment in segments:
        full_text += process_audio_segment(segment) + " "
        os.remove(segment)  # Limpia los archivos temporales
        print(f"Segmento eliminado: {segment}")
    
    return {
        "providencia": providencia,
        "tipo": tipo,
        "anio": anio,
        "texto": full_text.strip(),
    }

if __name__ == '__main__':
    start_time = time.time()
    client = None
    try:
        # Configuración de cliente Dask
        client = Client(
            n_workers=4,  # 2 trabajadores
            threads_per_worker=4,  # 4 hilos por trabajador
            memory_limit='3.5GB'  # Límite de memoria por trabajador
        )
        print("Cliente Dask configurado")

        # Directorios
        input_directory = r"C:\Users\LENOVO_LEGION_V\Downloads\Audios"
        output_directory = r"E:\ProyectoFinal\output"
        segment_directory = r"C:\Users\LENOVO_LEGION_V\Downloads\Segmentado"

        os.makedirs(output_directory, exist_ok=True)
        os.makedirs(segment_directory, exist_ok=True)

        # Procesar archivos de audio
        audio_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.endswith('.wav')]
        if not audio_files:
            print("No se encontraron archivos .wav en el directorio.")
            exit(1)
        
        tasks = [delayed(process_audio)(file_path, segment_directory) for file_path in audio_files]
        results = compute(*tasks)

        # Guardar resultados
        output_path = os.path.join(output_directory, "resultados.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"Resultados guardados en: {output_path}")
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
    finally:
        if client:
            client.close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo total de procesamiento: {elapsed_time:.2f} segundos")