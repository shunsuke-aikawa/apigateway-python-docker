# ApiGateway -> Python3-lambda Dockerfile

build

```
docker-compose build
```

up

```
docker-compose up
```


execute

```
#GET
curl localhost/aaa?a=1

{
    "json-body": {},
    "method": "GET",
    "query-string": {
        "a": "1"
    },
    "url": "/aaa"
}


#POST
curl -H "Content-type: application/json" -X POST -d '{"a":1,"b":2}' localhost/aaa

{
    "json-body": {
        "a": "1",
        "b": "2"
    },
    "method": "POST",
    "query-string": {},
    "url": "/aaa"
}

```
