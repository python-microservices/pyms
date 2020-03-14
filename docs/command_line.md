# Commnand line

PyMS has some command to make easy your developments:

```bash
pyms -h
```
Show you a list of options and help instructions to use this command like:

```bash
usage: main.py [-h] [-v VERBOSE] {encrypt,create-key,startproject} ...

Python Microservices

optional arguments:
  -h, --help            show this help message and exit
  -v VERBOSE, --verbose VERBOSE
                        Verbose

Commands:
  Available commands

  {encrypt,create-key,startproject}
    encrypt             Encrypt a string
    create-key          Generate a Key to encrypt strings in config
    startproject        Generate a project from https://github.com/python-
                        microservices/microservices-template

```

## Start a project

Command:
```bash
pyms startproject
```

This command create a project template like [Microservices Scaffold](https://github.com/python-microservices/microservices-scaffold).
This command use [cookiecutter](https://github.com/cookiecutter/cookiecutter) to download and install this [template](https://github.com/python-microservices/microservices-template)

!!! warning
    You must run first `pip install cookiecutter==1.7.0`

## Create a key encrypt/decrypt file

Command: 
```bash
pyms create-key
```

Create a key file to encrypt strings in your configuration file. This key is created with [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard).
You can run the next command in the terminal. See [Encrypt/Decrypt Configuration](encrypt_decryt_configuration.md)
for more information

## Encrypt a string

Command: 
```bash
pyms encrypt [string] 
```

Encrypt a string to use in your [configfile](configuration.md)

```bash
pyms encrypt 'mysql+mysqlconnector://important_user:****@localhost/my_schema'
>>  Encrypted OK: b'gAAAAABeSwBJv43hnGAWZOY50QjBX6uGLxUb3Q6fcUhMxKspIVIco8qwwZvxRg930uRlsd47isroXzkdRRnb4-x2dsQMp0dln8Pm2ySHH7TryLbQYEFbSh8RQK7zor-hX6gB-JY3uQD3IMtiVKx9AF95D6U4ydT-OA=='
```

See [Encrypt/Decrypt Configuration](encrypt_decryt_configuration.md) for more information
