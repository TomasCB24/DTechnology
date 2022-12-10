# DTechnology
DTechnology es un proyecto de *ecommerce* realizado en el ámbito de la asignatura Planificación y Gestión de Proyectos Informáticos de la Universidad de Sevilla.

## Pre-requisitos
- [Python 3.11](https://www.python.org/downloads/)
- [Docker 4.15.0](https://docs.docker.com/desktop/release-notes/)
- [WSL 2](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)



## Instalación local
1. Instale la versión especificada anteriormente de Python en su sistema operativo.
2. Para ejecutar el proyecto en local, abra una consola de comandos y ejecute los siguientes comandos:
    ```
    git clone https://github.com/TomasCB24/DTechnology.git
  
    cd .\DTechnology\
  
    pip install -r .\requirements.txt
  
    python .\manage.py makemigrations

    python .\manage.py migrate

    python .\manage.py loaddata "fixtures/initial.json"

    python .\manage.py runserver
    ```

3. Si ha llegado a este punto sin ningún error, debería estar ejecutando el proyecto  en local de forma satisfactoria. Podrá acceder a la ruta inicial a través del siguiente enlace: [http://localhost:8000](http://localhost:8000) 
   
 
## Despliegue en Docker
1. Es necesario tener Docker Desktop instalado y funcionando en el sistema. En caso de encontrarse en Windows, asegúrese de haber instalado previamente WSL en su versión 2 (disponible en los pre-requisitos).

2. A continuación, ejecute los siguientes comandos en una consola de comandos:
	  ```
    docker pull tomascb/dtechnology:latest
  
    docker run -p 8000:8000 -i -t tomascb/dtechnology
    ```

3. Finalmente, abra el navegador y acceda al siguiente enlace: [http://localhost:8000](http://localhost:8000)



## Despliegue en Internet
Además de todo lo anterior, el proyecto se encuentra desplegado en PythonAnywhere en el siguiente [enlace](http://dtechnology.pythonanywhere.com/).
