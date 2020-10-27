# HacktoberfestES 2020

This article is a review of the event [Python HacktoberfestES](https://hacktoberfest.es.python.org/)


# [2020-10-04] Presentación Hacktoberfest
- [vídeo inaugural](https://youtu.be/bRemmaI9M34?t=1289)
- [Presentación](https://github.com/avara1986/hacktoberfestES-pyms/blob/master/Microservicios%20v3.0%20Light.pdf)
  


# [2020-10-04] Presentación PyMS
Buenas! Con PyMS vamos a estudiar y aprender a construir microservicios para el mundo real: No solo una API que devuelve datos. ¿qué tiene que cumplir un microservicio para ser productivo? Configuración externalizada, healthchecks, trazabilidad... ¡y mucho más!

- Puedes ver la documentación en [este link](https://py-ms.readthedocs.io/en/latest/)
- [Ver el código fuente en Github](https://github.com/python-microservices/pyms) al igual que las issues abiertas (y las que se nos vayan ocurriendo)
- Puedes clonarte un [arquetipo de microservicio funcional](https://github.com/python-microservices/microservices-scaffold)
- O crearte el tuyo propio con [Cookiecutter](https://github.com/python-microservices/cookiecutter-pyms): 

# [2020-10-04] Hacktoberfest: primera reunión
De los que hemos participado juntamos un stack tecnológico muy interesante habiendo tocado no solo Python si no lenguajes como Java, .NET, Groovy, BASH, Ruby, además de tecnologías blockchain, sistemas e infrastructura, CI...

También hemos visto que PyMS, tanto la librería como el arquetipo "destacado" son sobre Flask pero puede incluir en un futuro otros frameworks como aiohttp o FastAPI. Pero además existe [este proyecto](https://github.com/python-microservices/microservices-django-scaffold)  para adaptar todas estas buenas prácticas sobre un proyecto de Django.

Planteamos, si a alguien no le atraen los microservicios como tal, poder crear una página web estática con la documentación, información y literatura sobre microservicios y quien sabe, hasta un posible blog con un generador de contenido estático como [Nikola](https://getnikola.com/) o alguno de [estos](https://wiki.python.org/moin/StaticSiteGenerator)  (pendiente de definir)

Como no todos tenemos el mismo nivel, hemos acordado empezar con unos tutoriales y formaciones en Python y el arquetipo para tener todos contexto y el fin de semana que viene hacer puesta en común y empezar a trabajar sobre issues de los proyectos.

Para poder colaborar, proponemos que cuando alguien esté mirando cosas del proyecto o dedicado a investigar, que avise por chat y si quiere, conectarse al chat de voz para resolver dudas y hacer pair-programming, presentar o charlar. Del mismo modo, si alguien quiere ver dudas que avise por chat "a tal hora me conecto"

## Recursos útiles para aprender Python:
- [7 Repositorios para aprender Python](https://towardsdatascience.com/top-7-repositories-on-github-to-learn-python-44a3a7accb44)

## Cursos, Posts y Podcasts
- [realpython.com](https://realpython.com/) - Python en general, cursos pago, posts gratis, muy claro. 
- [www.fullstackpython.com](https://www.fullstackpython.com/) - Posts de desarrollo fullstack, muchos enlaces a otros recursos.
- [training.talkpython.fm](https://training.talkpython.fm/) - Podcast gratis y cursos de pago, mucho de web en Flask.
- [www.pluralsight.com](https://www.pluralsight.com/) - De pago, muchos lenguajes, mucho testing, muchos perfiles (dev, sec, devops), buenos recursos video, examenes, portfolio de habilidades y roles.
- [ed.team](https://ed.team/) - Canal de youtube, cursos de pago, muchas tecnologías, en español.
- [codely.tv](https://codely.tv/) - Canal de youtube, cursos de pago (devops y arquitectura), algo de Golang pero nada de Python

## Katas
- [www.hackerrank.com](https://www.hackerrank.com/) muchos niveles, portfolio de habilidades, bolsa de trabajo.
- [exercism.io](https://exercism.io/) -  muchos lenguajes, basado en tests, editas offline y envias con terminal.
- [www.codewars.com](https://www.codewars.com/) - muchos lenguajes, plataforma de katas, con katas de usuario.
## Noticias
- [dev.to/t/python](https://dev.to/t/python) - Noticias y dudas.
- [www.reddit.com/r/Python](https://www.reddit.com/r/Python) - Noticias, dudas y nido de trolls.

## Aprender Jugando
- [www.codingame.com](https://www.codingame.com/) - Muchos lenguajes.
- [py.checkio.org](https://py.checkio.org/)
- [www.twilio.com/quest](https://www.twilio.com/quest) - Gracioso pero poco codigo.

## Relacionadas con PyMS:
- Forma más actual de hacer tests en python: [docs.pytest.org/en/stable](https://docs.pytest.org/en/stable/)
- Para complementar tus test, Tox: [tox.readthedocs.io/en/latest](https://tox.readthedocs.io/en/latest/)
- Pipenv como sustituto del típico virtualenv: [pipenv-es.readthedocs.io/es/latest](https://pipenv-es.readthedocs.io/es/latest/)
- Linter para verificar la sintaxis del código, Pylint: [pylint.readthedocs.io/en/latest/?badge=latest](https://pylint.readthedocs.io/en/latest/?badge=latest)
- También Flake8: [flake8.pycqa.org/en/latest](https://flake8.pycqa.org/en/latest/)
- "Tipado" en Python: [docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)
- "La biblia" de la arquitectura de microservicios: [microservices.io](https://microservices.io/)
- Trazabilidad distribuida con Python: [github.com/opentracing/opentracing-python](https://github.com/opentracing/opentracing-python)


# [2020-10-05] Formación, Python Básico:
[Ver repositorio](https://github.com/avara1986/hacktoberfestES-pyms/blob/master/python_101/Python%20%22b%C3%A1sico%22.ipynb)

# [2020-10-06] Formación, buenas prácticas:
[Ver repositorio](https://github.com/avara1986/hacktoberfestES-pyms/blob/master/python_best_practices/Python%20Best%20Practices.ipynb)

# [2020-10-08] Formación, Cómo funciona PyMS:
[Ver vídeo](https://youtu.be/i9msDUKA0Zk)

# [2020-10-08] Formación, Portainer, web-ui para manejar Docker:
[Ver vídeo](https://youtu.be/z-_DhL6wRFQ)

# [2020-10-09] Fin de sprint, reparto de tareas:
Se puede contribuir mediante Fork o avisadme y os añado como colaboradores para poder trabajar sobre el mismo repo. Lo que prefiráis!

- Para el flujo de ramas, ver [workflow para contribuir](https://guides.github.com/introduction/flow/)
- Para los mensajes de commit ver: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- Al igual que [Angular guideline](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)

## Tareas/issues repartidas:
* [ ] [PyMS Issue #166](https://github.com/python-microservices/pyms/issues/166) @BelenC y @AmandaKhol -> En esta pueden participar más de una persona
* [x] [PyMS Issue #89](https://github.com/python-microservices/pyms/issues/89) @Rapejim 
* [ ] [Microservices-scaffold Issue #213](https://github.com/python-microservices/microservices-scaffold/issues/213) @vmyelicich
* [ ] [PyMS Issue #178](https://github.com/python-microservices/pyms/issues/178) @kirk
* [ ] [Microservices-scaffold Issue #215](https://github.com/python-microservices/microservices-scaffold/issues/215) @felipem775 
* [x] [github.com/python-microservices/cookiecutter-pyms/issues/9](https://github.com/python-microservices/cookiecutter-pyms/issues/9) @AmandaKhol 
* [ ] [github.com/python-microservices/cookiecutter-pyms/issues/4](https://github.com/python-microservices/cookiecutter-pyms/issues/4) @PandyTheBroh

## Tareas/issues listas para asignar:
* [ ] [PyMS Issue #68](https://github.com/python-microservices/pyms/issues/68)
* [ ] [PyMS Issue #180](https://github.com/python-microservices/pyms/issues/180)
* [ ] [PyMS Issue #182](https://github.com/python-microservices/pyms/issues/182)
* [ ] [PyMS Issue #184](https://github.com/python-microservices/pyms/issues/184)
* [ ] [PyMS Issue #188](https://github.com/python-microservices/pyms/issues/188)
* [ ] [PyMS Issue #189](https://github.com/python-microservices/pyms/issues/189)
* [ ] [PyMS Issue #185](https://github.com/python-microservices/pyms/issues/185) (HARD)
* [ ] [PyMS Issue #156](https://github.com/python-microservices/pyms/issues/156) (HARD)
* [ ] [PyMS Issue #186](https://github.com/python-microservices/pyms/issues/186) (HARD)
* [ ] [PyMS Issue #190](https://github.com/python-microservices/pyms/issues/190) (HARD)

## Investigación:
- Access token:
    - Investigar [microservices.io/patterns/security/access-token.html](https://microservices.io/patterns/security/access-token.html)
    - Actualizar el [repositorio de ejemplo](https://github.com/python-microservices/oauth) con lo último de PyMS
    - Mejorar y hacer de manera genérica la implementación de JWT
- Saga:
    - Investigar [microservices.io/patterns/data/saga.html](https://microservices.io/patterns/data/saga.html)
    - Crear un arquetipo parecido al [que ya existe](https://github.com/python-microservices/microservices-scaffold) que haga este patrón
- Circuit Breaker:
    - Investigar [microservices.io/patterns/reliability/circuit-breaker.html]()
    - Llevar a PyMS, si es posible, ese patrón para que se pueda usar en todos los microservicios (por ejemplo, como hace https://micronaut.io/)

- gRCP ([protocol buffers](https://grpc.io/docs/what-is-grpc/introduction/)):
    - Una forma alternativa a API Rest para comunicar microservicios es [mediante gRCP](https://grpc.io/docs/languages/python/quickstart/)
    - Crear un arquetipo parecido al [que ya existe](https://github.com/python-microservices/microservices-scaffold) que se comunique con otro mediante gRCP
    - Llevar a PyMS, si es posible, este framework

## Retos:
- Publisher-subscriber: [github.com/python-microservices/pyms/issues/155]()
    - Crear un script que escuche y escriba en una cola infinitamente
    - Evolucionar el servicio para que en un futuro se puedan ir añadiendo diferentes servicios (SQS, Kafka, Pub/sub, RabbitMQ...)
    - Meter este servicio en un subproceso/thread para que se pueda integrar con PyMS
    - Añadir endpoints para consultar información de la cola


## Consejos y acuerdos:
- Hay que visitar Valparaíso (Chile)
- Es necesario visitar la isla de La Palma al menos una vez en la vida
- Cuidado al pedir pizza a domicilio

# [2020-10-10] Debate sobre issue #89:
[Ver vídeo](https://youtu.be/cDR10YSnb0M)

# [2020-10-11] Resumen de la primera semana:
[Ver vídeo](https://youtu.be/WU-IAGConjU)

# [2020-10-11] Git workflow y testing:

*TODO: falta link*

# [2020-10-16] Fin de sprint, reparto de tareas:
Dejamos asignadas tareas para todo el mundo para hacer el reto de hacktoberfest y que de aquí a 2
semanas nadie nos quite alguna tarea que teníamos pensada

## Tareas/issues repartidas:
* [ ] [PyMS Issue #189](https://github.com/python-microservices/pyms/issues/189) @AmandaKhol
* [ ] [PyMS Issue #196](https://github.com/python-microservices/pyms/issues/196) @PandyTheBroh
* [ ] [PyMS Issue #164](https://github.com/python-microservices/pyms/issues/164) @Rapejim
* [ ] [PyMS Issue #180](https://github.com/python-microservices/pyms/issues/180) @mbcaldeiro
* [ ] [Microservices-scaffold Issue #219](https://github.com/python-microservices/microservices-scaffold/issues/194) @mbcaldeiro
* [ ] [PyMS Issue #184](https://github.com/python-microservices/pyms/issues/184) @vmyelicich
* [ ] [Microservices-scaffold Issue #220](https://github.com/python-microservices/microservices-scaffold/issues/220) @PandyTheBroh
* [ ] [PyMS Issue #197](https://github.com/python-microservices/pyms/issues/197) @PandyTheBroh

## Tareas/issues listas para asignar:
* [ ] [Microservices-scaffold Issue #219](https://github.com/python-microservices/microservices-scaffold/issues/219)  ¿@felipem775?
* [ ] [Microservices-scaffold Issue #218](https://github.com/python-microservices/microservices-scaffold/issues/218)  ¿@felipem775?
* [ ] [PyMS Issue #195](https://github.com/python-microservices/pyms/issues/195)
* [ ] [PyMS Issue #188](https://github.com/python-microservices/pyms/issues/188)
* [ ] [PyMS Issue #68](https://github.com/python-microservices/pyms/issues/68)
* [ ] [PyMS Issue #182](https://github.com/python-microservices/pyms/issues/182)
* [ ] [PyMS Issue #199](https://github.com/python-microservices/pyms/issues/199)