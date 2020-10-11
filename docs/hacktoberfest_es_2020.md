# HacktoberfestES 2020

This article is a review of the event [Python HacktoberfestES](https://hacktoberfest.es.python.org/)


# [2020-10-04] Presentación Hacktoberfest
- vídeo inaugural:
  https://youtu.be/bRemmaI9M34?t=1289
- Presentación:
  https://github.com/avara1986/hacktoberfestES-pyms/blob/master/Microservicios%20v3.0%20Light.pdf


# [2020-10-04] Presentación PyMS

Buenas! Con PyMS vamos a estudiar y aprender a construir microservicios para el mundo real: No solo una API que devuelve datos. ¿qué tiene que cumplir un microservicio para ser productivo? Configuración externalizada, healthchecks, trazabilidad... ¡y mucho más!

- Puedes ver la documentación en: https://py-ms.readthedocs.io/en/latest/
- Ver el código fuente en Github al igual que las issues abiertas (y las que se nos vayan ocurriendo): https://github.com/python-microservices/pyms
- Puedes clonarte un arquetipo de microservicio funcional en: https://github.com/python-microservices/microservices-scaffold
- O crearte el tuyo propio con Cookiecutter: https://github.com/python-microservices/cookiecutter-pyms

# [2020-10-04] Hacktoberfest: primera reunión

De los que hemos participado juntamos un stack tecnológico muy interesante habiendo tocado no solo Python si no lenguajes como Java, .NET, Groovy, BASH, Ruby, además de tecnologías blockchain, sistemas e infrastructura, CI...

También hemos visto que PyMS, tanto la librería como el arquetipo "destacado" son sobre Flask pero puede incluir en un futuro otros frameworks como aiohttp o FastAPI. Pero además existe este proyecto https://github.com/python-microservices/microservices-django-scaffold para adaptar todas estas buenas prácticas sobre un proyecto de Django.

Planteamos, si a alguien no le atraen los microservicios como tal, poder crear una página web estática con la documentación, información y literatura sobre microservicios y quien sabe, hasta un posible blog con un generador de contenido estático como https://getnikola.com/ o alguno de estos https://wiki.python.org/moin/StaticSiteGenerator (pendiente de definir)

Como no todos tenemos el mismo nivel, hemos acordado empezar con unos tutoriales y formaciones en Python y el arquetipo para tener todos contexto y el fin de semana que viene hacer puesta en común y empezar a trabajar sobre issues de los proyectos.

Para poder colaborar, proponemos que cuando alguien esté mirando cosas del proyecto o dedicado a investigar, que avise por chat y si quiere, conectarse al chat de voz para resolver dudas y hacer pair-programming, presentar o charlar. Del mismo modo, si alguien quiere ver dudas que avise por chat "a tal hora me conecto"


# [2020-10-05] Formación, Python Básico:

https://github.com/avara1986/hacktoberfestES-pyms/blob/master/python_101/Python%20%22b%C3%A1sico%22.ipynb

# [2020-10-06] Formación, buenas prácticas:

https://github.com/avara1986/hacktoberfestES-pyms/blob/master/python_best_practices/Python%20Best%20Practices.ipynb

# [2020-10-08] Formación, Cómo funciona PyMS:

***TODO: añadir link***

# [2020-10-09] Fin de sprint, reparto de tareas:
Se puede contribuir mediante Fork o avisadme y os añado como colaboradores para poder trabajar sobre el mismo repo. Lo que prefiráis!

workflow para contribuir:
https://guides.github.com/introduction/flow/

## Tareas/issues repartidas:
https://github.com/python-microservices/pyms/issues/166 @BelenC -> En esta pueden participar más de una persona
https://github.com/python-microservices/pyms/issues/89 @Rapejim (Raúl)
https://github.com/python-microservices/microservices-scaffold/issues/213 @vmyelicich (Víctor)
https://github.com/python-microservices/pyms/issues/178 @kirk
https://github.com/python-microservices/microservices-scaffold/issues @felipem775 
https://github.com/python-microservices/cookiecutter-pyms/issues/9 @AmandaKhol
https://github.com/python-microservices/cookiecutter-pyms/issues/4 @PandyTheBroh

## Tareas/issues listas para asignar:
https://github.com/python-microservices/pyms/issues/68
https://github.com/python-microservices/pyms/issues/180
https://github.com/python-microservices/pyms/issues/182
https://github.com/python-microservices/pyms/issues/184
https://github.com/python-microservices/pyms/issues/185 (HARD)
https://github.com/python-microservices/pyms/issues/156 (HARD)
https://github.com/python-microservices/pyms/issues/186 (HARD)

## Investigación:
- Access token:
    - Investigar https://microservices.io/patterns/security/access-token.html
    - Actualizar el proyecto de ejemplo https://github.com/python-microservices/oauth con lo último de PyMS
    - Mejorar y hacer de manera genérica la implementación de JWT
- Saga:
    - Investigar https://microservices.io/patterns/data/saga.html
    - Crear un arquetipo parecido al [que ya existe](https://github.com/python-microservices/microservices-scaffold) que haga este patrón
- Circuit Breaker:
    - Investigar https://microservices.io/patterns/reliability/circuit-breaker.html
    - Llevar a PyMS, si es posible, ese patrón para que se pueda usar en todos los microservicios (por ejemplo, como hace https://micronaut.io/)

- gRCP ([protocol buffers](https://grpc.io/docs/what-is-grpc/introduction/)):
    - Una forma alternativa a API Rest para comunicar microservicios es [mediante gRCP](https://grpc.io/docs/languages/python/quickstart/)
    - Crear un arquetipo parecido al [que ya existe](https://github.com/python-microservices/microservices-scaffold) que se comunique con otro mediante gRCP
    - Llevar a PyMS, si es posible, este framework

## Retos:
- Publisher-subscriber: https://github.com/python-microservices/pyms/issues/155
    - Crear un script que escuche y escriba en una cola infinitamente
    - Evolucionar el servicio para que en un futuro se puedan ir añadiendo diferentes servicios (SQS, Kafka, Pub/sub, RabbitMQ...)
    - Meter este servicio en un subproceso/thread para que se pueda integrar con PyMS
    - Añadir endpoints para consultar información de la cola


## Consejos y acuerdos:
- Hay que visitar Valparaíso (Chile)
- Es necesario visitar la isla de La Palma al menos una vez en la vida
- Cuidado al pedir pizza a domicilio