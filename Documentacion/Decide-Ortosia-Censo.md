# Decide-Ortosia-Censo
##### Grupo 1
##### Id de opera: 141

### Miembros del grupo:
* Aguilera Moreno, Estrella: 4
* Fernández Montero, Francisco Javier: 4
* Herrera Ávila, Manuel: 5
* Narváez Sierra, Pablo: 3

### Enlaces de interés:
*   [Rama de ortosia-censo](https://github.com/pablotabares/decide/tree/ortosia-censo)
*   [Subsistema desplegado](https://decide-ortosia-censo.herokuapp.com/census/list)
*   [Diario del grupo](#)

---
## Índice

* [Resumen](#Resumen)
* [Introducción y contexto](#Introducción-y-contexto)
* [Descripción del sistema](#Descripción-del-sistema)
* [Planificación del proyecto](#Planificación-del-proyecto)
* [Entorno de desarrollo](#Entorno-de-desarrollo)
* [Gestión de incidencias](#Gestión-de-incidencias)
* [Gestión del código fuente](#Gestión-del-código-fuente)
* [Gestión de la construcción](#Gestión-de-la-construcción-e-integración-continua)
* [Gestión de liberaciones, despliegue y entregas](#Gestión-de-liberaciones,-despliegue-y-entregas)
    * [Liberaciones](#Liberaciones)
    * [Despliegue](#Despliegue)
    * [Entregas](#Entregas)
* [Mapa de herramientas](#Mapa-de-herramientas)
* [Ejercicio de propuesta de cambio](#Ejercicio-de-propuesta-de-cambio)
* [Conclusiones y trabajo futuro](#Conclusiones-y-trabajo-futuro)
* [Bibliografía](#Bibliografía)

---
## Resumen
En el presente proyecto se ha tratado la necesidad de tener un panel de administración del censo donde comprobar el correcto funcionamiento, donde se puede filtrar y ordenar los resultados para facilitar su lectura, la importación de información desde un directorio LDAP externo para simplificar la tarea de añadir votantes a una votación y la funcionalidad para reutilizar los datos de los votantes de una votación en otra evitando la tarea de introducir información ya existente

---
## Introducción y contexto
Nos encontramos ante una aplicación online de voto electrónico que necesita mejoras para incrementar su usabilidad y su facilidad de utilización puesto que la forma previa de autorizar a usuarios a votar era mediante llamadas a la API enviando manualmente la información sobre los usuarios y las votaciones.

Con la importación desde LDAP se pretende facilitar la inclusión de dichos datos ya que bastará con introducir la URL, los credenciales de acceso y el "Base DN", el identificador del grupo de personas que se quiere añadir a la aplicación, reduciendo en gran medida el tiempo y el esfuerzo necesario. Por otro lado ofreciendo la opción de compartir los datos de censos de dos votaciones también ayudara a reducir el esfuerzo a la hora de crear nuevas votaciones.

Por último el añadir un panel de control y listados permitirá por una parte tener una interfaz gráfica sencilla y amigable con la que realizar las funciones previamente comentadas y por otro de un sólo vistazo comprobar el correcto funcionamiento tanto de las funciones anteriores como el normal comportamiento del censo.

---
## Descripción del sistema
La aplicación Decide nos permite crear votaciones y que los votantes puedan emitir sus votos de forma online y segura. El sistema está compuesto de 9 módulos:
* Base: Módulo base sobre el que se desarrollan el resto
* Autentificación: Se encarga del registro de los usuarios en la aplicación
* Censo: Junto a los módulos Autentificación y Votación establece quién puede votar
* Votación: Establece el formato de las votaciones y permite su ejecución
* Cabina: Permite al votante emitir su voto
* Mixnet: Se encarga de desligar un voto de la persona que lo ha realizado, de modo que no se pueda rastrear su autoría
* Post-producción: Realiza el recuento tras finalizar la votación
* Visualización: Presenta los resultados obtenidos en la votación

Para nuestro proyecto en concreto (Censo), ademas de los especificados en la sección [Planificación-del-proyecto](#Planificación-del-proyecto), se han desarrollado los siguientes cambios:

* Llamada a la API para dado un usuario obtener las votaciones donde puede votar
* Paginado en las listas

---
## Planificación del proyecto:
En nuestro proyecto cada integrante se ha encargado de un incremento funcional por sí solo. Nos hemos ayudado en algunos momentos, pero las partes han sido individuales. Las tareas iniciales han sido    : 
* [Importación y exportación desde LDAP](https://github.com/pablotabares/decide/issues/115)
* [Front-end para visualizar el censo](https://github.com/pablotabares/decide/issues/112)
* [Una serie de filtros de los componentes de su modelo](https://github.com/pablotabares/decide/issues/114) (los filtros citados anteriormente se han basado en el modelo de Voting porque User no estaba ampliado cuando se realizaron)
* [Duplicado de los votantes registrados en una votación para autorizarlos en otra](https://github.com/pablotabares/decide/issues/113) 

Además se ha realizado un paginado de las vistas de Voting. 

---
## Entorno de desarrollo 
Se ha usado [Visual Code Studio](https://code.visualstudio.com/), en concreto la versión 1.30.1 como IDE. 
Para ejecutar el proyecto es necesario tener instalado Python en su versión 3.6 y Django en su versión 2.0.0.
Una vez instaladas las herramientas anteriores se debe seguir el proceso detallado en el [documento principal del proyecto](https://github.com/pablotabares/decide/blob/master/README.md)

---
## Gestión de incidencias y depuración
A la hora de resolver errores y depurarlos hemos usado los issues de Github. En concreto hemos diferenciado dos tipos de incidencias:
* Incidencias internas:
En las que se ha asignado directamente el issue al miembro del grupo correspondiente
* Incidencias externas:
Se reune más información sobre la incidencia y tras consultarlo con el grupo se asigna a uno u otro.

Un ejemplo del formato de los issues es [este](https://github.com/pablotabares/decide/issues/111)

---
## Gestión del código fuente
La gestión del código fuente del proyecto se hace a través de Git. Los commits tendrán la estructura definida en el siguiente [documento](https://github.com/pablotabares/decide/blob/ortosia-auth-documentation/decide/authentication/documentation/main.pdf). Pues se acordó entre los grupos que forman Ortosia usar dicho documento para todos.
Como se ve en este [commit](https://github.com/pablotabares/decide/commit/cf7106cdb502d9afdea0926fa11133744baf5975).

---
## Gestión de la construcción e integración continua
Se ha usado [Travis](https://travis-ci.com/) como herramienta para gestionar la integración continua, que nos permite automatizarla de modo que al detectar que se ha realizado un nuevo commit en Github se compile el código y se ejecuten los tests. Además nos permite el despliegue automático en otras herramientas.

---
## Gestión de liberaciones, despliegue y entregas

### Liberaciones:
No hemos realizado ninguna pues consideramos que el proyecto no ha estado terminado hasta la entrega final.

### Despliegue:
Para el despliegue del sistema se ha utilizado [Heroku](https://www.heroku.com/). Que nos proporciona un entorno de despliegue multilenguaje y con la posibilidad de añadir plugins como la base de datos Postgresql que usamos en el proyecto. El proceso de despligue ha sido el siguiente:
1. Se realiza un commit con los cambios que se añadan y se quiera desplegar.
2. Travis automáticamente envía una señal a Heroku para que compile el proyecto y lo despliegue.

### Entregas:
Las entregas se realizan subiendo el código al repositorio.

---
## Mapa de herramientas
![Mapa de herramientas](/Documentacion/images/tools_map.jpg)
Visual Code Studio es nuestro IDE, como se puntualiza en el apartado [Entorno de desarrollo](#Entorno-de-desarrollo). Una vez hemos realizado los cambios pertinentes en el código hemos seguido dos sistemas: o bien hecho commit y push directamente desde el apartado de Visual Code Studio o por medio de la consola en la carpeta raíz del proyecto. Al realizar el push, Travis monta el proyecto en un entorno virtual y ejecuta las pruebas para ver que el código esté en óptimas condiciones. Si no da error, Travis se conecta con heroku y juntos se encargan de desplegar el. Una vez está desplegado, es accesible para su utilización por medio de un link que Heroku proporciona.

---
## Ejercicio de propuesta de cambio
Se propone añadir paginación a la lista de usuarios. Para ello una vez instalado el entorno de desarrollo tal como se describe en el apartado [Entorno de desarrollo](#Entorno-de-desarrollo), en una consola de comando escribir lo siguiente para descargar el proyecto:
`git clone https://github.com/pablotabares/decide.git`
Esto creará una carpeta llamada decide con el proyecto dentro. Para usar nuestra rama hay que ejecutar los siguientes comando en la consola:
`git checkout -b ortosia-censo`
`git pull origin ortosia-censo`
Con ello ya tendremos nuestra rama preparada para trabajar, entonces hay que ir al archivo "/decide/census/templates/user_list.html" y añadir dentro del "div" con clase "container" el siguiente código:
```
<ul class="pager">
            <li>
                {% if page_obj.has_previous %}
                <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
                {% endif %}
            </li>
            <li>
                {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">Next</a>
                {% endif %}
            </li>
        </ul>
```
Tras eso ir al archivo "/decide/census/views.py" y en la clase "UserListView" añadir el parámetro "paginate_by" dándole un valor numérico que corresponderá al nº de objetos que se mostrará en cada página.

Una vez realizados los cambios en el código se realiza un commit escribiendo los siguientes comandos en la consola de comandos, estando abierto en ella el directorio donde se localice el proyecto:
`git add decide/census/templates/user_list.html`
`git add decide/census/views.py`
`git commit -m "{msg}"`
Siendo {msg} el mensaje que se mostrará en el commit
`git push origin ortosia-censo`
Con este comando los cambios serán enviados a Github. En el momento en que Github recibe un nuevo commit, Travis lo detecta y compila el proyecto para testearlo, si Travis da el visto bueno hará que Heroku lo despliegue, y si todo es correcto tendremos nuestra aplicación desplegada con el nuevo cambio.

---
## Conclusiones y trabajo futuro
Como mejoras de cara a una futura utilización del proyecto sería útil añadir mas documentación sobre la aplicación heredada y en concreto de la función de los campos de la base de datos, además de su refactorización ya que a primera vista no hay relación entre los votantes registrados en una votación y los usuarios del sistema. Si en lugar de un id se almacenase una referencia directa al objeto "User" ahorraría tener que hacer dos consultas para obtener primero el id en el censo y luego el usuario, al igual que con las votaciones.

---
## Bibliografía:
Se han usado como referencia o guía los siguientes documentos:
*   [Documentación de Django](https://docs.djangoproject.com/en/2.1/)
*   [Documentación del proyecto Decide](https://1984.lsi.us.es/wiki-egc/images/egc/6/6e/00-Decide1718.pdf)
*   [Documentación de Bootstrap para el CSS](https://getbootstrap.com/docs/4.2/getting-started/introduction/)
*   [Snippets de código basado en Bootstrap](https://bootsnipp.com/)
*   [Video sobre la paginación en Django](https://www.youtube.com/watch?v=ZvCw1jcXe4c)
*   [Documentación sobre el despliegue en Heroku de Travis](https://docs.travis-ci.com/user/deployment/heroku/)
