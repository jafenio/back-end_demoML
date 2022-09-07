# Microservicio DemoML.
Demo desarrollada backend.
## Requisitos.
- Contar con python 3.10.5
- Editor de Swagger.

## Crear el entorno virtual (Windows).
```
py -3 -m venv msdemo
```
## Activar el entorno virtual (Windows).
```
. msdemo/Scripts/activate
```
## Instalacion de dependencias.
```
pip install -r requirements.txt
```
## Variables de entorno.
```
export FLASK_APP=main.py
```
## Ejecutar el proyecto.
```
flask run --host=0.0.0.0
```

### Librerias usadas
Se pueden instalar de la siguiente forma:
```
pip install pandas
pip install Flask
pip install -U flask-cors
pip install sklearn==0.0
pip install tensorflow
```
