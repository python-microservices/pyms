# Encrypt Configuration

## Configuration

# Method 1: Encrypt and decrypt with key file and Fernet


When you work in multiple environments: local, dev, testing, production... you must set critical configuration in your
variables, such as:

config.yml, for local propose:
```yaml
pyms:
  config:
    DEBUG: true
    TESTING: true
    APPLICATION_ROOT : ""
    SECRET_KEY: "gjr39dkjn344_!67#"
    SQLALCHEMY_DATABASE_URI: mysql+mysqlconnector://user_of_db:user_of_db@localhost/my_schema
```

config_pro.yml, for production environment:
```yaml
pyms:
  config:
    DEBUG: true
    TESTING: true
    APPLICATION_ROOT : ""
    SECRET_KEY: "gjr39dkjn344_!67#"
    SQLALCHEMY_DATABASE_URI: mysql+mysqlconnector://important_user:****@localhost/my_schema
```

You can move this file to a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/), 
use [Vault](https://learn.hashicorp.com/vault) or encrypt the configuration with [AWS KMS](https://aws.amazon.com/en/kms/)
 or [Google KMS](https://cloud.google.com/kms). We strongly recommend these way of encrypting/decrypting your configuration,
 but if you don't want a vendor locking option or you don't have the resources to use these methods, we provide a way to encrypt
 and decrypt your variables.
 
## 1. Generate a key
PyMS has a command line option to create a key file. This key is created with [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard).
You can run the next command in the terminal:

```bash
pyms create-key
```

Then, type a password and it will create a file called `key.key`. This file contains a unique key. If you loose this file
and re-run the create command, the key hash will be different and your code encrypted with this key won't be able to be decrypted.

Store this key in a secure site, and DO NOT COMMIT it to your repository.


## 2. Add your key to your environment

Move your key, for example, to `mv key.key /home/my_user/keys/myproject.key`

then, store the key in a environment variable with:

```bash
export PYMS_KEY_FILE=/home/my_user/keys/myproject.key
```

## 3. Encrypt your information and store it in config

Do you remember the example file `config_pro.yml`? Now you can encrypt and decrypt the information, you can run the command
`pyms encrypt [string]` to generate a crypt string, for example:

```bash
pyms encrypt 'mysql+mysqlconnector://important_user:****@localhost/my_schema'
>>  Encrypted OK: b'gAAAAABeSwBJv43hnGAWZOY50QjBX6uGLxUb3Q6fcUhMxKspIVIco8qwwZvxRg930uRlsd47isroXzkdRRnb4-x2dsQMp0dln8Pm2ySHH7TryLbQYEFbSh8RQK7zor-hX6gB-JY3uQD3IMtiVKx9AF95D6U4ydT-OA=='
```

And store this string in your `config_pro.yml`:
```yaml
pyms:
  crypt:
    method: "fernet"
  config:
    DEBUG: true
    TESTING: true
    APPLICATION_ROOT : ""
    SECRET_KEY: "gjr39dkjn344_!67#"
    ENC_SQLALCHEMY_DATABASE_URI: gAAAAABeSwBJv43hnGAWZOY50QjBX6uGLxUb3Q6fcUhMxKspIVIco8qwwZvxRg930uRlsd47isroXzkdRRnb4-x2dsQMp0dln8Pm2ySHH7TryLbQYEFbSh8RQK7zor-hX6gB-JY3uQD3IMtiVKx9AF95D6U4ydT-OA==
```

Do you see the difference between `ENC_SQLALCHEMY_DATABASE_URI` and `SQLALCHEMY_DATABASE_URI`? In the next step you
can find the answer

## 4. Decrypt from your config file

Pyms knows if a variable is encrypted if this var start with the prefix `enc_` or `ENC_`. PyMS searches for your key file
in the `PYMS_KEY_FILE` env variable and decrypts this value to store it in the same variable without the `enc_` prefix, 
for example, 

```yaml
ENC_SQLALCHEMY_DATABASE_URI: gAAAAABeSwBJv43hnGAWZOY50QjBX6uGLxUb3Q6fcUhMxKspIVIco8qwwZvxRg930uRlsd47isroXzkdRRnb4-x2dsQMp0dln8Pm2ySHH7TryLbQYEFbSh8RQK7zor-hX6gB-JY3uQD3IMtiVKx9AF95D6U4ydT-OA==
```

Will be stored as 

```bash
SQLALCHEMY_DATABASE_URI: mysql+mysqlconnector://user_of_db:user_of_db@localhost/my_schema
```

And you can access this var with `current_app.config["SQLALCHEMY_DATABASE_URI"]`

# Method 2: Encrypt and decrypt with AWS KMS

## 1. Configure AWS

Pyms knows if a variable is encrypted if this var start with the prefix `enc_` or `ENC_`. PyMS uses boto3 and
aws cli to decrypt this value and store it in the same variable without the `enc_` prefix.

First, configure aws your aws account credentials:

```bash
aws configure
```

## 2. Encrypt with KMS

Cypher a string with this command:

```bash
aws kms encrypt --key-id alias/prueba-avara --plaintext "mysql+mysqlconnector://important_user:****@localhost/my_schema" --query CiphertextBlob --output text
>>  AQICAHiALhLQv4eW8jqUccFSnkyDkBAWLAm97Lr2qmdItkUCIAF+P4u/uqzu8KRT74PsnQXhAAAAoDCBnQYJKoZIhvcNAQcGoIGPMIGMAgEAMIGGBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDPo+k3ZxoI9XVKtHgQIBEIBZmp7UUVjNWd6qKrLVK8oBNczY0CfLH6iAZE3UK5Ofs4+nZFi0PL3SEW8M15VgTpQoC/b0YxDPHjF0V6NHUJcWirSAqKkP5Sz5eSTk91FTuiwDpvYQ2q9aY6w=

```

## 3. Decrypt from your config file

And put this string in your `config_pro.yml`:
```yaml
pyms:
  crypt:
    method: "aws_kms"
    key_id: "alias/your-kms-key"
  config:
    DEBUG: true
    TESTING: true
    APPLICATION_ROOT : ""
    SECRET_KEY: "gjr39dkjn344_!67#"
    ENC_SQLALCHEMY_DATABASE_URI: "AQICAHiALhLQv4eW8jqUccFSnkyDkBAWLAm97Lr2qmdItkUCIAF+P4u/uqzu8KRT74PsnQXhAAAAoDCBnQYJKoZIhvcNAQcGoIGPMIGMAgEAMIGGBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDPo+k3ZxoI9XVKtHgQIBEIBZmp7UUVjNWd6qKrLVK8oBNczY0CfLH6iAZE3UK5Ofs4+nZFi0PL3SEW8M15VgTpQoC/b0YxDPHjF0V6NHUJcWirSAqKkP5Sz5eSTk91FTuiwDpvYQ2q9aY6w=
"
```
