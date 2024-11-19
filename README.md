1. Instalar las dependencias
python -m pip install -r requirements.txt

2. Extraer los textos de audios
py etl\ExtraerTexto.py

3. Cargar los arreglos de las providencias extraidas
py etl\CargarTextosProvidencias.py

4. Cargar la información de las similitudes de las providencias 
py etl\CargarRelacionesSimilitud.py

5. Ejecutar la aplicación para visualización
streamlit run etl\Principal.py