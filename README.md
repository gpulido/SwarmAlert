# Introduction
Get Pushover Notifications when Services are not Running
Note: This project is based on the [monitor-docker-slack](https://github.com/DennyZhang/monitor-docker-slack)

# General Idea
1. Start a service in the swarm.
2. This service will query status for all services.
3. Send pushover notifications.

# How To Use: Docker-compose
```
version: '2'
services:
  searm-alert:
    image: gpulidodt/swarm-alert:latest
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
    environment:
      PUSHOVER_TOKEN: "#XXX"
      PUSHOVER_APP_KEY: "XXX"
      MSG_PREFIX: "Monitoring On XX.XX.XX.XX"
```

# More customization
- Add message prefix for the slack notification
```
export MSG_PREFIX="Swarm services"
```
- Skip checking certain services by customizing WHITE_LIST env.
```
export MSG_PREFIX="Docker Env "
export WHITE_LIST="nodeexporter,ngin.*"
```
<

Code is licensed under MIT license
