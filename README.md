![Flangsbot Logo](https://github.com/Flangrys/flangsbot-discord-bot)

# Descripcion

Flangsbot es un projecto personal que pretende servir como una herramienta de gestion y automatizacion de tareas, ademas de ofrecer otras funcionalidades
propias de un bot de Discord.

Este proyecto surge desde una necesidad concreta de los estudiantes de la [**Universidad Nacional de Rio Cuarto**](https://unrc.edu.ar) quienes buscaban agilizar el entorno comunicacional entre los medios oficiales y extra oficiales, ya sean Discord, Whatsapp, Slack, Classroom, y otros.

Con ello en mente, se propuso desarrollar un **bot** de Discord que pudiese acatar estos problemas. Ademas de ello, se propusieron los siguientes objetivos a lograr en el corto plazo:

- [ ] Sistema de gestion de ingresantes.
- [ ] Sistema de tickets.
- [ ] Sistema de notificaciones basado en el servicio de "E-Noti".
- [ ] Sistema de recordatorios basado en el calendario academico.
- [ ] Panel de sonidos integrado.
- [ ] Reproductor de musica.

# Desarrolladores

En esta seccion se concentran los aspectos mas importantes para todos los desarrolladores, ya sean nuevos contribuidores o contribuidores vigentes.

## Como contribuir

En esta seccion se encuentra condensado todo lo que necesita un desarrollador para colaborar en el proyecto.

> [!IMPORTANT]
> Si no eres estudiante de la UNRC no tendras acceso a ciertas funcionalidades del proyecto, que por naturaleza, requieren de que tengas a la mano tus credenciales.

### Espacio de trabajo

Si trabajas con **Visual Studio Code**, te recomendamos que uses la configuracion que ya se provee en el archivo `.\vscode\extensions.json` ya que posee ciertas extensiones que te ayudaran en el desarrollo. Ademas de ello, ya se provee un archivo de configuracion `.\vscode\settings.json`, por lo que no tienes que preocuparte mucho por configurar tu espacio de trabajo a mano.

A continuación deberas crear tu entorno virtual para poder trabajar sin conflictos entre dependencias. Para ello necesitaras tener a la mano tu terminal, en el que invocaras el siguiente comando:

```bash
pip install virtualenv
```

Y luego, sobre el directorio del proyecto, deberás invocar el siguiente comando:

```bash
python -m venv venv
```

Luego de haber ejecutado estos dos ultimos comandos, deberas invocar el script `.\venv\Bin\activate` (Linux) o `.\venv\Scripts\Activate.ps1` (Windows). Esto establece tu un entorno aislado de desarrollo en el que tus dependencias no entran en conflicto con las dependencias globales.

```bash
pip install -r ./requirements.txt
```

Con estos pasos ya estas listo para colaborar en el proyecto.

## Desarrollo

En esta sección encontraras los puntos claves que necesitas conocer para llevar a cabo el desarrollo de **Flangsbot**, en los cuales se recalcan ciertos aspectos que son requeridos.

<!-- TODO [ ] Convenciones. -->

### Despliegue en local.

El despliegue de este proyecto en forma local no es recomendado ya que se necesita contar con el acceso a ciertas credenciales para servicios de terceros y otras variables de entorno que son privadas. Por lo que no aconsejamos desplegar localmente este proyecto.

> [!INFO]
> En una proxima version, se utilizara un sistema de **feature flags** el cual permitira habilitar o deshabilitar ciertas caracteristicas de este software.

Para desplegar el proyecto localmente deberas establecer la variable de entorno `FLANGSBOT_DISABLE_SISINFO` en `1`. De esta forma estaras deshabilitando ciertas funcionalidades que impiden el desarrollo localmente, ya que estas precisan de secretos y otras variables de entorno que son privadas.

Ademas de esto ultimo, para lanzar el cliente necesitaras invocar en el terminal con el entorno virtual habilitado, el siguiente comando:

```bash
python main.py
```

Con esto hecho, puedes darle a las teclas <kbd>CTRL</kbd> + <kbd>C</kbd> para terminar el programa.

### Testing

Recomendamos que si es necesario hacer pruebas ya sean para comandos, eventos, tareas u otras piezas de software, no intentes hacerlo formalmente, es decir, utilizar una libreria de testing como pytest ya que sera añadir capas de complejidad al test. Esto es debido a que la libreria de [discord.py](https://github.com/Rapptz/discord.py) no facilita la escritura de test.

Por esto último, optamos por no introducir más capas de abstracciones al software y priorizando las pruebas de escritorio o pruebas funcionales, usando una instancia local del software, para este ultimo caso.

### Variables de entorno

Este software utiliza una serie de variables de entorno que son necesarias para que cliente pueda funcionar, las cuales varias de ellas se han nombrado aquí. A continuación encontrarás un listado de todas ellas y para que se utilizan:

| Nombre de la variable      | Descripcion                                                        | Tipo de dato | Valores posibles | Requerido |
| -------------------------- | ------------------------------------------------------------------ | ------------ | ---------------- | --------- |
| FLANGSBOT_DEBUG_MODE       | Permite el registro detallado en la consola acerca del programa.   | **Number**   | [0-1]            | NO        |
| FLANGSBOT_DEBUG_GUILD      | Almacena el ID del servidor donde se prueba el bot.                | **Number**   | -                | SI        |
| FLANGSBOT_DEBUG_GUILD      | Almacena el ID del servidor donde se prueba el bot.                | **Number**   | -                | SI        |
| FLANGSBOT_SECRET_KEY       | Almacena el token del cliente.                                     | **String**   | -                | SI        |
| FLANGSBOT_SISINFO_USER_DNI | Almacena el usuario asociado al Sistema de Informacion de la UNRC. | **Number**   | -                | SI        |
| FLANGSBOT_SISINFO_PASSWORD | Almacena las credenciales de login para el servicio SISINFO.       | **String**   | -                | SI        |
