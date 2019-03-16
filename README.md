[![Docker](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/docker.png)](https://cloud.docker.com/u/gpulidodt/repository/docker/gpulidodt/swarm-alert)

# Introduction
The SwarmAlert app monitors the availability of services running in a Docker Swarm environment. 

It offers an optional WHITELIST of services to monitor. If a WHITELIST is not defined, ALL services in the Swarm are monitored by default. 

An optional BLACKLIST is also configurable, and takes precedence over the whitelist and defaults. This is to allow you to use the BLACKLIST to avoid receiving alerts while doing planned maintenance. The app checks every CHECK_INTERVAL seconds. Upon checking, if a specified service has no running task, the app generates a Pushover Notification using the specified variables: 
  1. User Token
  2. Api Key
  3. Msg_Prefix

Note: This project is based on [monitor-docker-slack](https://github.com/DennyZhang/monitor-docker-slack)

# General Idea
1. Run one or more services in Docker Swarm mode.
2. Start this service to monitor the availability of other services.
3. Monitor services each CHECK_INTERVAL seconds for services with no running containers.
4. Send a pushover notifications containing the unavailable services.

# Usage: Docker-compose
```
version: '3'
services:
  swarm-alert:
    image: gpulidodt/swarm-alert:latest
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
    environment:
     - PUSHOVER_USER_KEY: user_key_from_pushover
     - PUSHOVER_API_TOKEN: your_app_token_from_pushover
     - MSG_PREFIX: '$MSG_PREFIX'
     - WHITE_LIST: ''traefik_traefik','plex_plex','test_service''
     - BLACK_LIST: ''test_service''
     - LOGGING_LEVEL: INFO | DEBUG
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
- Logging capabilities are included, it is set as INFO level by default, can be increased to DEBUG using the LOGGIN_LEVEL env variable.

Code is licensed under MIT license
