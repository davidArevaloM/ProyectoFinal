
1. Instalar las dependencias
python -m pip install -r requeriments.txt

2. Extraer los textos de audios


3. Cargar los arreglos de las providencias extraidas
py etl\CargarTextosProvidencias.py

2. Cargar la información de las similitudes de las providencias 
py etl\CargarRelacionesSimilitud.py

3. Ejecutar la aplicación para visualización
streamlit run etl\Principal.py