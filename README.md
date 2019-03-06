# Introduction
The SwarmAlert app monitors the availability of services running in a Docker Swarm. It currently monitors only those services specified in the WHITE_LIST ENV variable, making this a required parameter. If a specified service has no running task, the app generates a Pushover Notification using the specified Token, App Key, and MSG_PREFIX.

Note: This project is based on [monitor-docker-slack](https://github.com/DennyZhang/monitor-docker-slack)

# General Idea
1. Start one or more services in Docker Swarm mode.
2. Use this service to monitor the availability of services specified in the WHITE_LIST.
3. Send a pushover notifications containeing the unavailable services.

# How To Use: Docker-compose
```
version: '2'
services:
  swarm-alert:
    image: gpulidodt/swarm-alert:latest
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
    environment:
     - PUSHOVER_TOKEN="#XXX"
     - PUSHOVER_APP_KEY="XXX"
     - MSG_PREFIX="Monitoring On XX.XX.XX.XX"
     - WHITE_LIST="traefik_traefik,plex_plex,etc."
```

# Further customization
- Customize the message prefix for the Pushover Notification via the MSG_PREFIG variable:
```
 - MSG_PREFIX="Swarm services"
```
- Specify services in the Swarm  to be monitored via the WHITE_LIST variable:
```
 - WHITE_LIST="nodeexporter,ngin.*"
```


Code is licensed under MIT license
