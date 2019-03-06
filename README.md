# Introduction
Get Pushover Notifications when Services are not Running
Note: This project is based on the [monitor-docker-slack](https://github.com/DennyZhang/monitor-docker-slack)

# General Idea
1. Start a service in the swarm.
2. This service will query status for all services.
3. Send pushover notifications.

# How To Use: Plain Container
- Specify pushover credentials via env

```
export PUSHOVER_TOKEN="#XXX"
export PUSHOVER_APP_KEY="XXX"
export MSG_PREFIX="Monitoring On XX.XX.XX.XX"
```

- Start service to check

# How To Use: Docker-compose
```
version: '2'
services:
  monitor-docker-slack:
    container_name: monitor-docker-slack
    image: denny/monitor-docker-slack:latest
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
    environment:
      SLACK_CHANNEL: "#XXX"
      SLACK_USERNAME: "XXX"
      SLACK_TOKEN: "xoxp-XXX-XXX-XXX-XXXXXXXX"
      MSG_PREFIX: "Monitoring On XX.XX.XX.XX"
    restart: always
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