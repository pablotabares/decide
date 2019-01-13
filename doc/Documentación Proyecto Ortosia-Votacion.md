# Decide-Ortosia-Votacion

Grupo de teoría: 1  
ID de opera: 140 (Grupo:27)  
Miembros del grupo: Nombre del alumno (usuario de GitHub), nota de esfuerzo y correo asociado
* Lozano Pineda, José Ángel (angelxwars), 5 - angelxwars@gmail.com
* Pérez Llorente, Ángel (agepere), 5 - angperllo@alum.us.es 
* Sánchez Montiel, José Luis (jlsanchezm), 5 - jossanmon6@alum.us.es
* Valero García, Luis (luisval11), 5 - luivalgar@alum.us.es 

Enlaces de interés: 
* https://github.com/pablotabares/decide (master)
* https://github.com/pablotabares/decide/tree/ortosia-prepro (preproducción)
*	https://github.com/pablotabares/decide/tree/ortosia-votacion (primera rama master para nuestro módulo)
* https://github.com/pablotabares/decide/tree/ortosia-votacion-develop (develop)
* https://github.com/pablotabares/decide/tree/ortosia-votacion-prepro (debido a conflictos se migró a esta rama como master para nuestro módulo)
* https://decide-ortosia-votacion.herokuapp.com (despliegue de la rama Ortosia-Votacion-Prepro en Heroku)
* https://decide-ortosia.herokuapp.com (despliegue de la integración en Heroku)
* [Decide-Ortosia-Votacion](#Decide-Ortosia-Votacion)
* [Resumen](#Resumen)
* [Introducción y contexto](#Introducción-y-contexto)
* [Descripción del sistema](#Descripción-del-sistema)
* [Planificación del proyecto](#Planificación-del-proyecto)
* [Entorno de desarrollo](#Entorno-de-desarrollo)
* [Gestión de incidencias](#Gestión-de-incidencias)
* [Gestión de depuración](#Gestión-de-depuración)
* [Gestión de liberaciones, despliegues y entregas](#Gestión-de-liberaciones,-despliegues-y-entregas)
* [Mapa de herramientas](#Mapa-de-herramientas)
* [Gestión del código fuente](#Gestión-del-código-fuente)
* [Ejercicio de propuesta de cambio](#Ejercicio-de-propuesta-de-cambio)
* [Conclusiones y trabajo futuro](#Conclusiones-y-trabajo-futuro)

# Resumen

Nos han planteado un desarrollo de un proyecto previo con funcionalidades relativas a la votación de manera electrónica. Dicha plataforma, se llama “Decide”. Debemos ampliar el sistema mediante el uso de la integración continua. 

Debido a la estructura modular del proyecto, se distribuyeron los problemas intrínsecos a dichos módulos por grupo. Los avances en los distintos grupos implican la necesidad de comunicación con el resto de los grupos para que sus correspondientes módulos se adapten a las mejoras realizadas. 


# Introducción y contexto

En nuestro proyecto intervienen 8 módulos diferenciados, e intervienen 8 equipos, pero no todos los equipos tienen asignado un módulo distinto. Tenemos 2 grupos para el módulo de Cabina y ninguno para el de módulo de Almacenamiento. 

En nuestro caso, tenemos asignado el módulo de Votación que abarca lo relacionado a las votaciones y las preguntas incluidas en ellas.  

Debido a la relevancia de nuestro módulo, estamos en permanente contacto con el resto de los módulos ya que, ante cualquier mejora desarrollada por nosotros, conllevará una modificación en alguno/s del resto de los módulos. Así mismo, cualquier mejora del resto de los grupos, también implica cambios en nuestro módulo.

# Descripción del sistema

Los módulos participantes en el desarrollo del proyecto son los siguientes:
*	Ortosia-authentication: Sistema de autenticación para saber quién puede votar.
* Ortosia-store:  Almacenamiento de los datos (ningún grupo en concreto)
* Ortosia-booth: Cabina de votación.
* Ortosia-census: Censo de personas para las votaciones.
* Ortosia-mixnet: Módulo orientado a la criptografía.
* Ortosia-postproc: Post-procesado de la votación. 
* Ortosia-visualizer: Visualizador de los votos.
* Ortosia-voting: Votaciones.

Durante el proceso de integración continua, hemos tratado de conectar todos los módulos en desarrollo por un grupo. Principalmente, nuestra relación directa es con Authentication, Booth, Mixnet y Postprocesado.

1.	Automatización de la creación de una votación tipo referéndum.
1.	Posibilidad de aumentar el número de preguntas dentro de una votación.
1.	Adición de valor a las preguntas dentro una votación. 
1.	Inclusión de las vistas para todas las mejoras desarrolladas.
1.	Mejora del diseño de las vistas haciendo uso de la librería “Bootstrap”.
1.	Adición de importancia de una pregunta.
1.	Mejora de la API en distintos campos.
1.	Posibilidad de incluir fecha de inicio en la creación de la votación.
1.	Posibilidad de crear votación en 2 fases según respuestas a preguntas previas.
1.  Adición de los nuevos campos al formato JSON de una votación

Funcionalidades requeridas por otros módulos que hemos desarrollado:

1. Añadir peso a las preguntas
1. Enviar a postprocesado un JSON donde se indique si la votación es con peso o no
1. Controlar errores en las comunicaciones con mixnet para el método tally
1. Enviar el token de admin en cada operación con mixnet para que sólo pueda realizar ciertas operaciones un superusuario
1. Posibilidad de crear votaciones con múltiples preguntas a traves de la API por POST

# Planificación del proyecto
Las tareas asignadas a cada integrante del grupo fueron: (Se han realizado todas)

* Lozano Pineda, José Ángel:
  * Adición de importancia de una pregunta
  * Mejora de la API
  * Incluir fecha de inicio en creación de votación
  * Mejora del JSON de una votación
  * Controlar errores para Mixnet
* Pérez Llorente, Ángel:
  * Posibilidad de crear votación en 2 fases según respuestas a preguntas previas
  * Mejora del JSON de una votación
  * Añadir el peso y enviarlo a postprocesado
  * Crear votaciones con multiples preguntas por POST
  * Enviar token de admin a Mixnet
  * Automatización de los tests y el despliegue
  * Arreglo de los tests de nuestro módulo
  * Creación de la MV
* Sánchez Montiel, José Luis:
  * Posibilidad de crear un referendum
  * Automamitazión de la creación del referendum
  * Introducción de nuevas vistas 
  * Inclusión y uso de la libreria Bootstrap
* Valero García, Luis:
  * Creación del UML para los nuevos cambios
  * Modificación e implementación del soporte de preguntas múltiples
  * Arreglo de tests

# Entorno de desarrollo

Todos los miembros del grupo hemos usado una máquina virtual con el sistema operativo Ubuntu 18.04, dicha máquina tiene instalado Pycharm Commnunity Edition, el cual hemos utilizado como IDE.

Como lenguaje será necesario Python 3.6.6, además de la instalación de Git, Docker, Heroku y Travis CI. Todo está inicialmente en la máquina virtual excepto Travis CI y Heroku, para instarlarlos habrá que usar los siguientes comando en terminal:

### Instalación de travis

```
sudo apt install ruby ruby-dev
sudo gem install travis
```

### Instalación de Heroku

```
sudo snap install --classic heroku
```

Cabe destacar que para los requisitos de python hemos usado el requirements.txt que hay en nuestro proyecto,
el cual PyCharm lo instalará automatáticamente si está en el directorio del proyecto y si no se puede instalar mediante el siguiente comando, ejecutado en el directorio donde se encuentre el fichero requirements.txt:

```
pip3 install -r requirements.txt
```
La máquina virtual que usamos cada miembro inicialmente puede ser descargada en el siguiente enlace: https://drive.google.com/open?id=1kw6veIZJ_dvcwXhGwNH3_YLgwEvvxtdW


# Gestión de incidencias

Hemos gestionado las incidencias a través de los issues de github. El formato definido para 
dichas incidencias es el ya utilizado por la mayoría de módulos, entre ellos nosotros, es: [Nombre del módulo que la crea] - Breve titulo descriptivo.
Por otro lado, en todos los módulos se ha acordado añadir como etiqueta al módulo al que va dirigido esa issue. La descripción deberá ser lo más
extensa posible, dando datos de manera concisa, como por ejemplo contener trazas de excepción y ser lo más explícito posible.

En nuestro módulo hemos considerado también otras características sobre los issues como: añadir etiquetas de la prioridad y el tipo
de incidencia que es (cambio, mejora, fallo...). Además habrá que asignar al desarrollador de nuestro módulo que se encarge de la resolución de dicha incidencia. 

Por último en nuestro módulo se creo un proyecto en github para controlar el estado de las incidencias,
tenemos dos estados: Working (incidencias en proceso de resolución) y DONE (incidencias resueltas).

En cuanto a las incidencias internas, simplemente se crean y se asignan al miembro del grupo que tuviera que encargarse de dicha parte,
para finalizar dicha incidencia hay dos opciones: 

1. Si se arregla mediante un commit, se deberá referenciar en el mismo a la incidencia, para que se cierre automáticamente o, al menos, para llevar
un histórico de los pasos que ha seguido esa incidencia.
1. En otro caso, si la issue no se arregla mediante un commit, o se debe añadir más información , aunque haya commits referenciados se deberá cerrar manualmente tras el comentario

Una vez cerrada se pasará a DONE en nuestro proyecto. La política de finalización de incidencias será igual para las incidencias externas. En cuanto a la creación de las externas
se acordó que una vez creada el issue se notificaría al manager de cada módulo para que se lo asignarán en dicho grupo. Además de los commits también se podrán
referenciar otros issues en caso de que uno dependa de otro. En caso de no realizar una incidencia se deberá de finalizar con la etiqueta "Wontfix" y explicar por qué no se ha realizado.

Algunos ejemplos de la resolución de incidencias son:

* Incidencia interna finalizada con un commit: https://github.com/pablotabares/decide/issues/103
* Incidencia interna referencia a otra incidencia: https://github.com/pablotabares/decide/issues/98
* Incidencia interna finalizada a mano: https://github.com/pablotabares/decide/issues/170
* Incidencia externa (para nuestro grupo) finalizada con un commit: https://github.com/pablotabares/decide/issues/149
* Creación de una incidencia externa (para otro grupo): https://github.com/pablotabares/decide/issues/77
* Issue que finalmente no se implementa: https://github.com/pablotabares/decide/issues/21

# Gestión de depuración

Para la gestión de depuración, una vez se encuentre una excepción, se deberá crear un issue y explicar en que situación se genera esa incidencia
y detallar, si se conoce, el motivo para que ocurra. Una vez creada se deberá investigar sobre el error, intentar aislarlo en código mediante la herramiena de depuración (Debug) 
de PyCharm y una vez se resuelva se deberá asociar el commit a la incidencia y explicar en el commit el motivo del error y cómo se ha solucionado, incluyendo la fuente en caso de haber consultado información externa.

Un ejemplo de depuración de código se puede ver en esta issue: https://github.com/pablotabares/decide/issues/100

# Gestión de liberaciones, despliegues y entregas

## Liberación:
El protocolo de liberación de cambios que hemos seguido consiste en:

- Alfa: Implementación de la funcionalidad asignada. Una vez realizada, se guardan los 
  cambios en el repositorio de desarrollo de nuestro módulo (github.com/pablo-tabares/decide-ortosia-develop)
- Beta: Una vez unificados todos los cambios en el repositorio de desarrollo, se ponen a prueba
  los cambios realizados con la herramienta Travis CI, con unos tests ya modificados para comprobar
  las nuevas implementaciones. Si los tests se completan de manera satisfactoria, se realiza un commit
  al repositorio master de nuestro módulo (github.com/pablotabares/ortosia-votacion-prepro)
- Versión estable: una vez está el contenido en nuestro repositorio master, se realiza un pull-request 
  al repositorio master en común con el resto de módulos (github.com/pablotabares/decide)
 
## Despliegue:
Como se menciona anteriormente, el despligue se realiza sobre la plataforma Heroku. Para que la aplicación se despligue de manera satisfactoria en dicha plataforma, deberá pasar los tests específicos para que queden registrados los cambios que se han realizado en el proyecto, dichos tests están autmoatizados con la herramienta Travis CI, explicada en el [Mapa de herramientas](#Mapa-de-herramientas). 

## Entregables:
Hemos considerado que los entregables eran los milestones, en nuestro caso, 3 milestones.
Tienen una nomenclatura interna en el equipo como Entregable MX, siendo X el número del milestone en cuestión. 
En cada milestone, se realizaba un control de seguimiento de los avances del módulo en cuestión y recibir
feedback, en forma de proposición de mejoras para el siguiente milestone. Hemos tratado de implementar las mejoras propuestas
como la creación de un label propio para los issues concernientes a nuestro módulo, como se ha explicado en la sección de [Gestión de incidencias](#Gestión-de-incidencias) o una estructura definida para los títulos de los issues, como se explicará en la sección de [Gestión del código fuente](#Gestión-del-código-fuente)

# Gestión del código fuente

El formato de los títulos de los commits es: [Verbo en Participio Pasado] + [Breve explicación de que se ha hecho]

Ejemplo: https://github.com/pablotabares/decide/commit/be0ce2cecbd8c6287a2ea55c44ea5efa9fd26b58

En cuanto a la descripción deberá ser concisa y dar tantos detalles como sean necsarios para entender qué se ha realizado en dicho commit.

Ejemplo: https://github.com/pablotabares/decide/commit/832e081c512950302cdf74040e80ba5b6d34750f

Los commits se harán en el momento que se haya avanzando una cantidad notoria o terminado una funcionalidad, siempre y cuando la versión sea estable y no provoque errores a priori en otras partes del proyecto.

En cuanto a la gestión del repositorio se han usado varías ramas (enlaces al principio del documento):

* Master: Es la rama principal del proyecto, sólo un alumno tenía acceso a esa rama
* Ortosia-Prepro: Es la rama de preproducción, para asegurarnos de que no hay ningún problema antes de subirlo a la rama master. También un solo alumno tiene permisos de escritura para esta rama
* Ortosia-Votacion: Es la rama "master" de nuestro módulo, tras un problema con un pull request dejó de usarse y se volvió a una versión anterior en la siguiente rama.
* Ortosia-Votacion-Prepro: Finalmente esta fue nuestra rama master y es donde se conservan los cambios aislados del módulo de votación.
* Ortosia-Votacion-Develop: La rama utilizada para el desarrollo de los cambios en el módulo de votación

Los merges a la rama master de nuestro módulo, es decir, Ortosia-Votacion-Prepro se harán cuando se posean versiones estables, una vez todos los cambios esten allí y se haya desplegado el sistema se harán pruebas para asegurarse que todo está correcto. Tras finalizar las pruebas, el manager de nuestro módulo será el encargado de hacer un pull request a Ortosia-Prepro; preparando debidamente la rama para no causar conflictos ni pisar archivos de configuración, como travis, requirements, settings...

Ejemplo: https://github.com/pablotabares/decide/pull/145

# Mapa de herramientas

IDE: 			PyCharm Community Edition
Control de versiones: 	Git
Repositorio: 		Github
Control de repositorio: Terminal 
Integración continua:	Travis CI
Despliegue: 		Heroku

Para el desarrollo del código, asi como el uso para el resto de herramientas mencionadas en la sección de [Entorno de Desarrollo](#Entorno-de-desarrollo),
utilizaremos el IDE PyCharm, centralizando el uso del resto de herramientas. Utilizaremos el Terminal que incluye PyCharm para hacer las pertinentes acciones relacionadas
con el repositorio alojado en Github. Una vez desarrollados los cambios en el IDE, para el control de los commits, se realizarán pruebas automatizadas, con el uso de la herramienta 
Travis CI, a la cual se le especificará la rutina a realizar para comprobar que no contiene ningún error, de acuerdo con los tests especificados. Si dicha comprobación es satisfactoria, 
Travis CI permite que la actualización se manifieste en el servicio de despliegue que utilizamos que hemos mencionado en la sección de [Despliegue](##Despliegue). 

# Ejercicio de propuesta de cambio

Añadir importancia a las questions:

Antes de comenzar a trabajar en cualquier aspecto relacionado con el proyeycto, en primer lugar, lo que debemos hacer es asegurarnos de que estamos en la rama pertinente a nuestro desarrollo, ortosia-votacion-develop con el comando:
```
git branch
```
Este comando nos devuelve las ramas, y la rama en la que nos encontamos.
Si no estamos en nuestra rama, ejecutamos:
```
git checkout ortosia-votacion-develop
```
A continuación, nos aseguramos de que tenemos nuestro repositorio actualizado, con el método:
```
git pull 
```
para así, evitar conflictos de concurrencia, al olvidarnos tener la rama actualizada.
Determinamos los cambios y clases en las que vamos a necesitar hacer modificaciones para las propuestas, que en este caso, son: models.py, para modificar nuestros modelos, views.py, para implementar la gestión del nuevo atributo, en este caso tenemos que modificar, el método createVoting, para la creación de una votación mediante el panel de administración, y el método votingView, para la gestión del mismo en las llamadas de nuestra API, al igual que modificar el la clase serializers.py para que correspondan con nuestros modelos y test.py para actualizar los tests, y añadir si fuera necesario, alguno nuevo.
Una vez identificados los cambios necesarios para su implementación, gestionamos primero lo necesario para su implementación por el panel de administración.
Modificamos el modelo, y realizamos los comandos:
```
python3 ./manage.py makemigrations
python3 ./manage.py migrate
```
Con estos dos, se modifica la base de datos conforme a los nuevos modelos
Realizamos los cambios necesarios en el view.
Tras esto, creamos los test pertinentes.
Cuando veamos que esta funcional, ejecutamos el servidor, y hacemos las pruebas con la aplicación desplegada en local.
```
python3 ./manage.py runserver
```
Si todo está correcto, y la funcionalidad responde de la manera esperada, modificamos las clases serializers.py para que estén conforme a los modelos, y el método VotingView, para que gestione el método de la API con la nueva funcionalidad.
Finalmente, realizamos los test.
Cuando todo esté completamente correcto, subimos los cambios a nuestro repositorio:
```
git add <nombre_de_archivo_cambiado>
git commit -m “Titulo del mensaje” -m “Cuerpo del mensaje”
git push
```

# Conclusiones y trabajo futuro

Hemos obtenido una base bastante completa de numerosas herramientas utilizadas en la actualidad, citadas en la sección de [Mapa de herramientas],(#Mapa-de-herramientas)
como Django para desarrollo de servicios web, Heroku para despliegue de las aplicaciones o Travis CI para desarrollar rutinas de control para la integración continua, 
además del enfoque al trabajo es útil ya que es una primera toma de contacto en el desarrollo de proyectos con un mayor número de grupos participantes para su desarrollo, 
lo que nos ha ayudado a mejorar en nuestras capacidades de comunicación con equipos externos a nuestro propio módulo, dándole una vista realista al proyecto en el que hemos trabajado.







