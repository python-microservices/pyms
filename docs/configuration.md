# Configuration

Each microservice needs a config file in yaml or json format to work with it. This configuration contain
the Flask configuration of your project and the [Services](services.md).

a simple configuration file could be a config.yaml:

```yaml
pyms:
  requests: true
  swagger:
    path: ""
    file: "swagger.yaml"
my-ms:
  DEBUG: true
  TESTING: false
  APP_NAME: "Python Microservice"
  APPLICATION_ROOT: ""
```

or in a config.json:

```json
{
"pyms":{
  "requests": true,
  "swagger": {
    "path": "",
    "file": "swagger.yaml"
    }
  },
"my-ms": {
  "DEBUG": true,
  "TESTIN": false,
  "APP_NAME": "Python Microservice",
  "APPLICATION_ROOT": ""
  }
}
```