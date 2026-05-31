# Sistema de gestion de una Papeleria

Una aplicacion de escritorio desarrollada en PYthon utilizando la libreria grafica Tkinter. 
Este sistema permite:
- Gestionar la venta de productos de papeleria
- Gestionar el inventario
- Gestionar clientes y proveedores
- Realizar consultas del negocio

## Tecnologias utilizadas

- Lenguaje: Python 3.x
- Base de datos: MySQL
- Libreria GUI: Tkinter

## Requisitos previos

Asegurate de tener instalado lo siguiente en tu maquina local antes de comenzar:
- [Python 3.10 o superios](https://www.python.org/downloads/)
- Servidor MySQL ejecutandose localmente
- Git

## Instalacion y configuracion local

Sigue estos paso para levantar el entorno de desarrollo:

### 1. Clonar el repositorio
```bash
git clone https://github.com/Kev-Hdz/Papeleria-con-Tkinter.git
```
### 2. Crear y activar el entorno virtual
Es indispensable usar un entorno virtual para no mezclar dependencias.

```bash
# En windows:
python -m venv venv
venv\Scripts\activate

# En Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
El proyecto utiliza un archivo `config.py` para leer credenciales de manera segura.
1. Haz una copia del archivo de plantilla:
- Copia `.env.example` y renombralo a `.env`
2. Abre el nuevo archivo `.env` y coloca tus credenciales locales de MySQL

### 5. Configurar la base de datos
1. Abre tu cliente de MySQL (consola, DBeaver, phpMyAdmin, etc.).
2. Ejecuta el script inicial ubicado en `db/esquema_inicial.sql` para crear la base de datos y las tablas necesarias.

## Ejecucion del proyecto
Una vez configurado todo, puedes iniciar la aplicacion ejecutando:
```bash
python main.py
```

## Ejecucion de pruebas
Este proyecto cuenta con un conjunto de pruebas para garantizar su estabilidad. Para correr todas las pruebas de la carpeta `tests/`, ejecuta:
```bash
# Si usar pytest
pytest tests/
```
