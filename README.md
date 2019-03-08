[![Docker](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/docker.png)](https://cloud.docker.com/u/gpulidodt/repository/docker/gpulidodt/swarm-alert)

# Introduction
The SwarmAlert app monitors the availability of services running in a Docker Swarm. It currently monitors only those services specified in the WHITE_LIST ENV variable, making this a required parameter. If a specified service has no running task, the app generates a Pushover Notification using the specified Token, App Key, and MSG_PREFIX.

Note: This project is based on [monitor-docker-slack](https://github.com/DennyZhang/monitor-docker-slack)

# General Idea
1. Start one or more services in Docker Swarm mode.
2. Use this service to monitor the availability of services.
3. Send a pushover notifications containeing the unavailable services.

# How To Use: Docker-compose
```
version: '3'
services:
  swarm-alert:
    image: gpulidodt/swarm-alert:latest
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
    environment:
     - PUSHOVER_USER_KEY: "user_key_from_pushover"
     - PUSHOVER_API_TOKEN: "your_app_token_from_pushover"
     - MSG_PREFIX: "$MSG_PREFIX"
     - WHITE_LIST="traefik_traefik,plex_plex,etc."
     - BLACK_LIST="shepherd_shepherd"
```

# Further customization
- Customize the message prefix for the Pushover Notification via the MSG_PREFIG variable:
```
 - MSG_PREFIX="Swarm services"
```
 - If defined, the services that are monitored are those on the WHITE_LISTE_LIST variable:
```
 - WHITE_LIST="nodeexporter,ngin.*"
```
 - If defined, the services defined on the BLACK_LIST are excluded from monitoring:
```
 - BLACK_LIST="nodeexporter,ngin.*"
```

Code is licensed under MIT license
