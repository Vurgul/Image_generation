# Project Emoticon
### Description
A FastAPI web server that generates emoticons for an arbitrary text string.
Emoticon - auto-generated avatar.

#### Implementation principle
1) We pass the text of the request via the API, the picture is returned
2) The generation of avatars must be implemented by a separate service:
https://github.com/amouat/dnmonster & https://hub.docker.com/r/amouat/dnmonster
3) Access to the API through authorization with a login and password
4) Access to the image generation API only through a token
5) Implemented image caching
6) All web services support docker & docker compose
7) Configured nginx to access the service

### Core technologies
* FastAPI
* Redis
* Docker
* Nginx
### Installation
1. Clone repository

2. Create environment variables
3. From the project directory, run the command below to create the images and the docker container:
```
docker-compose up
``` 

### Examples
After starting the project, documentation and examples can be viewed at: 
http://127.0.0.1:8888/redoc/
### Author
Vurgul: https://github.com/Vurgul