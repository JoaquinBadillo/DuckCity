# Multiagentes

Este proyecto simula la movilidad de un grupo de agentes que representan coches en una ciudad. Estos agentes tienen distintos destinos que se escogen de forma aleatoria y tienen como objetivo llegar a dichas ubicaciones.

Se asume que los agentes conocen la ciudad, por lo que pueden calcular rutas eficientes  (en términos de disntacia) usando A*, sin embargo, no conocen la ubicación de los demás agentes, por lo que sus rutas no siempre serán las mejores considerando el tiempo que les tomará llegar a su destino. Por esta razón cuentan con otros comportamientos para tomar decisiones autónomas que les permitan navegar la ciudad y tratar de evitar congestionamientos.

## Stack de Tecnología

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Blender](https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white)
![Unity](https://img.shields.io/badge/unity-%23000000.svg?style=for-the-badge&logo=unity&logoColor=white)

## Uso

### Levantar el Servidor
Hay muchas maneras de levantar el servidor, aquí enlistamos algunas que evitan instalar paquetes globalmente.

#### Usando Docker Compose

```bash
cd Backend && \
docker compose up
```

#### Usando únicamente el Dockerfile

```bash	
cd Backend && \
docker build -t multiagentes . && \
docker run -p 8080:8080 multiagentes
```

#### Usando venv

```bash
cd Backend && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
python3 app.py
```

### Levantar el Cliente

**Es importante que el servidor esté corriendo para que la visualización funcione correctamente.**

El cliente de esta visualización está hecho con Unity. La forma más sencilla de utilizarlo es instalar Unity Hub, abrir el proyecto y abrir la escena `Assets/Scenes/Agents.unity`. Una vez que esté abierta la escena, se puede ejecutar la visualización presionando el botón de _play_.

## Contribuciones

Este proyecto se realizó para una clase de Gráficas Computacionales y Multiagentes. Después de su entrega aceptamos contribuciones de cualquier tipo, ya sea código, documentación, ideas, etc. Para contribuir, por favor sigue los siguientes pasos:

1. Crea un fork del repositorio
2. Crea una rama con el nombre de la funcionalidad que quieres agregar
3. Haz tus cambios
4. Crea un pull request

