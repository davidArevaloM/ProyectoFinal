
import pymongo
import os
from pymongo import MongoClient
import json

connection_str = "mongodb+srv://ADMIN2:Vapu021292@cluster0.edkufrd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_str)

db = client["mlds3"]

if "providencias" in db.list_collection_names():
    db.drop_collection("providencias")

collection = db["providencias"]

directorio = "C:/Users/USER/Downloads/relatoria"

# Cargar cada archivo JSON en la colección de MongoDB
for filename in os.listdir(directorio):
    if filename.endswith(".json"):  # Asegurarse de que el archivo es JSON
        archivo_json = os.path.join(directorio, filename)

        # Abrir y cargar el contenido del archivo JSON
        with open(archivo_json, 'r', encoding="utf-8") as file:
            try:
                datos = json.load(file)

                # Insertar los datos en MongoDB
                if isinstance(datos, list):
                    # Si los datos son una lista, insertarlos como varios documentos
                    collection.insert_many(datos, ordered=False)  # `ordered=False` ignora errores de duplicados y continúa
                else:
                    # Si los datos son un solo objeto, insertarlo como un único documento
                    collection.insert_one(datos)
                
                print(f"Archivo {filename} cargado con éxito.")

            except pymongo.errors.BulkWriteError as e:
                print(f"Error de escritura en lote en el archivo {filename}: {e}")
            except json.JSONDecodeError as e:
                print(f"Error al leer el archivo {filename}: {e}")
            except Exception as e:
                print(f"Error al cargar el archivo {filename} en MongoDB: {e}")